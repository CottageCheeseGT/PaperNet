import os
import subprocess

batch_size = 1000
result = subprocess.run(['wc', '-l', 'ids'], stdout=subprocess.PIPE)
total_size = int(result.stdout.decode('utf-8').split(" ")[0])
for start in range(0, total_size, batch_size):
        os.system('rm -r papers/*')
        end = min(start + 1000, total_size)
        os.system(f"awk 'FNR>={start} && FNR<{end}' ids | gsutil -m cp -I papers")  
        # Kartik's code goes here