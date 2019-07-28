import ast
import telnetlib
import time
import pandas as pd


host_ip = '127.0.0.1'
tn = telnetlib.Telnet()
tn.open(host_ip, port=81)
results = []
for i in range(1, 5000):
    tn.write(str(i).encode("ascii"))
    time.sleep(0.1)
    row = tn.read_very_eager().decode('ascii')
    row = ast.literal_eval(row)
    user_sample = [i]
    for _ in row:
        user_sample.append(_[0])
    results.append(user_sample)
results = pd.DataFrame(results)
results.to_csv("user_recomm.csv", header=None, index=False)
results = pd.read_csv("user_recomm.csv", header=None)
print(results)
