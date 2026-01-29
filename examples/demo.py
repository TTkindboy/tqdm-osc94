import time
from tqdm_osc94 import tqdm_osc94

for i in tqdm_osc94(range(5000), show_bar=False):
    time.sleep(0.001)

