import logging
import os
from logging.handlers import RotatingFileHandler
import sys
import traceback

# Create a filter to ignore specific messages
class IgnoreTorchWarning(logging.Filter):
    def filter(self, record):
        return not (
            "Examining the path of torch.classes" in record.getMessage() or
            "torch::class_" in record.getMessage()
        )

# Configure logging
def configure_logging():
    # Check if logging is already configured to avoid duplicate handlers
    if logging.getLogger().handlers:
        return
        
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
    
    # Set up exception logging
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            # Don't log keyboard interrupt
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
            
        logging.error("Uncaught exception", 
                     exc_info=(exc_type, exc_value, exc_traceback))
    
    # Set the exception hook
    sys.excepthook = handle_exception