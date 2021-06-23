import logging


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelno)s"
                        + " | %(module)s:%(lineno)d - %(message)s")

Logger = logging
