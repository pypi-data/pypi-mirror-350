from .database import DatabaseManager
from .analytics import AnalyticsManager
from .embeddings import EmbeddingManager
from .prompts import PromptManager
# from .url_handler import URLHandler
from .config import get_credentials
from .logging_config import IgnoreTorchWarning, configure_logging

# Configure logging when the package is imported
configure_logging()

__all__ = [
    'DatabaseManager',
    'AnalyticsManager',
    'EmbeddingManager',
    'PromptManager',
    # 'URLHandler',
    'get_credentials',
    'IgnoreTorchWarning',
    'configure_logging'
]