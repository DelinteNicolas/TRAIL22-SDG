from calendar import c
from re import sub
import subprocess
import datetime
import os

def report(index_path, model, version="0.0.5"):
    dir_name = model if model != "bert" else f"{model}-{version}"
    dir_path = os.path.join(index_path, dir_name)
    os.mkdir(dir_path)
    print(f"\n***** {dir_name.upper()} *****\n")
    report_path = os.path.join(dir_path, 'report.html')
    summary_path = os.path.join(dir_path, 'summary.txt')
    output = subprocess.Popen([
            "behave", 
            "-f", "html", 
            "-o", os.path.join("..", report_path),
            "-D", f"model={model}",
            "-D", f"version={version}"]  
            , cwd="src", shell=True, stdout=subprocess.PIPE)
    summary = output.stdout.read().decode("utf-8")
    with open(summary_path, "w+") as f:
        f.write(summary)
    print(summary)

if __name__ ==  "__main__":
    dirs = [int(d) for d in os.listdir('tests/reports/') if d.isdigit()]
    index = max(dirs) + 1 if len(dirs) > 0 else 1
    index_path = os.path.join('tests', 'reports', str(index))
    os.mkdir(index_path)
    report(index_path, "bert", "0.0.5") # class 0 using GLUE
    report(index_path, "bert", "0.0.4") # class 0 using superGLUE
    report(index_path, "bert", "0.0.2") # no class 0
    report(index_path, "naive-bayes")
    report(index_path, "naive-bayes", "prior")
    report(index_path, "random-forest")