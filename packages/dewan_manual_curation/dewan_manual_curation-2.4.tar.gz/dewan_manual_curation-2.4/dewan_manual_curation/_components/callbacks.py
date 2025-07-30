""" Parent Class for ManualCurationUI to provide callback methods """

from PySide6.QtCore import Qt
from PySide6 import QtWidgets

UNCHECKED = Qt.CheckState.Unchecked
CHECKED = Qt.CheckState.Checked


class GuiCallbacks:

    def select_none(self):
        for checkbox in self.cell_selection_checkbox_list:
            checkbox.setCheckState(UNCHECKED)

    def select_all(self):
        for checkbox in self.cell_selection_checkbox_list:
            checkbox.setCheckState(CHECKED)

    def export_cells(self):
        for checkbox in self.cell_selection_checkbox_list:
            if checkbox.checkState() is CHECKED:
                self.curated_cells.append(checkbox.text())
        self.accept()

    def view_all(self):
        self.change_view_checkboxes(True)
        for trace in self.trace_pointers:
            trace.setHidden(False)

        if self.max_projection is not None:
            self.max_projection.reset_polygon_colors()

    def view_none(self):
        self.change_view_checkboxes(False)
        for trace in self.trace_pointers:
            trace.setHidden(True)
        if self.max_projection is not None:
            self.max_projection.reset_polygon_colors()

    def transfer_view(self):
        modifiers = QtWidgets.QApplication.keyboardModifiers()

        for i, checkbox in enumerate(self.cell_view_checkbox_list):
            selection_checkbox = self.cell_selection_checkbox_list[i]
            view_checkbox_state = checkbox.checkState()

            if modifiers == Qt.KeyboardModifier.ControlModifier:
                if view_checkbox_state == CHECKED:
                    view_checkbox_state = UNCHECKED
                else:
                    view_checkbox_state = CHECKED

            selection_checkbox.setCheckState(view_checkbox_state)


    def on_checkbox_release(self, checkbox):
        cell_key = checkbox.text()
        check_state = checkbox.checkState()

        outline_state = []

        if check_state == CHECKED:
            self.trace_pointers_dict[cell_key].setHidden(False)
            outline_state = 1
        elif check_state == UNCHECKED:
            self.trace_pointers_dict[cell_key].setHidden(True)
            outline_state = 0

        self.max_projection.change_outline_color(cell_key, outline_state)

    def change_view_checkboxes(self, checked=False):
        check_state = Qt.CheckState.Unchecked
        if checked:
            check_state = Qt.CheckState.Checked

        for checkbox in self.cell_view_checkbox_list:
            checkbox.setCheckState(check_state)

    def reset_image_zoom(self):
        self.scale = 1
        self.max_projection_view.fitInView(self.max_projection.itemsBoundingRect(), Qt.KeepAspectRatio)

    def zoom_image_in(self):
        self._zoom_image(1)

    def zoom_image_out(self):
        self._zoom_image(-1)
