import importlib.metadata
import click
import os
import platform
import subprocess
import re
import json
from dotenv import load_dotenv, find_dotenv # For .env handling
from groq import Groq
from packaging.version import parse as parse_version, InvalidVersion
from packaging.specifiers import SpecifierSet, InvalidSpecifier
from pathlib import Path
import importlib.resources # For accessing package data
import xml.etree.ElementTree as ET
from appdirs import user_config_dir # For user-specific config directory

# --- "Trae IDE Effect" & Credits ---
# This project, DevEnv Genie, was proudly developed by Hamdaan Baloch
# during the Code Craft AI x Dev Hackathon, utilizing Trae IDE for an enhanced development experience.
DEVELOPER_CREDIT = "Developed by Hamdaan Baloch with Trae IDE for the Code Craft AI x Dev Hackathon."

# --- Configuration ---
GROQ_MODEL_FOR_EXTRACTION = "llama3-8b-8192"
GROQ_MODEL_FOR_SUGGESTION = "llama3-8b-8192"

# --- Configuration File Handling ---
APP_NAME = "DevEnvGenie"
APP_AUTHOR = "HamdaanBaloch" # Or your GitHub username, etc.
CONFIG_DIR = Path(user_config_dir(APP_NAME, APP_AUTHOR))
CONFIG_FILE = CONFIG_DIR / "config.json"

def get_tools_config_path():
    """Gets the path to tools_config.json, whether running from source or installed."""
    try:
        return importlib.resources.files('devenv_genie_pkg').joinpath('tools_config.json')
    except (ImportError, AttributeError, TypeError):
        return Path(__file__).resolve().parent / "tools_config.json"

TOOLS_CONFIG_PATH = get_tools_config_path()

# --- Global Variables ---
client = None
tools_config = {} # This will be populated by load_tools_config_data

def load_tools_config_data():
    global tools_config # Explicitly state we are modifying the global variable
    try:
        with open(TOOLS_CONFIG_PATH, 'r', encoding='utf-8') as f:
            tools_config = json.load(f)
    except FileNotFoundError:
        click.echo(click.style(f"Critical Error: {TOOLS_CONFIG_PATH} not found. Installation might be corrupt.", fg="red"), err=True)
        raise click.Abort()
    except json.JSONDecodeError:
        click.echo(click.style(f"Critical Error: Could not decode {TOOLS_CONFIG_PATH}. Installation might be corrupt.", fg="red"), err=True)
        raise click.Abort()

def save_api_key_to_config(api_key: str):
    """Saves the API key to the user's config file."""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({"GROQ_API_KEY": api_key}, f, indent=2)
        click.echo(click.style(f"Groq API key saved to: {CONFIG_FILE}", fg="green"))
    except Exception as e:
        click.echo(click.style(f"Error saving API key to {CONFIG_FILE}: {e}", fg="red"), err=True)

def load_api_key_from_config() -> str | None:
    """Loads the API key from the user's config file."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                return config_data.get("GROQ_API_KEY")
        except Exception:
            return None
    return None

def initialize_groq_client():
    global client # Explicitly state we are modifying the global variable
    api_key = None
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        load_dotenv(find_dotenv(usecwd=True, raise_error_if_not_found=False))
        api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        api_key = load_api_key_from_config()

    if not api_key:
        click.echo(click.style("Error: GROQ_API_KEY not found.", fg="red") +
                    " Please set it using 'genie config set-key', as an environment variable, "
                    "or in a .env file in your current directory.", err=True)
        raise click.Abort()
    client = Groq(api_key=api_key)

# --- LLM Interaction Functions ---
def get_llm_response(prompt_text, system_prompt, model_name, is_json_output=True):
    if not client: # Should have been initialized before this is called by a command
        click.echo(click.style("Groq client not initialized. This indicates an issue in command setup.", fg="red"), err=True)
        return None
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_text}
            ],
            model=model_name,
            temperature=0.2,
            max_tokens=1024,
        )
        response_content = chat_completion.choices[0].message.content.strip()
        if is_json_output:
            match = re.search(r'```json\s*([\s\S]*?)\s*```', response_content)
            json_str = match.group(1).strip() if match else response_content.strip()
            try:
                start_index = json_str.find('{')
                end_index = json_str.rfind('}')
                if start_index != -1 and end_index != -1 and end_index > start_index:
                    json_str_cleaned = json_str[start_index : end_index + 1].strip()
                    return json.loads(json_str_cleaned)
                else:
                    click.echo(click.style(f"LLM did not return a recognizable JSON object structure. Raw: '{response_content}'", fg="yellow"), err=True)
                    return None
            except (ValueError, json.JSONDecodeError) as e_parse:
                click.echo(click.style(f"LLM JSON Parsing Error: {e_parse}. Raw: '{response_content}'", fg="yellow"), err=True)
                return None
        return response_content
    except Exception as e:
        click.echo(click.style(f"Error communicating with Groq LLM ({model_name}): {e}", fg="red"), err=True)
        return None

def extract_requirements_from_llm(description_text):
    system_prompt = (
        "You are an expert system that extracts software development environment requirements from text. "
        "Output ONLY a valid JSON object. The JSON object should have a single top-level key 'requirements', "
        "which is a list of objects. Each object should have 'name' (e.g., 'Python', 'Node.js', 'Git') "
        "and 'version_required' (e.g., '3.9.x', '>=18.0.0', 'any'). If an OS is hinted, include an 'os_hint' key at the top level. "
        "Example: {\"os_hint\": \"macOS\", \"requirements\": [{\"name\": \"Python\", \"version_required\": \"3.9.x\"}]}"
    )
    prompt = f"Extract development environment requirements from the following description. Focus on specific versions if mentioned. Description: \"{description_text}\""
    return get_llm_response(prompt, system_prompt, GROQ_MODEL_FOR_EXTRACTION, is_json_output=True)

def get_fix_suggestion_from_llm(tool_name, required_version, found_version, target_os, version_manager_hint=None):
    vm_guidance = ""
    if version_manager_hint:
        vm_guidance = f" If a version manager like '{version_manager_hint}' is commonly used for '{tool_name}', prefer suggesting commands for it."

    system_prompt = (
        "You are an expert DevOps assistant. Provide concise, actionable installation or update advice for software development tools. "
        "Focus on common package managers (apt/apt-get for linux-debian/ubuntu, yum/dnf for linux-redhat/fedora, brew for macos, choco/winget for windows)."
        f"{vm_guidance} "
        "Output ONLY a valid JSON object with keys 'suggestion_command' and 'suggestion_link'. "
        "The command should be a single, runnable shell command. The link should be to an official download or guide. "
        "Example: {\"suggestion_command\": \"sudo apt update && sudo apt install -y nodejs\", \"suggestion_link\": \"https://nodejs.org/\"}"
    )
    if found_version.lower() == "not found":
        user_message = f"The tool '{tool_name}' (required version: {required_version}) was not found on a {target_os} system. Provide a JSON response with 'suggestion_command' to install it and 'suggestion_link' for more info."
    else:
        user_message = f"The tool '{tool_name}' requires version '{required_version}' but version '{found_version}' was found on a {target_os} system. Provide a JSON response with 'suggestion_command' to update/change to the required version and 'suggestion_link' for more info."

    return get_llm_response(user_message, system_prompt, GROQ_MODEL_FOR_SUGGESTION, is_json_output=True)


# --- File Parsers ---
def parse_requirements_txt(filepath: Path):
    requirements = []
    python_version_specified = False
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    if "python" in line.lower() and re.search(r'(\d+\.\d+)', line):
                        match = re.search(r'([><=~!]*\s*\d+\.\d+(\.\d+)*([a-zA-Z0-9.+-]*)?)', line, re.IGNORECASE)
                        if match:
                            requirements.append({"name": "python", "version_required": match.group(1).strip()})
                            python_version_specified = True
                    continue
        if not python_version_specified:
             requirements.append({"name": "python", "version_required": "any"})
        return {"requirements": requirements}
    except FileNotFoundError:
        click.echo(click.style(f"File not found: {filepath}", fg="yellow"), err=True)
        return None
    except Exception as e:
        click.echo(click.style(f"Error parsing {filepath}: {e}", fg="yellow"), err=True)
        return None

def parse_package_json(filepath: Path):
    requirements = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if "engines" in data:
                if "node" in data["engines"]:
                    requirements.append({"name": "node", "version_required": data["engines"]["node"]})
                if "npm" in data["engines"]:
                    requirements.append({"name": "npm", "version_required": data["engines"]["npm"]})
        return {"requirements": requirements} if requirements else None
    except FileNotFoundError:
        click.echo(click.style(f"File not found: {filepath}", fg="yellow"), err=True)
        return None
    except json.JSONDecodeError:
        click.echo(click.style(f"Error decoding JSON from {filepath}", fg="yellow"), err=True)
        return None
    except Exception as e:
        click.echo(click.style(f"Error parsing {filepath}: {e}", fg="yellow"), err=True)
        return None

def parse_pyproject_toml(filepath: Path):
    requirements = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'requires-python\s*=\s*["\']([^"\']+)["\']', content, re.IGNORECASE)
            if not match:
                match = re.search(r'\[tool\.poetry\.dependencies\]\s*python\s*=\s*["\']([^"\']+)["\']', content, re.DOTALL | re.IGNORECASE)
            if match:
                requirements.append({"name": "python", "version_required": match.group(1).strip()})
            else:
                requirements.append({"name": "python", "version_required": "any"})
        return {"requirements": requirements}
    except FileNotFoundError:
        click.echo(click.style(f"File not found: {filepath}", fg="yellow"), err=True)
        return None
    except Exception as e:
        click.echo(click.style(f"Error parsing {filepath}: {e}", fg="yellow"), err=True)
        return None

def parse_pom_xml(filepath: Path):
    requirements = []
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
        java_version_element = root.find('.//m:properties/m:java.version', ns)
        if java_version_element is None:
            java_version_element = root.find('.//m:properties/m:maven.compiler.source', ns)
        if java_version_element is None:
            java_version_element = root.find('.//m:properties/m:java.source.version', ns)
        if java_version_element is not None and java_version_element.text:
            requirements.append({"name": "java", "version_required": java_version_element.text.strip()})
        else:
            requirements.append({"name": "java", "version_required": "any"})
        requirements.append({"name": "maven", "version_required": "any"})
        return {"requirements": requirements}
    except FileNotFoundError:
        click.echo(click.style(f"File not found: {filepath}", fg="yellow"), err=True)
        return None
    except ET.ParseError:
        click.echo(click.style(f"Error parsing XML from {filepath}", fg="yellow"), err=True)
        return {"requirements": [{"name": "java", "version_required": "any"}, {"name": "maven", "version_required": "any"}]}
    except Exception as e:
        click.echo(click.style(f"Error parsing {filepath}: {e}", fg="yellow"), err=True)
        return None

def parse_build_gradle(filepath: Path):
    requirements = []
    java_version = "any"
    gradle_version = "any"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            match_java = re.search(r'(sourceCompatibility|targetCompatibility)\s*=\s*( JavaVersion\.VERSION_|["\']?)(\d+(_\d+)?|\d\.\d)["\']?', content, re.IGNORECASE)
            if match_java:
                version_text = match_java.group(3)
                if version_text.startswith("VERSION_"):
                    java_version = version_text.split('_')[-1]
                elif "_" in version_text:
                    java_version = version_text.replace("_",".")
                else:
                    java_version = version_text
            requirements.append({"name": "java", "version_required": java_version})
            requirements.append({"name": "gradle", "version_required": gradle_version})
        return {"requirements": requirements}
    except FileNotFoundError:
        click.echo(click.style(f"File not found: {filepath}", fg="yellow"), err=True)
        return None
    except Exception as e:
        click.echo(click.style(f"Error parsing {filepath}: {e}", fg="yellow"), err=True)
        return None

def parse_gradle_wrapper_properties(filepath: Path):
    requirements = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'distributionUrl=.*gradle-([0-9.]+)-bin\.zip', content)
            if match:
                requirements.append({"name": "gradle", "version_required": match.group(1)})
            else:
                requirements.append({"name": "gradle", "version_required": "any"})
        return {"requirements": requirements}
    except FileNotFoundError:
        click.echo(click.style(f"File not found: {filepath}", fg="yellow"), err=True)
        return None
    except Exception as e:
        click.echo(click.style(f"Error parsing {filepath}: {e}", fg="yellow"), err=True)
        return None

def parse_go_mod(filepath: Path):
    requirements = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'^go\s+([0-9]+\.[0-9]+(\.[0-9]+)?)\s*$', content, re.MULTILINE | re.IGNORECASE)
            if match:
                requirements.append({"name": "go", "version_required": match.group(1)})
            else:
                requirements.append({"name": "go", "version_required": "any"})
        return {"requirements": requirements}
    except FileNotFoundError:
        click.echo(click.style(f"File not found: {filepath}", fg="yellow"), err=True)
        return None
    except Exception as e:
        click.echo(click.style(f"Error parsing {filepath}: {e}", fg="yellow"), err=True)
        return None

def parse_cargo_toml(filepath: Path):
    requirements = []
    rust_version = "any"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            match_edition = re.search(r'\[package\][^\[]*\s*edition\s*=\s*["\'](\d{4})["\']', content, re.DOTALL | re.IGNORECASE)
            match_rust_ver = re.search(r'\[package\][^\[]*\s*rust-version\s*=\s*["\']([^"\']+)["\']', content, re.DOTALL | re.IGNORECASE)
            if match_rust_ver:
                rust_version = match_rust_ver.group(1).strip()
            elif match_edition:
                edition_year = match_edition.group(1)
                if edition_year == "2015": rust_version = ">=1.0"
                elif edition_year == "2018": rust_version = ">=1.31"
                elif edition_year == "2021": rust_version = ">=1.56"
                elif edition_year == "2024": rust_version = ">=1.75"
            requirements.append({"name": "rust", "version_required": rust_version})
        return {"requirements": requirements}
    except FileNotFoundError:
        click.echo(click.style(f"File not found: {filepath}", fg="yellow"), err=True)
        return None
    except Exception as e:
        click.echo(click.style(f"Error parsing {filepath}: {e}", fg="yellow"), err=True)
        return None

def parse_gemfile(filepath: Path):
    requirements = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r"ruby\s+['\"]([^'\"]+)['\"]", content, re.IGNORECASE)
            if match:
                requirements.append({"name": "ruby", "version_required": match.group(1)})
            else:
                requirements.append({"name": "ruby", "version_required": "any"})
        return {"requirements": requirements}
    except FileNotFoundError:
        click.echo(click.style(f"File not found: {filepath}", fg="yellow"), err=True)
        return None
    except Exception as e:
        click.echo(click.style(f"Error parsing {filepath}: {e}", fg="yellow"), err=True)
        return None

def parse_generic_version_file(filepath: Path, tool_name: str):
    requirements = []
    try:
        version = get_version_from_project_file(filepath)
        if version:
            requirements.append({"name": tool_name, "version_required": version})
        else:
            requirements.append({"name": tool_name, "version_required": "any"})
        return {"requirements": requirements}
    except Exception as e:
        click.echo(click.style(f"Error parsing generic version file {filepath} for {tool_name}: {e}", fg="yellow"), err=True)
        requirements.append({"name": tool_name, "version_required": "any"})
        return {"requirements": requirements}

# --- System Check Functions ---
def get_local_version_from_command(command_str):
    try:
        parts = command_str.split('||')[0].strip().split()
        process = subprocess.run(parts, capture_output=True, text=True, timeout=5, check=False, shell=False)
        output = process.stdout + process.stderr
        if process.returncode == 0 or "version" in output.lower():
            match = re.search(r'(\d+\.\d+(\.\d+([a-zA-Z0-9.-]*))?)', output)
            if match: return match.group(1)
            match = re.search(r'(\d+\.\d+)', output)
            if match: return match.group(1)
        if '||' in command_str: # Try alternative command if first failed or no version found
            alt_command_parts = command_str.split('||')[1].strip().split()
            process_alt = subprocess.run(alt_command_parts, capture_output=True, text=True, timeout=5, check=False, shell=False)
            output_alt = process_alt.stdout + process_alt.stderr
            if process_alt.returncode == 0 or "version" in output_alt.lower():
                match_alt = re.search(r'(\d+\.\d+(\.\d+([a-zA-Z0-9.-]*))?)', output_alt)
                if match_alt: return match_alt.group(1)
                match_alt = re.search(r'(\d+\.\d+)', output_alt)
                if match_alt: return match_alt.group(1)
        return "Not Found"
    except subprocess.TimeoutExpired: return "Timeout"
    except FileNotFoundError: return "Not Found"
    except Exception: return "Error running command"

def get_version_from_project_file(filepath: Path):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            version = f.readline().strip()
            if version.startswith('v'):
                version = version[1:]
            return version if version else None
    except FileNotFoundError:
        return None
    except Exception:
        return None

def check_single_requirement(tool_key, initial_req_version_str, current_os):
    # Access the global tools_config populated by load_tools_config_data()
    global tools_config
    tool_info = tools_config.get(tool_key)
    if not tool_info:
        for t_key_alias, t_info_alias in tools_config.items():
            if tool_key.lower() in [a.lower() for a in t_info_alias.get("aliases", [])]:
                tool_key = t_key_alias 
                tool_info = t_info_alias
                break
        if not tool_info: 
             click.echo(click.style(f"Warning: Tool definition for '{tool_key}' (from input '{initial_req_version_str}') not found in tools_config.json. Skipping.", fg="yellow"), err=True)
             return None

    display_name = tool_info.get("display_name", tool_key)
    version_command = tool_info.get("version_command")
    project_version_filepath_str = tool_info.get("project_version_file")
    effective_req_version_str = initial_req_version_str
    version_source = "description/file" 

    if project_version_filepath_str:
        current_path = Path.cwd()
        for i in range(4): 
            path_to_check = current_path / project_version_filepath_str
            if path_to_check.exists():
                proj_ver = get_version_from_project_file(path_to_check)
                if proj_ver:
                    effective_req_version_str = proj_ver
                    relative_prefix = "./" if i == 0 else "../" * i
                    version_source = f"{relative_prefix}{project_version_filepath_str}"
                    break
            if current_path.parent == current_path: 
                break
            current_path = current_path.parent

    local_version_str = "Not Found"
    if version_command:
        local_version_str = get_local_version_from_command(version_command)
    else:
        click.echo(click.style(f"Warning: No version_command for {display_name} in config. Skipping checks for this tool.", fg="yellow"), err=True)
        return {
            "key": tool_key, "name": display_name, "required_raw": initial_req_version_str,
            "effective_required": effective_req_version_str, "version_source": version_source,
            "found": "Check Skipped", "satisfied": False, "checked_command": None
        }

    satisfied = False
    normalized_req_version = str(effective_req_version_str).lower().replace(".x", "").replace("*", "")

    if local_version_str.lower() not in ["not found", "error running command", "timeout", "check skipped"]:
        if normalized_req_version == "any":
            satisfied = True
        else:
            try:
                spec_str_prep = str(effective_req_version_str).replace(".x", ".*")
                if not any(c in spec_str_prep for c in '><=!~'):
                    if "." in spec_str_prep and spec_str_prep.endswith(".*"):
                        spec_str = f"=={spec_str_prep}"
                    else:
                         spec_str = f"=={spec_str_prep}"
                else:
                    spec_str = spec_str_prep
                spec = SpecifierSet(spec_str, prereleases=True)
                parsed_local_ver = parse_version(local_version_str)
                satisfied = parsed_local_ver in spec
            except (InvalidSpecifier, InvalidVersion) as e_spec:
                click.echo(click.style(f"  Debug: Version spec error for '{display_name}' (req: '{effective_req_version_str}', local: '{local_version_str}'): {e_spec}", fg="magenta"), err=True)
                try:
                    satisfied = parse_version(local_version_str).base_version.startswith(parse_version(normalized_req_version).base_version)
                except InvalidVersion:
                    satisfied = local_version_str.startswith(normalized_req_version)
            except TypeError as e_type:
                 click.echo(click.style(f"  Debug: Type error in version spec for '{display_name}' (req: '{effective_req_version_str}'): {e_type}", fg="magenta"), err=True)
                 satisfied = False
    return {
        "key": tool_key, "name": display_name, "required_raw": initial_req_version_str,
        "effective_required": effective_req_version_str, "version_source": version_source,
        "found": local_version_str, "satisfied": satisfied, "checked_command": version_command
    }

# --- Click CLI Commands ---
@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(
    version=importlib.metadata.version("devenv-genie"), # Assumes your package name in pyproject.toml is "devenv-genie"
    prog_name="genie",
    message="%(prog)s version %(version)s\n" + DEVELOPER_CREDIT
)
@click.pass_context
def cli(ctx):
    """
    DevEnv Genie 🧞‍♂️: AI-Powered Dev Environment Diagnoser & Fixer.
    Helps set up and troubleshoot local dev environments.
    """
    ctx.obj = {} # Initialize context object for subcommands

@cli.group()
@click.pass_context
def config(ctx):
    """Manage DevEnv Genie configuration."""
    # No immediate setup needed here for 'set-key'
    pass

@config.command(name="set-key")
@click.option('--key', prompt="Enter your Groq API key", hide_input=True,
              help="Your Groq API key.")
# No ctx needed for set_api_key if it doesn't use parent context
def set_api_key(key): # Removed ctx as it's not used
    """Saves your Groq API key for DevEnv Genie to use."""
    if not key or not key.strip():
        click.echo(click.style("API key cannot be empty.", fg="red"), err=True)
        return
    save_api_key_to_config(key.strip())

@cli.command()
@click.option('--description', '-d', help="Text description of project requirements.")
@click.option('--file', '-f', type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
              help="Project file to parse (e.g., package.json, requirements.txt).")
@click.option('--os-target', default=None, help="Target OS (linux, macos, windows). Auto-detects if not set.")
@click.pass_context
def diagnose(ctx, description, file: Path | None, os_target):
    """Diagnoses the local environment based on project description or file."""
    global tools_config # Ensure we are using the global tools_config
    try:
        # Ensure tools_config is loaded. load_tools_config_data() populates the global.
        if not tools_config: # If global tools_config is empty, try loading
            load_tools_config_data()
        
        # Ensure Groq client is initialized
        initialize_groq_client()
    except click.Abort: # Abort from initialize_groq_client or load_tools_config_data
        return

    if not client: # Safeguard, should be handled by initialize_groq_client
        click.echo(click.style("Groq client could not be initialized.", fg="red"), err=True)
        return
    if not tools_config: # Safeguard
        click.echo(click.style("Tools configuration could not be loaded.", fg="red"), err=True)
        return

    if not description and not file:
        click.echo(click.style("Error: Please provide either a --description or a --file.", fg="red"), err=True)
        return

    click.echo(click.style(f"🧞‍♂️ DevEnv Genie analyzing...", bold=True))
    initial_parsed_reqs_data = None
    source_of_reqs = ""

    if file: 
        source_of_reqs = f"file ({file.name})"
        filename_lower = file.name.lower()
        parsed_data_from_file = None 

        if "requirements.txt" == filename_lower:
            parsed_data_from_file = parse_requirements_txt(file)
        elif "pyproject.toml" == filename_lower:
            parsed_data_from_file = parse_pyproject_toml(file)
        elif "package.json" == filename_lower:
            parsed_data_from_file = parse_package_json(file)
        elif "pom.xml" == filename_lower:
            parsed_data_from_file = parse_pom_xml(file)
        elif "build.gradle" in filename_lower: 
            parsed_data_from_file = parse_build_gradle(file)
        elif "gradle-wrapper.properties" in filename_lower:
            if file.parent.name == "wrapper" and file.parent.parent.name == "gradle":
                 parsed_data_from_file = parse_gradle_wrapper_properties(file)
            else:
                 click.echo(click.style(f"Info: Parsing '{file.name}' for Gradle version. For best results, ensure it's 'gradle/wrapper/gradle-wrapper.properties'.", fg="blue"), err=True)
                 parsed_data_from_file = parse_gradle_wrapper_properties(file)
        elif "go.mod" == filename_lower:
            parsed_data_from_file = parse_go_mod(file)
        elif "cargo.toml" == filename_lower:
            parsed_data_from_file = parse_cargo_toml(file)
        elif "gemfile" == filename_lower: 
            parsed_data_from_file = parse_gemfile(file)
        elif ".ruby-version" == filename_lower:
            parsed_data_from_file = parse_generic_version_file(file, "ruby")
        elif ".java-version" == filename_lower:
            parsed_data_from_file = parse_generic_version_file(file, "java")
        elif ".nvmrc" == filename_lower:
            parsed_data_from_file = parse_generic_version_file(file, "node")
        elif "dockerfile" == filename_lower:
            parsed_data_from_file = {"requirements": [{"name": "docker", "version_required": "any"}]}
        elif "docker-compose.yml" == filename_lower or "docker-compose.yaml" == filename_lower:
            parsed_data_from_file = {"requirements": [
                {"name": "docker", "version_required": "any"},
                {"name": "docker-compose", "version_required": "any"}
            ]}
        elif filename_lower.endswith((".tf", ".tfvars", ".terraform.lock.hcl")):
             parsed_data_from_file = {"requirements": [{"name": "terraform", "version_required": "any"}]}
        
        if parsed_data_from_file:
            initial_parsed_reqs_data = parsed_data_from_file
        else:
            click.echo(click.style(f"Warning: File type '{file.name}' not directly supported for detailed parsing or no requirements found. Try using --description.", fg="yellow"), err=True)
            if not description: return 
    
    if not initial_parsed_reqs_data and description:
        source_of_reqs = "description"
        initial_parsed_reqs_data = extract_requirements_from_llm(description)
    
    if not initial_parsed_reqs_data or "requirements" not in initial_parsed_reqs_data or not isinstance(initial_parsed_reqs_data.get("requirements"), list):
        click.echo(click.style(f"Could not parse requirements from {source_of_reqs}. Please check the input.", fg="red"), err=True)
        return

    click.echo(click.style(f"\n📋 Initial Requirements (from {source_of_reqs}):", fg="cyan", bold=True))
    click.echo(json.dumps(initial_parsed_reqs_data, indent=2))

    current_os_detected = platform.system().lower()
    if "darwin" in current_os_detected: current_os_detected = "macos"
    elif "win" in current_os_detected: current_os_detected = "windows"
    
    if os_target:
        final_os_target = os_target.lower()
    else:
        os_hint_from_llm = initial_parsed_reqs_data.get("os_hint")
        if os_hint_from_llm and isinstance(os_hint_from_llm, str):
            final_os_target = os_hint_from_llm.lower()
        else:
            final_os_target = current_os_detected
    click.echo(click.style(f"\n💻 Targeting OS: {final_os_target} (Detected: {current_os_detected})", bold=True))

    all_results = []
    click.echo(click.style("\n🔍 Diagnosis Results:", fg="cyan", bold=True))

    requirements_to_check = initial_parsed_reqs_data.get("requirements", [])
    if not requirements_to_check:
        click.echo("No checkable requirements found.")
        return

    for item in requirements_to_check:
        tool_name_from_req = item.get('name', '') 
        initial_version_req = item.get('version_required', 'any')
        
        canonical_tool_key = None
        tool_name_lower = tool_name_from_req.lower()
        for t_key, t_info in tools_config.items(): # Uses global tools_config
            if tool_name_lower == t_key.lower() or tool_name_lower in [a.lower() for a in t_info.get("aliases", [])]:
                canonical_tool_key = t_key 
                break
        
        if not canonical_tool_key:
            click.echo(click.style(f"Warning: Tool '{tool_name_from_req}' from requirements is not defined in tools_config.json. Skipping.", fg="yellow"), err=True)
            continue

        res = check_single_requirement(canonical_tool_key, initial_version_req, final_os_target) # Uses global tools_config
        if not res: continue

        all_results.append(res)
        status_symbol = "✅" if res['satisfied'] else "❌"
        status_color = "green" if res['satisfied'] else "red"
        found_color = "green" if res['satisfied'] else ("yellow" if res['found'].lower() != "not found" else "red")
        
        version_info = f"Required: {res['effective_required']}"
        if isinstance(res['version_source'], str) and \
           res['version_source'] != "description/file" and \
           res['version_source'] != res['effective_required']: 
            version_info += f" (from {res['version_source']})"
        
        click.echo(
            f"{status_symbol} {click.style(res['name'], bold=True)}: " 
            f"{version_info}, "
            f"Found: {click.style(res['found'], fg=found_color)} "
            f"({click.style('OK' if res['satisfied'] else 'ISSUE', fg=status_color, bold=True)})"
        )

        if not res['satisfied']:
            click.echo(click.style("   ⏳ Getting AI suggestion...", fg="magenta"))
            tool_cfg_for_suggestion = tools_config.get(res['key'], {}) # Uses global tools_config
            vm_hint = tool_cfg_for_suggestion.get("version_manager_hint")
            
            suggestion_data = get_fix_suggestion_from_llm(
                res['name'], res['effective_required'], res['found'], final_os_target, vm_hint
            )
            if suggestion_data and isinstance(suggestion_data, dict):
                cmd = suggestion_data.get('suggestion_command')
                link = suggestion_data.get('suggestion_link')
                if cmd: click.echo(click.style(f"   💡 Suggestion: {click.style(cmd, bold=True)}", fg="yellow"))
                if link: click.echo(click.style(f"   🔗 More Info: {link}", fg="blue"))
            else:
                click.echo(click.style("   ⚠️ Could not get AI suggestion for this item.", fg="yellow"), err=True)
    click.echo(click.style("\n✨ Diagnosis Complete.", bold=True))
    click.echo(click.style(f"\n---\n{DEVELOPER_CREDIT}", dim=True))

if __name__ == "__main__":
    cli()