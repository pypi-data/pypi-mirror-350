"""Module providing the DomainContext class."""
from typing import Optional

from .adapters.tracing.opener_tracer_logging import OpenerTracerLogging
from .adapters.tracing.service_tracer_logging import ServiceTracerLogging
from .adapters.tracing.transactional_tracer_logging import TransactionalTracerLogging
from .ports.tracing.opener_tracer import OpenerTracer
from .ports.tracing.service_tracer import ServiceTracer
from .ports.tracing.transactional_tracer import TransactionalTracer
from .utils.singleton import SingletonReplaceAttrsMeta


class DomainContext(metaclass=SingletonReplaceAttrsMeta):
    """Singleton class managing tracing components within an application.

    This class provides a centralized way to initialize and manage different
    tracers used for logging and monitoring purposes."""

    def __init__(self, appname: Optional[str] = None, runtime_ecosystem: Optional[str] = None):
        """Initializes the DomainContext instance.

        Parameters
        ----------
        appname : Optional[str], optional
            The name of the application using the context, by default None.
        runtime_ecosystem : Optional[str], optional
            The runtime environment of the application (e.g., "script", "server"), by default None.
        """
        self.appname = appname
        self.runtime_ecosystem = runtime_ecosystem
        self.tracer: Optional[TransactionalTracer] = None
        self.opener: Optional[OpenerTracer] = None
        self.service_tracer: Optional[ServiceTracer] = None

    def init_default(self):
        """Initializes the default tracing components.

        This method sets up default instances of `OpenerTracerLogging`,
        `ServiceTracerLogging`, and `TransactionalTracerLogging`.
        It also assigns the runtime ecosystem to "script".
        """
        self.opener = OpenerTracerLogging()
        self.service_tracer = ServiceTracerLogging()
        self.runtime_ecosystem = "script"
        self.tracer = TransactionalTracerLogging()


domain_context = DomainContext()
domain_context.init_default()
