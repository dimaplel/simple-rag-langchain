import sys
import logging
import logging.config
import yaml


def setup_logging(path_to_config: str = "../logging_config.yaml"):
    with open(path_to_config) as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)

        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding='utf-8')
