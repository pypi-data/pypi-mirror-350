from collections import defaultdict
from typing import List, Union

from django.db.models.signals import (
    ModelSignal,
    post_delete,
    post_init,
    post_migrate,
    post_save,
    pre_delete,
    pre_init,
    pre_migrate,
    pre_save,
)
from django.dispatch import Signal


class DisableSignals:
    """
    Class for managing the disabling of signals.
    """

    disabled_signals: List[Union[ModelSignal, Signal]]

    def __init__(self, disabled_signals: List[Union[ModelSignal, Signal]]):
        self.stashed_signals = defaultdict(list)
        self.disabled_signals = disabled_signals or [
            pre_init,
            post_init,
            pre_save,
            post_save,
            pre_delete,
            post_delete,
            pre_migrate,
            post_migrate,
        ]

    def __enter__(self):
        for signal in self.disabled_signals:
            self.disconnect(signal)

    def __exit__(self, exc_type, exc_val, exc_tb):
        for signal in list(self.stashed_signals):
            self.reconnect(signal)

    def disconnect(self, signal: Union[ModelSignal, Signal]):
        self.stashed_signals[signal] = signal.receivers
        signal.receivers = []

    def reconnect(self, signal: Union[ModelSignal, Signal]):
        signal.receivers = self.stashed_signals.get(signal, [])

        if signal in self.stashed_signals:
            del self.stashed_signals[signal]
