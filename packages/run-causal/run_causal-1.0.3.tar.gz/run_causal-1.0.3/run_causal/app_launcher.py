import subprocess
import os

def main():
    script_path = os.path.join(os.path.dirname(__file__), "causal_forecast.py")
    subprocess.run(["streamlit", "run", script_path])
