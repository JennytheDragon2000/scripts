import subprocess
output = subprocess.check_output("ls -l", shell=True)
output = output.decode("utf-8")

for i in output.split("\n"):
    print(i)



