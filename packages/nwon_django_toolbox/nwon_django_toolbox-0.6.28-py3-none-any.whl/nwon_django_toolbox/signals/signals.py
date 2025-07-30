from typing import List

from django.db.models.signals import ModelSignal

from nwon_django_toolbox.signals.disable_signals import DisableSignals

DISABLE_SIGNALS = DisableSignals([])


def disable_signals(signals: List[ModelSignal]):
    for signal in signals:
        DISABLE_SIGNALS.disconnect(signal)


def enable_signals(signals: List[ModelSignal]):
    for signal in signals:
        DISABLE_SIGNALS.reconnect(signal)
