"""
Name: DewanLab Manual Curation V2
Author: Austin Pauley (Dewan Lab, FSU)
Date: 06/2024
Desc: User interface to enable simultaneous visualization of 1-P calcium fluorescence traces (dF) along with the
spatial positioning of different cells. This interface is intended to be launched both from,
or independent of, the DewanLab InscopixAnalysis.ipynb processing pipeline notebook.
"""
import os
os.environ['ISX'] = '0'

import qdarktheme
import pandas as pd
from PySide6.QtWidgets import QApplication

# Our Libraries
from .gui import ManualCurationUI
from ._components.analog_trace import AnalogTrace

import os

if 'calcium' in os.environ:
    from dewan_calcium.helpers.project_folder import ProjectFolder
    from dewan_calcium.helpers import parse_json


def launch_gui(root_directory_override=None, project_folder_override=None, cell_trace_data_override=None,
               cell_props_override=None, cell_contours_override=None):
    # See if an application exists, if not make our own
    app = QApplication.instance()
    if not app:
        app = QApplication([])

    qdarktheme.setup_theme('dark')

    if project_folder_override is None:
        project_folder = ProjectFolder('MAN', root_dir=root_directory_override,
                                       select_dir=True, existing_app=app)
        # If no folder provided, we pick
    else:
        project_folder = project_folder_override

    cell_trace_data, cell_props, cell_contours = get_data(project_folder, cell_trace_data_override,
                                                          cell_props_override, cell_contours_override)
    # Load all the raw data

    # There is some preprocessing needed if we load the data from disk
    # This replicates what is seen in the jupyter notebooks
    if cell_trace_data_override is None:
        cell_trace_data = _preprocess_trace_data(cell_trace_data)
    if cell_props_override is None:
        cell_props, cell_names = _preprocess_props(cell_props)

    cell_names = cell_props['Name'].values

    cell_traces = AnalogTrace.generate_cell_traces(cell_trace_data, cell_names)

    window = ManualCurationUI(cell_names, cell_traces, cell_contours,
                              project_folder.inscopix_dir.max_projection_path)

    window.show()
    return_val = app.exec()

    if return_val == 0:  # 0: Success! | 1: Failure!
        window.max_projection.save()
        return window.curated_cells
    else:
        return None


def launch_sniff_gui(sniff_traces: list[AnalogTrace], trial_names):
    # See if an application exists, if not make our own
    app = QApplication.instance()
    if not app:
        app = QApplication([])

    qdarktheme.setup_theme('dark')


    window = ManualCurationUI(trial_names, sniff_traces, None,
                              None)
    window.show()
    return_val = app.exec()

    if return_val == 0:  # 0: Success! | 1: Failure!
        return window.curated_cells
    else:
        return None


def get_data(project_folder, cell_trace_data_override, cell_props_override, cell_contours_override):
    if cell_trace_data_override is None:
        cell_trace_data = pd.read_csv(project_folder.inscopix_dir.cell_trace_path, engine='pyarrow')
    else:
        cell_trace_data = cell_trace_data_override

    if cell_props_override is None:
        cell_props = pd.read_csv(project_folder.inscopix_dir.props_path, header=0, engine='pyarrow')
    else:
        cell_props = cell_props_override

    if cell_contours_override is None:
        cell_contours = parse_json.get_outline_coordinates(project_folder.inscopix_dir.contours_path)
    else:
        cell_contours = cell_contours_override

    return cell_trace_data, cell_props, cell_contours


def _preprocess_trace_data(cell_trace_data):
    # Drop the first row which contains all 'undecided' labels which is the Inscopix default label.
    cell_trace_data = cell_trace_data.drop([0])
    # Force all dF/F values to be numbers and round times to 2 decimal places
    cell_trace_data = cell_trace_data.apply(pd.to_numeric, errors='coerce')
    # Set the times as the index so the listed data is all dF/F values
    cell_trace_data[cell_trace_data.columns[0]] = cell_trace_data[cell_trace_data.columns[0]].round(2)
    cell_trace_data = cell_trace_data.set_index(cell_trace_data.columns[0])
    # Remove spaces from column names and contents
    cell_trace_data.columns = cell_trace_data.columns.str.replace(" ", "")

    return cell_trace_data


def _preprocess_props(cell_props):
    # We only want cells that have one component
    cell_props = cell_props[cell_props['NumComponents'] == 1]
    # Get rid of the Status Column
    cell_props = cell_props.drop(columns='Status').reset_index(drop=True)
    # Extract the names of the cells
    cell_names = cell_props['Name'].values

    return cell_props, cell_names

