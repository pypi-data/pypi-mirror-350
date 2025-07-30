import logging
import sys

def configure_root_logger():
    logging.basicConfig(
        level=logging.DEBUG,  # 最重要：级别低于你要输出的日志级别
        stream=sys.stdout,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    """
    Configure the root logger to display all log messages on the console
    """
    # Get the root logger
    root_logger = logging.getLogger("openai.agents")
    root_logger.setLevel(logging.DEBUG)

    root_logger.propagate = True
    # logger = logging.getLogger("openai.agents")
    # logger.propagate = True

    # Remove existing handlers to avoid duplicate logs
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    class PrintHandler(logging.Handler):
        def emit(self, record):
            log_entry = self.format(record)
            print(log_entry)
    # Create a console handler
    console_handler = PrintHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    console_handler.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)

    logging.info("Root logger configured, logs will be displayed on the console")