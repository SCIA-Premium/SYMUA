"""Extends crowddynamics commandline client with gui related commands"""
import logging
import sys

import click
from PySide6 import QtCore, QtWidgets
from crowddynamics.logging import setup_logging

from main import MainWindow


def run_gui(simulation_cfg=None):
    r"""Launches the graphical user interface for visualizing simulation."""
    setup_logging()

    logger = logging.getLogger(__name__)
    logger.info('Starting GUI')
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    logger.info('Simulation file: %s', simulation_cfg)
    if simulation_cfg:
        win.set_simulations(simulation_cfg)
    win.show()

    # Start Qt event loop unless running in interactive mode or using pyside.
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app.exec()
    else:
        logger.warning("Interactive mode and pyside are not supported.")

    logging.info('Exiting GUI')
    logging.shutdown()

    win.close()
    app.exit()
    sys.exit()


@click.group()
def main():
    pass


@main.command()
@click.option('--simulation_file', type=str, default=None)
def run(simulation_file):
    """Launch gui for crowddynamics"""
    run_gui(simulation_file)


if __name__ == "__main__":
    main()
