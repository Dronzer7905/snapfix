import subprocess
import sys

res = subprocess.run(
    [r"C:\Users\Dronzer\Desktop\LogAnalyser\venv\Scripts\python.exe", "-m", "pylogai", "--help"],
    cwd=r"c:\Users\Dronzer\Desktop\LogAnalyser\pylogai",
    capture_output=True,
    text=True
)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
print("CODE:", res.returncode)
