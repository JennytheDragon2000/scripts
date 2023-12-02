import os
with open('/home/srinath/scripts/env_vars.txt', 'w') as f:
    for key, value in os.environ.items():
        f.write(f'{key}={value}\n')

