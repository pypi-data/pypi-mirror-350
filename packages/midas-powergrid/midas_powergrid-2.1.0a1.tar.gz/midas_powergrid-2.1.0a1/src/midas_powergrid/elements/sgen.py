import logging

from .storage import PPStorage

LOG = logging.getLogger(__name__)


class PPSgen(PPStorage):
    def __init__(self, index, grid, value=0.02):
        super().__init__(index, grid, value, "sgen")
