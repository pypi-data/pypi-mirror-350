"""Top-level package for frogml."""

__author__ = "jfrog"
__version__ = "0.0.87"

from frogml_core.inner.di_configuration import wire_dependencies
from frogml_core.model.model_version_tracking import (  # noqa: F401,E501
    log_metric,
    log_param,
)
from frogml_core.model_loggers.artifact_logger import (  # noqa: F401,E501
    load_file,
    log_file,
)
from frogml_core.model_loggers.data_logger import load_data, log_data  # noqa: F401
from frogml_core.model_loggers.model_logger import (  # noqa: F401,E501
    load_model,
    log_model,
)

from .frogml_client.client import FrogMLClient  # noqa: F401
from .model.decorators.api import api_decorator as api  # noqa: F401
from .model.decorators.timer import frogml_timer  # noqa: F401

_container = wire_dependencies()
