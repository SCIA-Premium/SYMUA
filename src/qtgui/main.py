"""Main window for crowddynamics graphical user interface.

Graphical user interface and simulation graphics for crowddynamics implemented
using PyQt and pyqtgraph. Layout for the main window is created by using Qt
designer. [Hess2013]_, [Sepulveda2014]_

Design of the gui was inspired by the design of RtGraph [campagnola2012]_
"""
import logging
from typing import Optional
from collections import OrderedDict, namedtuple
from multiprocessing import Queue

import numpy as np
import pyqtgraph as pg
from PySide6 import QtGui, QtCore, QtWidgets
from copy import deepcopy
from crowddynamics.simulation.multiagent import MultiAgentProcess, LogicNode, MultiAgentSimulation
from crowddynamics.traits import class_own_traits
from crowddynamics.utils import import_subclasses
from loggingtools import log_with
from traitlets.traitlets import Instance

from graphics import MultiAgentPlot
from traits import trait_to_QWidget
from ui.gui import Ui_MainWindow

logger = logging.getLogger(__name__)

Message = namedtuple("Message", "agents data")


class GuiCommunication(LogicNode):
    """Communication between the GUI and simulation."""

    queue = Instance(klass=type(Queue()), allow_none=True)

    def update(self, *args, **kwargs):
        self.queue.put(Message(agents=np.copy(self.simulation.agents.array), data=self.simulation.data))


@log_with()
def clear_queue(queue):
    """Clear all items from a queue"""
    while not queue.empty():
        queue.get()


@log_with()
def clear_widgets(layout):
    """Clear widgets from a layout

    Args:
        layout:

    References
        - http://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt
    """
    for i in reversed(range(layout.count())):
        if i in (0, 1):
            continue
        layout.itemAt(i).widget().setParent(None)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    r"""MainWindow

    Main window for the grahical user interface. Layout is created by using
    qtdesigner and the files can be found in the *designer* folder. Makefile
    to generate python code from the designer files can be used with command::

       make gui

    Main window consists of

    - Menubar (top)
    - Sidebar (left)
    - Graphics layout widget (middle)
    - Control bar (bottom)
    """
    logger = logging.getLogger(__name__)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Simulation with multiprocessing
        self.configs = OrderedDict()
        self.simulation = None
        self.simulation_cls = None
        self.simulation_kwargs = {}
        self.process = None
        self.queue = Queue(maxsize=4)

        # Graphics widget for plotting simulation data.
        pg.setConfigOptions(antialias=True)
        self.timer = QtCore.QTimer(self)
        self.plot = MultiAgentPlot()
        self.graphicsLayout.setBackground(None)
        self.graphicsLayout.addItem(self.plot, 0, 0)

        # self.plot_data = DataPlot()
        # self.graphicsLayout.addItem(self.plot_data, 0, 1)

        # Buttons
        self.initButton = QtWidgets.QPushButton("Initialize Simulation")

        # Sets the functionality and values for the widgets.
        self.enable_controls(False)  # Disable until simulation is set
        self.timer.timeout.connect(self.update_plots)
        self.startButton.clicked.connect(self.start)
        self.stopButton.clicked.connect(self.stop)
        self.initButton.clicked.connect(self.set_simulation)
        self.simulationsBox.currentIndexChanged.connect(self.set_sidebar)
        self.actionOpen.triggered.connect(self.load_simulation_cfg)

    def enable_controls(self, boolean):
        """Enable controls

        Args:
            boolean (bool):
        """
        self.startButton.setEnabled(boolean)
        self.stopButton.setEnabled(boolean)
        self.saveButton.setEnabled(boolean)

    def reset_buffers(self):
        r"""Reset buffers"""
        clear_queue(self.queue)

    @log_with(qualname=True, ignore=("self",))
    def set_simulations(self, module_path):
        self.configs.update(import_subclasses(module_path, MultiAgentSimulation))
        self.simulationsBox.addItems(list(self.configs.keys()))

    @log_with(qualname=True, ignore=("self",))
    def load_simulation_cfg(self):
        """Load simulation configurations"""
        self.simulationsBox.clear()
        module_path = QtWidgets.QFileDialog().getOpenFileName(self, "Open file", "", "Python file (*.py)")
        self.set_simulations(module_path)

    @log_with(qualname=True, ignore=("self",))
    def set_sidebar(self, simuname):
        """Set sidebar

        Args:
            simuname (str):
        """
        self.reset_buffers()

        # Clear sidebar first
        clear_widgets(self.sidebarLeft)

        # Get the simulation

        simulation_cls = deepcopy(list(self.configs.values())[simuname])
        simulation_kwargs = {name: trait.default_value for name, trait in class_own_traits(simulation_cls)}

        def gen_callback(name):
            @log_with()
            def callback(value):
                simulation_kwargs[name] = value

            return callback

        for name, trait in class_own_traits(simulation_cls):
            label, widget = trait_to_QWidget(name, trait, gen_callback(name))
            self.sidebarLeft.addWidget(label)
            self.sidebarLeft.addWidget(widget)

        self.simulation_cls = simulation_cls
        self.simulation_kwargs = simulation_kwargs
        self.sidebarLeft.addWidget(self.initButton)

    def set_simulation(self):
        simulation = self.simulation_cls(**self.simulation_kwargs)

        communication = GuiCommunication(simulation)
        communication.queue = self.queue

        node = simulation.logic["Reset"]
        node.inject_after(communication)

        bg_image: Optional[np.ndarray] = None
        if hasattr(simulation, "bg_image_data"):
            bg_image = simulation.bg_image_data

        self.plot.configure(
            simulation.field.domain,
            simulation.field.obstacles,
            simulation.field.targets,
            simulation.agents.array,
            bg_image,
        )

        # Last enable controls
        self.simulation = simulation
        self.enable_controls(True)

    def stop_plotting(self):
        self.timer.stop()
        self.enable_controls(True)
        self.process = None

    def update_plots(self):
        r"""Update plots. Consumes data from the queue."""
        message = self.queue.get()
        if message is not MultiAgentProcess.EndProcess:
            try:
                self.plot.update_data(message)
                # self.plot_data.update_data(message)
            except Exception as error:
                self.logger.error("Plotting stopped to error: {}".format(error))
                self.stop_plotting()
        else:
            self.stop_plotting()

    def start(self):
        """Start simulation process and updating plot."""
        if self.simulation:
            # Wrap the simulation into a process class here because we can
            # only use processes once.
            self.startButton.setEnabled(False)
            self.process = MultiAgentProcess(self.simulation, self.queue)
            self.process.start()
            self.timer.start(1)
        else:
            self.logger.info("Simulation is not set.")

    def stop(self):
        """Stops simulation process and updating the plot"""
        if self.process:
            self.process.stop()
        else:
            self.logger.info("There are no processes running.")
