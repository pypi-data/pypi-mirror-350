""" Parent Class for ManualCurationUI to provide general GUI function """


from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QCheckBox, QListWidgetItem, QGraphicsView, QSizePolicy
from functools import partial


# noinspection PyUnresolvedReferences
class GuiFuncs:
    def _populate_selection_list(self):
        for each in self.cells:
            selection_CB = QCheckBox(str(each))
            selection_CB.setCheckState(Qt.CheckState.Checked)
            self.cell_selection_checkbox_list.append(selection_CB)
            self.cell_select_checkbox_layout.addWidget(selection_CB)

    def _populate_view_list(self):
        for each in self.cells:
            view_CB = QCheckBox(str(each))
            view_CB.setCheckState(Qt.CheckState.Checked)
            view_CB.released.connect(partial(self.on_checkbox_release, view_CB))
            # Pass a reference of each checkbox to the click callback
            self.cell_view_checkbox_list.append(view_CB)
            self.cell_view_checkbox_layout.addWidget(view_CB)

    def _populate_cell_traces(self):
        for each in self.cell_traces:
            each.installEventFilter(self)
            _list_widget = QListWidgetItem()
            _list_widget.setSizeHint(QSize(each.width() / 3, each.height()))
            self.cell_trace_scroll_area.addItem(_list_widget)
            self.cell_trace_scroll_area.setItemWidget(_list_widget, each)

    def _zoom_image(self, steps: int):
        if steps != self.direction:
            self.scale = 1
            self.direction = steps

        self.scale += (self.scale_factor * steps)
        self.max_projection_view.scale(self.scale, self.scale)

    def _get_trace_pointers(self):
        for trace in range(self.cell_trace_scroll_area.count()):
            _trace = self.cell_trace_scroll_area.item(trace)
            self.trace_pointers.append(_trace)

        self.trace_pointers_dict = dict(list(zip(self.cells, self.trace_pointers)))

    def _configure_maxproj_view(self):
        self.max_projection_view.setInteractive(True)
        self.max_projection_view.setMouseTracking(True)
        self.max_projection_view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.max_projection_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.max_projection_view.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.max_projection_view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.max_projection_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.max_projection_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.max_projection_view.viewport().installEventFilter(self)

    def _init_window_params(self):
        self.setWindowTitle('Dewan Manual Curation')
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setFont(self.default_font)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.activateWindow()
