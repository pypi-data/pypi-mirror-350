import logging

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
    
    # Add our custom filter to all handlers
    for handler in root_logger.handlers:
        handler.addFilter(IgnoreTorchWarning()) 