from calendar import c
from re import sub
import subprocess
import datetime
import os

if __name__ ==  "__main__":
    dirs = [int(d) for d in os.listdir('tests/reports/') if d.isdigit()]
    index = max(dirs) + 1 if len(dirs) > 0 else 1
    index_path = os.path.join('tests', 'reports', str(index))
    os.mkdir(index_path)
    for model in ["bert", "naive-bayes", "random-forest"]:
        model_path = os.path.join(index_path, model)
        os.mkdir(model_path)
        print(f"\n***** {model.upper()} *****\n")
        report_path = os.path.join(model_path, 'report.html')
        summary_path = os.path.join(model_path, 'summary.txt')
        output = subprocess.Popen([
            "behave", 
            "-f", "html", 
            "-o", os.path.join("..", report_path),
            "-D", f"cls={model}"]  
            , cwd="src", shell=True, stdout=subprocess.PIPE)
        summary = output.stdout.read().decode("utf-8")
        with open(summary_path, "w+") as f:
            f.write(summary)
        print(summary)