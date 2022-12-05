from PySide6 import QtCore, QtGui, QtWidgets
from ui.main_ui import Ui_MainWindow
import pyqtgraph as pg

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Simulation with multiprocessing
        self.simulation = None
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
        self.initButton = QtGui.QPushButton("Initialize Simulation")

        # Sets the functionality and values for the widgets.
        self.enable_controls(False)  # Disable until simulation is set
        self.timer.timeout.connect(self.update_plots)
        self.startButton.clicked.connect(self.start)
        self.stopButton.clicked.connect(self.stop)
        self.initButton.clicked.connect(self.set_simulation)
        self.simulationsBox.currentIndexChanged[str].connect(self.set_sidebar)
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

    @log_with(qualname=True, ignore=('self',))
    def set_simulations(self, module_path):
        self.configs.update(
            import_subclasses(module_path, MultiAgentSimulation))
        self.simulationsBox.addItems(list(self.configs.keys()))

    @log_with(qualname=True, ignore=('self',))
    def load_simulation_cfg(self):
        """Load simulation configurations"""
        self.simulationsBox.clear()
        module_path = QtGui.QFileDialog().getOpenFileName(
            self, 'Open file', '', 'Python file (*.py)')
        self.set_simulations(module_path)

    @log_with(qualname=True, ignore=('self',))
    def set_sidebar(self, simuname):
        """Set sidebar
        Args:
            simuname (str):
        """
        self.reset_buffers()

        # Clear sidebar first
        clear_widgets(self.sidebarLeft)

        # Get the simulation
        simulation_cls = deepcopy(self.configs[simuname])
        simulation_kwargs = {name: trait.default_value for name, trait in
                             class_own_traits(simulation_cls)}

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

        node = simulation.logic['Reset']
        node.inject_after(communication)

        self.plot.configure(
            simulation.field.domain,
            simulation.field.obstacles,
            simulation.field.targets,
            simulation.agents.array
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
            except CrowdDynamicsGUIException as error:
                self.logger.error('Plotting stopped to error: {}'.format(
                    error
                ))
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