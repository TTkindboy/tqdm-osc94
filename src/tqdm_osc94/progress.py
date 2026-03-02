from typing import override
from enum import IntEnum
from tqdm import tqdm


ESC = "\x1b]"
ST = "\x1b\\"


class OSC94State(IntEnum):
    """OSC 9;4 progress indicator states for Windows Terminal."""

    CLEAR = 0  # No progress indicator / clear
    NORMAL = 1  # Normal progress (requires percentage)
    ERROR = 2  # Error state
    INDETERMINATE = 3  # Indeterminate progress (cannot be set with percentage)
    PAUSED = 4  # Paused/Warning state


class tqdm_osc94(tqdm):
    """tqdm subclass that can send OSC 9;4 progress updates to the terminal."""

    @override
    def __init__(self, *args, osc94: bool = True, show_bar: bool = True, **kwargs):
        self.osc94 = osc94
        self.show_bar = show_bar
        super().__init__(*args, **kwargs)

    def _osc94_write(self, state: OSC94State, progress: int | None):
        if progress is None:
            msg = f"{ESC}9;4;{state.value}{ST}"
        else:
            msg = f"{ESC}9;4;{state.value};{progress}{ST}"

        try:
            self.fp.write(msg)
            self.fp.flush()
        except Exception:
            pass

    def _osc94_update(self):
        if not self.osc94 or self.disable:
            return

        if self.total:
            pct = int(min(100, max(0, self.n / self.total * 100)))
            self._osc94_write(OSC94State.NORMAL, pct)
        else:
            self._osc94_write(OSC94State.INDETERMINATE, None)

    @override
    def display(self, *args, **kwargs):
        self._osc94_update()
        if self.show_bar:
            super().display(*args, **kwargs)

    @override
    def close(self):
        if self.disable:
            return
        if self.osc94:
            self._osc94_write(OSC94State.CLEAR, None)
        super().close()
