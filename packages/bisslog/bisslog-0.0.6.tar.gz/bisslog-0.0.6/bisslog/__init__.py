"""Bisslog - Hexagonal Architecture Library for Python

This library provides a lightweight and dependency-free implementation of
Hexagonal Architecture (Ports and Adapters) in Python. It enforces a strict
separation between domain logic, application, and infrastructure,
allowing easy integration with different frameworks and external services
without modifying core business logic.

Key Features:
- **UseCase**: Encapsulates domain logic, independent of infrastructure.
- **Ports**: Define clear interfaces for external dependencies such as:
  - Database
  - Messaging (Publisher)
  - File Upload
  - Tracing (Logs & Spans)
  - Email & SMS sending
  - Entry Points (to integrate with FastAPI, Flask, AWS Lambda, etc.)
  - External API integrations
  - Notifications (WebSockets, Push, Webhooks)
  - Background Jobs
  - Feature Flags
- **Adapters**: Implement ports to connect with specific technologies.

This library ensures that the domain remains pure and testable while providing
the flexibility to replace infrastructure components without affecting business logic."""
from .adapters.division import Division
from .adapt_handler.adapt_handler import AdaptHandler
from .adapt_handler.file_uploader_handler import bisslog_upload_file, UploadFileHandler
from .adapt_handler.notifier_handler import bisslog_notifier, NotifierHandler
from .adapt_handler.publisher_handler import bisslog_pubsub, PublisherHandler
from .database.bisslog_db import bisslog_db, BissLogDB
from .domain_context import DomainContext, domain_context
from .transactional.transaction_manager import transaction_manager
from .use_cases.use_case_base import UseCaseBase
from .use_cases.use_case_basic import BasicUseCase
from .use_cases.use_case_full import FullUseCase
from .use_cases.use_case_decorator import use_case

__all__ = [
    "BasicUseCase", "FullUseCase", "UseCaseBase", "use_case",
    "AdaptHandler",
    "bisslog_db", "BissLogDB", "Division",
    "NotifierHandler", "bisslog_notifier",
    "bisslog_pubsub", "PublisherHandler", "bisslog_upload_file", "UploadFileHandler",
    "transaction_manager",
    "domain_context", "DomainContext"
]
