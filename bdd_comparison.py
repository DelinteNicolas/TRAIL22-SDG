from calendar import c
import subprocess
import datetime
import os

if __name__ ==  "__main__":
    dirs = [d for d in os.listdir('tests/reports/') if os.path.isdir(d)]
    index = len(dirs) + 1
    for model in ["bert", "naive-bayes", "random-forest"]:
        print(f"\n***** {model.upper()} *****\n")
        output = subprocess.Popen([
            "behave", 
            "-f", "html", 
            "-o", f"../tests/reports/{index}/report-{model}.html",
            "-D", f"cls={model}"]  
            , cwd="src", shell=True, stdout=subprocess.PIPE)
        print(output.stdout.read().decode("utf-8"))