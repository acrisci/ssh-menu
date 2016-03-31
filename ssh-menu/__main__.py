from .config import Config
from . import widget
from argparse import ArgumentParser

parser = ArgumentParser()

args = parser.parse_args()

config = Config()

widget.start()
