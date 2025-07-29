# IsItInstalled 🧰

**Check if your favorite CLI tools are installed — and where!**

---

## What is IsItInstalled?

IsItInstalled is a simple command-line tool that helps you quickly check if specific CLI tools or packages are installed on your system. It tells you:

- **Whether each tool is installed**
- **Where it is installed** (globally or inside a virtual environment)
- **The installed version**
- **How to install it if missing**

---

## Why Use It?

Ever forgotten if you installed a tool globally or just inside a Python virtual environment?  
Or struggled to remember the correct install command?  
IsItInstalled solves that instantly — no more guessing!

---

## 🚀 Installation

Make sure you have **Python 3.7+** installed.

Install IsItInstalled easily with pip:

```bash
pip install isitinstalled


💻 How to Use
Simply open your terminal and type:

>>

isitinstalled <tool1> <tool2> <tool3> ...
Replace <tool1>, <tool2>, etc., with the names of the tools you want to check.

📦 Example
Check if black, pip, and poetry are installed:

>>

isitinstalled black pip poetry
You’ll see a nice table like this:

Tool	Installed	Location	Version	Suggestion
black	✅	venv	23.7.0	-
pip	✅	global	24.0	-
poetry	❌	-	-	pip install poetry
