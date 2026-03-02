import time
from tqdm_osc94 import tqdm_osc94
from tqdm import tqdm

MS_DELAY = 20

out: list[tuple[int, bool | None]] = []
with tqdm_osc94(total=100, show_bar=False) as t:
    for i in range(100):
        time.sleep(MS_DELAY / 1000)
        out.append((i, t.update()))

# print successes
for i, result in filter(lambda x: x[1] is True, out):
    print(f"Update {i} succeeded")

print(f"{sum(1 for _, result in out if result is True)}/100 succeeded")