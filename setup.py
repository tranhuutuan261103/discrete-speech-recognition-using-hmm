import os
import subprocess
import sys

def create_venv():
    """Tạo môi trường ảo nếu chưa tồn tại."""
    venv_path = '.venv'
    if not os.path.exists(venv_path):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
    else:
        print("Virtual environment already exists.")

def install_requirements():
    """Cài đặt các gói từ requirements.txt trong môi trường ảo."""
    venv_python = os.path.join(os.getcwd(), '.venv', 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join(os.getcwd(), '.venv', 'bin', 'python')
    if not os.path.exists(venv_python):
        raise FileNotFoundError("Python executable in virtual environment not found. Did venv creation fail?")
    
    print("Installing requirements...")
    subprocess.check_call([venv_python, '-m', 'pip', 'install', '--upgrade', 'pip'])  # Update pip
    subprocess.check_call([venv_python, '-m', 'pip', 'install', '-r', 'requirements.txt'])

def main():
    create_venv()
    install_requirements()
    print("\nSetup complete. Activate the virtual environment with:")
    print("  source .venv/bin/activate" if os.name != 'nt' else ".venv\\Scripts\\activate")

if __name__ == '__main__':
    main()