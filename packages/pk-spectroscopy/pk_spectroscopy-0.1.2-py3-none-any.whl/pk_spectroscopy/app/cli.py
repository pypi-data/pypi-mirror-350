"""
App entry point
"""
import sys
from importlib import import_module
from streamlit.web import cli as stcli

def main() -> None:

    mod = import_module('pk_spectroscopy.app.app')
    sys.argv = ['streamlit', 'run', mod.__file__, '--server.headless', 'false']
    stcli.main()