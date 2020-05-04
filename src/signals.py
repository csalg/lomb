from blinker import Namespace

signals = Namespace()

exposure_was_received = signals.signal('exposure_was_received')
