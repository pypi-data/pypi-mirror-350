# DevEnv Genie 🧞‍♂️

**AI-Powered Dev Environment Diagnoser & Fixer.**

DevEnv Genie is a command-line tool designed to help developers quickly set up and troubleshoot their local development environments. It intelligently parses project requirements, checks your local system, and leverages AI (via Groq LPU with Llama 3) to provide OS-specific fix suggestions.

---

**Developed by: Hamdaan Baloch**
*   **LinkedIn:** [linkedin.com/in/your-linkedin-profile](https://pk.linkedin.com/in/hamdaan-baloch-3ba3b51ab) 
*   **Project for:** Code Craft AI x Dev Hackathon
*   **Development Environment:** Proudly built using Trae IDE

---

## Key Features

*   **Smart Requirement Parsing:** Understands requirements from text descriptions or common project files (e.g., `package.json`, `requirements.txt`).
*   **Local Environment Diagnosis:** Checks installed tool versions on your system.
*   **Project-Specific Version Detection:** Recognizes versions defined in files like `.nvmrc` or `.python-version` within your project.
*   **AI-Powered Fix Suggestions:** Uses Groq's Llama 3 to generate OS-specific command-line fixes for discrepancies.
*   **Version Manager Aware:** Provides hints for common version managers (nvm, pyenv, sdkman).
*   **Cross-Platform:** Offers suggestions tailored for macOS, Linux, and Windows.
*   **Easy to Use CLI:** Simple and intuitive command-line interface.

## Installation

You can install DevEnv Genie using pip:

```bash
pip install devenv-genie

API Key Setup
DevEnv Genie requires a Groq API key to leverage its AI capabilities.
Obtain a free API key from GroqCloud.
Make the key available to DevEnv Genie in one of two ways:
Recommended: Environment Variable: Set GROQ_API_KEY as a system environment variable.

For example, on Linux:
export GROQ_API_KEY=your-api-key
```

Alternative: .env File: Create a file named .env in the directory where you run the genie command and add your key:
```bash
GROQ_API_KEY=your-api-key
```

## Usage

To use DevEnv Genie, simply run the command:

```bash
genie diagnose
```

DevEnv Genie will analyze your project and suggest fixes for any discrepancies. 

#Usage

Once installed and the API key is configured, you can use the genie command from your terminal:
1. Diagnose based on a text description:
genie diagnose --description "My project needs Python 3.10, Node.js version 18.x, and git. I'm on macOS."
Use code with caution.
Bash
Shorthand:
genie diagnose -d "Python 3.9, npm 8"
Use code with caution.

2. Diagnose based on a project file:
Supported files include package.json (for Node.js/npm versions from engines) and requirements.txt (for Python version hints from comments).
genie diagnose --file ./package.json
genie diagnose -f ./project/requirements.txt```
*(DevEnv Genie will also automatically look for `.nvmrc`, `.python-version`, etc., in the current or parent directories.)*

**3. Specify target OS (otherwise auto-detected):**

genie diagnose -d "Java 17, Maven" --os-target windows
Use code with caution.
Bash
4. Get help or version information:
genie --help
genie diagnose --help
genie --version

#Example Output

$ genie diagnose -d "Python 3.9, Node 20, but I have Node 18. OS is macOS"

🧞‍♂️ DevEnv Genie analyzing...

📋 Initial Requirements (from description):
{
  "os_hint": "macOS",
  "requirements": [
    { "name": "Python", "version_required": "3.9" },
    { "name": "Node", "version_required": "20" }
  ]
}

💻 Targeting OS: macos (Detected: macos)

🔍 Diagnosis Results:
✅ Python: Required: 3.9 (from .python-version), Found: 3.9.13 (OK)
❌ Node.js: Required: 20, Found: 18.17.0 (ISSUE)
   ⏳ Getting AI suggestion...
   💡 Suggestion: nvm install 20 && nvm use 20 && nvm alias default 20
   🔗 More Info: https://github.com/nvm-sh/nvm

✨ Diagnosis Complete.

---
Developed by Hamdaan Baloch with Trae IDE for the Code Craft AI x Dev Hackathon.