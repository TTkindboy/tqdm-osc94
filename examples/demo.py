import time
from tqdm_osc94 import tqdm_osc94
from tqdm import tqdm

for i in tqdm_osc94(range(2000), mininterval=0.1):
    time.sleep(0.001)

print("all done!")