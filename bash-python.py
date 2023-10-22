import subprocess
import pandas as pd
res = subprocess.check_output(["ls", "-la"]).decode("utf-8")
lines = res.split('\n')

for line in lines[1:]:
    print(line)

