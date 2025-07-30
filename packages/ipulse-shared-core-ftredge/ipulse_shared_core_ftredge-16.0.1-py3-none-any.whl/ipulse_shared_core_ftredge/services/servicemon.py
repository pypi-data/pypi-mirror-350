"""
ServiceMon - Lightweight monitoring for service functions and API endpoints
"""
import uuid
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from contextlib import contextmanager
from ipulse_shared_base_ftredge import (LogLevel, AbstractResource,
                                      ProgressStatus, Action, Resource,
                                      Alert, StructLog)

class Servicemon:
    """
    ServiceMon is a lightweight version of Pipelinemon designed specifically for monitoring
    service functions like Cloud Functions and API endpoints.

    It provides:
    1. Structured logging with context tracking
    2. Performance metrics capture
    3. Service health monitoring
    4. Integration with FastAPI request/response cycle
    """

    def __init__(self, logger,
                 base_context: str,
                 service_name: str):
        """
        Initialize ServiceMon with basic configuration.

        Args:
            logger: The logger instance to use for logging
            base_context: Base context information for all logs
            service_name: Name of the service being monitored
        """
        # Set up execution tracking details
        self._start_time = None
        self._service_name = service_name

        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        uuid_suffix = str(uuid.uuid4())[:8]  # Take first 8 chars of UUID
        self._id = f"{timestamp}_{uuid_suffix}"

        # Set up context handling
        self._base_context = base_context
        self._context_stack = []

        # Configure logging
        self._logger = logger

        # Metrics tracking
        self._metrics = {
            "status": ProgressStatus.NOT_STARTED.name,
            "errors": 0,
            "warnings": 0,
            "start_time": None,
            "end_time": None,
            "duration_ms": None,
        }

    @property
    def id(self) -> str:
        """Get the unique ID for this service execution."""
        return self._id

    @property
    def base_context(self) -> str:
        """Get the base context for this service execution."""
        return self._base_context

    @property
    def service_name(self) -> str:
        """Get the service name being monitored."""
        return self._service_name

    @property
    def metrics(self) -> Dict[str, Any]:
        """Get the current service metrics."""
        return self._metrics.copy()

    @property
    def current_context(self) -> str:
        """Get the current context stack as a string."""
        return " >> ".join(self._context_stack) if self._context_stack else "root"

    @contextmanager
    def context(self, context_name: str):
        """
        Context manager for tracking execution context.

        Args:
            context_name: The name of the current execution context
        """
        self.push_context(context_name)
        try:
            yield
        finally:
            self.pop_context()

    def push_context(self, context: str):
        """Add a context level to the stack."""
        self._context_stack.append(context)

    def pop_context(self):
        """Remove the most recent context from the stack."""
        if self._context_stack:
            return self._context_stack.pop()

    def start(self, description: Optional[str] = None) -> None:
        """
        Start monitoring a service execution.

        Args:
            description: Optional description of what's being executed
        """
        self._start_time = time.time()
        self._metrics["start_time"] = datetime.now(timezone.utc).isoformat()
        self._metrics["status"] = ProgressStatus.IN_PROGRESS.name

        # Log the start event
        msg = description if description else f"Starting {self.service_name}"
        self.log(level=LogLevel.INFO, description=msg, resource=AbstractResource.SERVICEMON, action=Action.EXECUTE,
                 progress_status=ProgressStatus.IN_PROGRESS)

    def end(self, status: ProgressStatus = ProgressStatus.DONE) -> Dict[str, Any]:
        """
        End monitoring and record final metrics.

        Args:
            status: The final status of the service execution

        Returns:
            Dict containing metrics summary
        """
        # Calculate duration
        end_time = time.time()
        if self._start_time:
            duration_ms = int((end_time - self._start_time) * 1000)
            self._metrics["duration_ms"] = duration_ms

        # Update metrics
        self._metrics["end_time"] = datetime.now(timezone.utc).isoformat()
        self._metrics["status"] = status.name

        # Determine log level based on metrics
        if self._metrics["errors"] > 0:
            level = LogLevel.ERROR
            if status == ProgressStatus.DONE:
                status = ProgressStatus.FINISHED_WITH_ISSUES
        elif self._metrics["warnings"] > 0:
            level = LogLevel.WARNING
            if status == ProgressStatus.DONE:
                status = ProgressStatus.DONE_WITH_WARNINGS
        else:
            level = LogLevel.INFO

        # Prepare summary message
        summary_msg = (
            f"Service {self.service_name} completed with status {status.name}. "
            f"Duration: {self._metrics['duration_ms']}ms. "
            f"Errors: {self._metrics['errors']}, Warnings: {self._metrics['warnings']}"
        )

        # Log the completion
        self.log(
            level=level,
            description=summary_msg,
            resource=AbstractResource.SERVICEMON,
            action=Action.EXECUTE,
            progress_status=status,
        )

        return self._metrics

    def log(self,
           level: LogLevel,
           description: str,
           resource: Optional[Resource] = None,
           source: Optional[str] = None,
           destination: Optional[str] = None,
           action: Optional[Action] = None,
           progress_status: Optional[ProgressStatus] = None,
           alert: Optional[Alert] = None,
           e: Optional[Exception] = None,
           systems_impacted: Optional[str] = None,
           notes: Optional[str] = None,
           **kwargs) -> None:
        """
        Log a message with structured context.

        Args:
            level: Log level
            description: Log message
            resource: Resource being accessed
            action: Action being performed
            progress_status: Current progress status
            alert: Alert type if applicable
            e: Exception if logging an error
            **kwargs: Additional fields to include in the log
        """
        # Update metrics
        if level in (LogLevel.ERROR, LogLevel.CRITICAL):
            self._metrics["errors"] += 1
        elif level == LogLevel.WARNING:
            self._metrics["warnings"] += 1


        formatted_notes = f"{notes} ;elapsed_ms: {int((time.time() - self._start_time) * 1000)} " + str(kwargs)
        # Create structured log
        log = StructLog(
            level=level,
            resource=resource,
            action=action,
            progress_status=progress_status,
            alert=alert,
            e=e,
            source=source,
            destination=destination,
            description=description,
            collector_id=self.id,
            base_context=self.base_context,
            context=self.current_context,
            systems_impacted=systems_impacted,
            note=formatted_notes,
            **kwargs
        )

        # Add service-specific fields
        log_dict = log.to_dict()

        # Write to logger
        if level.value >= LogLevel.ERROR.value:
            self._logger.error(log_dict)
        elif level.value >= LogLevel.WARNING.value:
            self._logger.warning(log_dict)
        elif level.value >= LogLevel.INFO.value:
            self._logger.info(log_dict)
        else:
            self._logger.debug(log_dict)

