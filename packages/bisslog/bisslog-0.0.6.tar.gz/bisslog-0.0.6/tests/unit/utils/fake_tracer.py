from bisslog.ports.tracing.tracer import Tracer


class FakeTracer(Tracer):

    def __init__(self):
        self._calls = {"info": [], "error": [], "warning": []}

    def error(self, *args, **kwargs):
        self._calls["error"].append((args, kwargs))

    def info(self, *args, **kwargs):
        self._calls["info"].append((args, kwargs))

    def warning(self, *args, **kwargs):
        self._calls["warning"].append((args, kwargs))

    def debug(self, *args, **kwargs):
        self._calls["debug"].append((args, kwargs))

    def critical(self, *args, **kwargs):
        self._calls["critical"].append((args, kwargs))
