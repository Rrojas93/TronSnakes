
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.system("python3 -m pip install --upgrade pip")
os.system("python3 -m pip install setuptools")
os.system("python3 -m pip install -r requirements.txt")
os.system("sudo chmod +x ./*.py")