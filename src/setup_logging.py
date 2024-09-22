"""
Module for setting up logging config
"""
import sys
import logging
import logging.config
import yaml


def setup_logging(path_to_config: str = "../logging_config.yaml"):
    """
    Setups the logging config
    :param path_to_config: path to yaml file with logging config
    :return: nothing
    """
    with open(path_to_config, encoding="utf-8") as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)

        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding='utf-8')
