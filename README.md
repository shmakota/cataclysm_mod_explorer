# Cataclysm Mod Explorer

A simple and intuitive Python Tkinter application designed to help you browse, search, and explore Cataclysm: Dark Days Ahead mod JSON files with ease.

Note: Initially vibe coded by me and ChatGPT. Code may not be the best quality!

![image](https://github.com/user-attachments/assets/f637baec-a53b-48aa-be50-bdc274af78c0)

---

## Features

- **Folder Browser:** Select any folder on your system and automatically load all valid mod JSON files contained within.
- **Powerful Search:** Quickly find mods by filtering through multiple fields including:
  - **Type** (e.g., item, recipe, monster)
  - **ID**
  - **Name**
  - **Description**
  - Or search across *all* fields simultaneously for maximum flexibility.
- **Detailed Mod View:** Select any entry from the list to see its detailed information alongside the complete raw JSON data for deep inspection or debugging.
- **Lightweight & Fast:** Built with Python’s Tkinter GUI framework to keep the app quick and responsive without heavy dependencies.

---

## Installation & Setup

### Prerequisites
- Python 3.x installed on your system
- Tkinter GUI library (usually included with Python)

### Running the App

Use the included scripts to quickly set up a Python virtual environment, install dependencies, and launch the app.

- **Windows:**
  1. Open Command Prompt in the app directory.
  2. Run `run_mod_viewer.bat`
- **Linux / macOS:**
  1. Open Terminal in the app directory.
  2. Run `./run_mod_viewer.sh` (make sure it’s executable via `chmod +x run_mod_viewer.sh`)

The scripts will:  
- Create a Python virtual environment in the local folder (if not present)  
- Install any required packages from `requirements.txt`  
- Launch `mod_viewer.py`

---

## Usage

1. **Launch the app** using the appropriate script.
2. **Browse** and select a folder containing your Cataclysm mod JSON files.
3. The app will load and display all mods in a sortable list.
4. Use the **search bar** to filter mods by any desired field.
5. Click on a mod to view detailed information and the full JSON content.
6. Explore, inspect, and manage your mod collection with ease!

---

## Troubleshooting

- If the app fails to start, ensure Python 3 and Tkinter are installed and accessible via your system PATH.
- For missing dependencies, try running the setup scripts again.
- On Windows, run Command Prompt as Administrator if you face permission issues.
- On macOS/Linux, verify the shell script has execution permission.

---

## Contributions & Feedback

Feel free to open issues or submit pull requests on the project’s GitHub repository. Contributions, bug reports, and feature requests are always welcome!

---

## License

TBD

---

