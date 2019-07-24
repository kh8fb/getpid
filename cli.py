"""
GetPid's command line interface
"""

import click_completion
from . import cli_main

import .getpid

if __name__ == "__main__":
    click_completion.init()
    
