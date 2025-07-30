from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QWheelEvent, QShowEvent
from PySide6.QtWidgets import (QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, QScrollArea, QSizePolicy,
                               QGraphicsView, QWidget, QListWidget, QAbstractItemView)

from ._components.analog_trace import AnalogTrace
from ._components.callbacks import GuiCallbacks
from ._components.funcs import GuiFuncs
from ._components.maxprojection import MaximumProjection


class ManualCurationUI(GuiFuncs, GuiCallbacks, QDialog):

    def __init__(self, cell_names, cell_traces, cell_contours, maxproj_path):

        super().__init__()
        self.default_font = QFont("Arial", 12)
        self.cells = cell_names
        self.cell_traces = cell_traces
        self.cell_contours = cell_contours
        self.maxproj_path = maxproj_path

        #  Cell Selection List Components
        self.cell_scroll_area = None
        self.cell_list = None
        self.select_all_button = None
        self.select_none_button = None
        self.export_cells_button = None
        self.cell_selection_checkbox_list = []
        self.cell_view_checkbox_list = []
        # Cell View List Components
        self.cell_view_list = None
        self.cell_view_scroll_area = None
        self.view_all_button = None
        self.view_none_button = None
        self.transfer_view_button = None
        # Cell Trace List Components
        self.cell_trace_scroll_area_contents = None
        self.cell_trace_scroll_area = None
        self.trace_pointers = []
        self.trace_pointers_dict = {}
        #  Layouts
        self.main_layout = None
        self.top_half_container = None
        self.bottom_half_layout = None
        self.cell_list_layout = None
        self.cell_list_control_layout = None
        self.cell_select_checkbox_layout = None
        self.max_projection_layout = None
        self.max_projection_controls = None
        self.cell_view_checkbox_layout = None
        self.bottom_half_container = None
        self.cell_trace_box_layout = None
        self.cell_trace_contents_layout = None
        self.cell_view_layout = None
        self.cell_view_controls_layout = None
        self.cell_list_control_selection_layout = None
        #  Group Boxes
        self.cell_list_box = None
        self.max_projection_box = None
        self.cell_trace_box = None
        #  Max Projection Controls
        self.scale = 1
        self.scale_factor = 0.01
        self.direction = 0
        self.zoom_in = None
        self.zoom_out = None
        self.zoom_reset = None
        #  Image View Components
        self.max_projection_view = None
        self.max_projection = None
        self.value = []

        self.curated_cells = []

        self._init_window_params()
        self.initUI()
        if self.maxproj_path is not None:
            self._configure_maxproj_view()
        self._populate_cell_traces()
        self._get_trace_pointers()

    #  Function Overloads
    def eventFilter(self, obj, event):
        if type(event) is QWheelEvent:
            if type(obj) is AnalogTrace:
                self.cell_trace_scroll_area.wheelEvent(event)
                return True
            elif obj is self.max_projection_view.viewport():
                if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                    num_degrees = event.angleDelta() / 8
                    steps = int(num_degrees.y() / 15)
                    self._zoom_image(steps)
                    return True
        elif type(event) is QShowEvent and self.max_projection_view is not None and obj is self.max_projection_view.viewport():
            self.max_projection_view.fitInView(self.max_projection.itemsBoundingRect(), Qt.KeepAspectRatio)
            # We don't actually wanna handle this event, just needed to run this with it

        return False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            self.reset_image_zoom()
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_Equal:
                self.zoom_image_in()
            elif event.key() == Qt.Key.Key_Minus:
                self.zoom_image_out()

    def resizeEvent(self, event):
        event.accept()
        if self.scale == 1:
            if self.max_projection_view is not None:
                self.max_projection_view.fitInView(self.max_projection.itemsBoundingRect(), Qt.KeepAspectRatio)
                self.scale = 1

    def initUI(self):

        # ==MAIN LAYOUT== #
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # ==TOP HALF== #
        self.top_half_container = QHBoxLayout()  # Holds the cell list and max projection
        # ==Cell Selection List== #
        self.cell_list_box = QGroupBox("Cells")
        self.cell_list_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.cell_list_box.setMaximumWidth(250)
        self.cell_list_layout = QVBoxLayout()
        self.cell_list_box.setLayout(self.cell_list_layout)

        self.cell_list = QWidget()
        self.cell_select_checkbox_layout = QVBoxLayout(self.cell_list)
        self._populate_selection_list()

        self.cell_scroll_area = QScrollArea()  # Add the scroll area to the layout
        self.cell_scroll_area.setWidget(self.cell_list)
        self.cell_list_layout.addWidget(self.cell_scroll_area)

        # ==Cell Selection List Controls== #
        self.cell_list_control_layout = QVBoxLayout()
        self.cell_list_control_selection_layout = QHBoxLayout()  # Add the two buttons to a layout
        self.select_all_button = QPushButton(u"Select All")
        self.select_all_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.select_all_button.clicked.connect(self.select_all)
        self.select_none_button = QPushButton(u"Select None")
        self.select_none_button.clicked.connect(self.select_none)
        self.select_none_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.export_cells_button = QPushButton(u"Export Cells")
        self.export_cells_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.export_cells_button.clicked.connect(self.export_cells)
        self.cell_list_control_selection_layout.addWidget(self.select_all_button)
        self.cell_list_control_selection_layout.addWidget(self.select_none_button)
        self.cell_list_control_layout.addLayout(self.cell_list_control_selection_layout)
        self.cell_list_control_layout.addWidget(self.export_cells_button)
        self.cell_list_layout.addLayout(self.cell_list_control_layout)

        self.top_half_container.addWidget(self.cell_list_box)  # Cell list to top half



        # ==Max Projection Display== #
        self.max_projection_box = QGroupBox("Max Projection")  # Create the max projection box
        self.max_projection_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.max_projection_box.setMinimumSize(300, 300)
        self.max_projection_layout = QHBoxLayout()
        self.max_projection_box.setLayout(self.max_projection_layout)

        if self.maxproj_path is not None:
            # ==Maximum Projection View== #


            self.max_projection_controls = QVBoxLayout()
            self.max_projection_controls.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.zoom_in = QPushButton("+")
            self.zoom_out = QPushButton("-")
            self.zoom_reset = QPushButton("R")
            self.zoom_in.clicked.connect(self.zoom_image_in)
            self.zoom_out.clicked.connect(self.zoom_image_out)
            self.zoom_reset.clicked.connect(self.reset_image_zoom)

            self.max_projection_controls.addWidget(self.zoom_in)
            self.max_projection_controls.addWidget(self.zoom_out)
            self.max_projection_controls.addWidget(self.zoom_reset)
            self.max_projection_layout.addLayout(self.max_projection_controls)
            self.max_projection = MaximumProjection(self.cells, self.cell_contours, self.maxproj_path)
            self.max_projection_view = QGraphicsView()

            self.max_projection_view.setScene(self.max_projection)

            self.max_projection_layout.addWidget(self.max_projection_view)

            # Add the list and max projection box to the top half layout
        self.top_half_container.addWidget(self.max_projection_box)

        self.main_layout.addLayout(self.top_half_container)

        # ==BOTTOM HALF== #
        self.bottom_half_container = QHBoxLayout()  # Layout for the bottom half of the GUI

        # ==CELL TRACE REGION== #
        self.cell_trace_box = QGroupBox("Traces")  # Create the cell trace box and add it to the layout
        self.cell_trace_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.cell_trace_box.setMinimumHeight(300)

        self.cell_trace_box_layout = QHBoxLayout()
        self.cell_trace_box.setLayout(self.cell_trace_box_layout)

        # ==Cell View List== #
        self.cell_view_layout = QVBoxLayout()

        self.cell_view_list = QWidget()
        self.cell_view_checkbox_layout = QVBoxLayout(self.cell_view_list)
        self._populate_view_list()

        self.cell_view_scroll_area = QScrollArea()
        self.cell_view_scroll_area.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.cell_view_scroll_area.setMinimumWidth(100)
        self.cell_view_scroll_area.setWidget(self.cell_view_list)

        self.cell_view_controls_layout = QHBoxLayout()
        self.view_all_button = QPushButton(u'View All')
        self.view_none_button = QPushButton(u'View None')
        self.transfer_view_button = QPushButton(u'^ Transfer Selection ^')
        self.view_all_button.clicked.connect(self.view_all)
        self.view_none_button.clicked.connect(self.view_none)
        self.transfer_view_button.clicked.connect(self.transfer_view)
        self.cell_view_controls_layout.addWidget(self.view_all_button)
        self.cell_view_controls_layout.addWidget(self.view_none_button)

        self.cell_view_layout.addWidget(self.cell_view_scroll_area)
        self.cell_view_layout.addLayout(self.cell_view_controls_layout)
        self.cell_view_layout.addWidget(self.transfer_view_button) 
        self.cell_trace_box_layout.addLayout(self.cell_view_layout)

        # ==Cell Trace View== #
        self.cell_trace_scroll_area = QListWidget()
        self.cell_trace_box_layout.addWidget(self.cell_trace_scroll_area)
        self.cell_trace_scroll_area.setSizeAdjustPolicy(QListWidget.SizeAdjustPolicy.AdjustToContents)
        self.cell_trace_scroll_area.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,
                                                  QSizePolicy.Policy.MinimumExpanding)
        self.cell_trace_scroll_area.setSpacing(2)
        self.cell_trace_scroll_area.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.cell_trace_scroll_area.verticalScrollBar().setSingleStep(7)

        self.bottom_half_container.addWidget(self.cell_trace_box)
        self.main_layout.addLayout(self.bottom_half_container)

    def closeEvent(self, e):
        self.reject()

    def reject(self):
        self.curated_cells = []
        super().reject()
