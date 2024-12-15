# Discrete Speech Recognition Using HMM

## Introduction
This project implements a discrete speech recognition system based on Hidden Markov Models (HMM). The `setup.py` file is used to set up the development environment, including creating a virtual environment (`.venv`) and installing the required libraries from `requirements.txt`.

## Usage Guide

### 1. System Requirements
- **Python**: Version 3.6 or higher (check using `python --version`).
- **Pip**: Python's package manager (ensure it is installed).
- **Access Rights**: If using Windows, you may need to run commands with Administrator privileges.

### 2. Steps to Run

#### Step 1: Clone the Project
Download the project source code to your machine:
```bash
# Clone via Git
git clone https://github.com/tranhuutuan261103/discrete-speech-recognition-using-hmm.git

# Or download the ZIP file and extract it
```

Navigate to the project directory:
```bash
cd discrete-speech-recognition-using-hmm
```

#### Step 2: Run `setup.py`
Execute the `setup.py` file to create the virtual environment and install the libraries:
```bash
python setup.py
```

**When you run this command, the script will:**
1. Create a virtual environment in the `.venv` directory.
2. Install the libraries listed in `requirements.txt` into the virtual environment.

#### Step 3: Activate the Virtual Environment
Once the setup is complete, activate the virtual environment to run the project:

- **On Windows:**
  ```cmd
  .venv\Scripts\activate
  ```

- **On Linux/macOS:**
  ```bash
  source .venv/bin/activate
  ```

You should see the virtual environment's name (e.g., `.venv`) displayed in the terminal prompt.

#### Step 4: Run Project Scripts

#### Step 5: Deactivate the Virtual Environment
When finished, deactivate the virtual environment using:
```bash
deactivate
```

### 3. Troubleshooting

1. **Error: Python executable in virtual environment not found**
   - Check if the `.venv` directory was created.
   - Ensure you are using the correct Python version (3.6+).
   - Try creating the virtual environment manually:
     ```bash
     python -m venv .venv
     ```

2. **Error: Permission denied**
   - If using Windows, try running the terminal with Administrator privileges.

3. **Error: Missing required packages**
   - Ensure the `requirements.txt` file contains all necessary packages.
   - Reinstall dependencies using:
     ```bash
     pip install -r requirements.txt
     ```

