import logging
import os
from logging.handlers import RotatingFileHandler
import sys

# Create a filter to ignore specific messages
class IgnoreTorchWarning(logging.Filter):
    def filter(self, record):
        return not (
            "Examining the path of torch.classes" in record.getMessage() or
            "torch::class_" in record.getMessage()
        )

# Configure logging
def configure_logging():
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(IgnoreTorchWarning())
    
    # Create file handler for production environments
    try:
        log_dir = os.path.join(os.path.expanduser("~"), ".startgarlic", "logs")
        os.makedirs(log_dir, exist_ok=True)
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, "startgarlic.log"),
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        file_handler.addFilter(IgnoreTorchWarning())
        root_logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not set up file logging: {e}")
    
    # Add console handler
    root_logger.addHandler(console_handler)