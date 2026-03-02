import io
import re

from tqdm_osc94.progress import ESC, ST, OSC94State, tqdm_osc94
from tqdm import tqdm


def msg(state: OSC94State, progress: int | None) -> str:
    if progress is None:
        return f"{ESC}9;4;{state.value}{ST}"
    return f"{ESC}9;4;{state.value};{progress}{ST}"


def normalize_timing_fields(output: str) -> str:
    # Strip only volatile tqdm timing/rate fragments, keep everything else intact.
    output = re.sub(r"\d+:\d+<\d+:\d+", "<TIME>", output)
    output = re.sub(r"\d+(?:\.\d+)?it/s", "<RATE>", output)
    return re.sub(r"[ \t]+(\r?\n|$)", r"\1", output) # normalize trailing whitespace


def test_percent_and_clear() -> None:
    buf = io.StringIO()

    with tqdm_osc94(total=100, file=buf, show_bar=False) as t:
        t.update(50)
        t.display()

    out = buf.getvalue()
    assert msg(OSC94State.NORMAL, 50) in out
    assert out.rstrip("\r\n").endswith(msg(OSC94State.CLEAR, None))


def test_indeterminate() -> None:
    buf = io.StringIO()

    with tqdm_osc94(total=None, file=buf, show_bar=False) as t:
        t.display()

    assert msg(OSC94State.INDETERMINATE, None) in buf.getvalue()


def test_osc94_false_writes_as_tqdm() -> None: # test with tqdm
    buf_no_osc94 = io.StringIO()
    buf_tqdm = io.StringIO()

    with tqdm_osc94(total=100, file=buf_no_osc94, osc94=False) as t:
        t.update(50)
        t.display()

    with tqdm(total=100, file=buf_tqdm) as t:
        t.update(50)
        t.refresh()

    assert normalize_timing_fields(buf_no_osc94.getvalue()) == normalize_timing_fields(buf_tqdm.getvalue())

def test_disable_true_writes_nothing() -> None:
    buf = io.StringIO()

    with tqdm_osc94(total=100, file=buf, disable=True) as t:
        t.update(50)
        t.refresh()

    assert buf.getvalue() == ""


def test_percent_clamped_to_100() -> None:
    buf = io.StringIO()

    with tqdm_osc94(total=10, file=buf, show_bar=False) as t:
        t.update(999)
        t.refresh()

    assert msg(OSC94State.NORMAL, 100) in buf.getvalue()
