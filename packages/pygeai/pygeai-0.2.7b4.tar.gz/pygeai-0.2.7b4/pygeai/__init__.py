import logging

__author__ = 'Globant'
__version__ = '0.2.7'


# Recommended handler for libraries.
# Reference: https://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
logger = logging.getLogger('geai')
logger.addHandler(logging.NullHandler())
