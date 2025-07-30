from typing import Dict, Tuple, List, Optional
import os

import numpy as np
from PyQt6.QtWidgets import (
    QVBoxLayout, QSizePolicy, QComboBox, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QMessageBox, QFileDialog, QInputDialog
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from ...FDTDiscover.dbPanel import signals
from ...FDTDiscover.dbPanel.models import DBObjects

from ...db_gui.top_level import TopLevel
from ...db_gui.widgets import TightNavigationToolbar
from .dataset import Dataset
from .linear_plt_subsettings.settings import LinearPlotSettings
from .ScalableLine2D import ScalableLine2D


class LinearPlotTab(QWidget):

    top: TopLevel

    # region PyQt6
    import_sampled_data: QPushButton
    settings: Optional[QWidget]
    # endregion

    # region Matplotlib
    fig: Figure
    canvas: FigureCanvas
    toolbar: TightNavigationToolbar
    datasets: Dict[str, Dataset]
    current_dataset: Dataset
    # endregion

    def _init_dataset(self, name: str, set_visible: bool = True) -> Optional[Dataset]:

        if name in self.datasets:
            QMessageBox.critical(self, "Name Error",
                                 f"Another dataset named '{name}' already exist. Please choose another name.")
            return None

        dataset = Dataset(name, self.fig, set_visible)

        # Add it to the dictionary of datasets
        self.datasets[name] = dataset

        # ✅ Update combo box
        self.dataset_selector.addItem(name)
        self.dataset_selector.blockSignals(True)
        self.dataset_selector.setCurrentText(name)
        self.dataset_selector.blockSignals(False)

        return dataset

    def _init_figure(self) -> None:

        # Init the figure, canvas and toolbar
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = TightNavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas, stretch=1)

        # Set up the main dataset
        self.datasets = {}
        self._init_dataset("__main__", set_visible=True)
        self.current_dataset = self.datasets["__main__"]
        self.redraw_plot()

    def _init_buttons(self) -> None:
        self.import_sampled_data = QPushButton("Import Sampled Data")
        self.add_to_dataset = QPushButton("Add to Dataset")
        self.add_to_dataset.setEnabled(False)
        self.settings_btn = QPushButton("Plot settings")
        self.settings_btn.clicked.connect(self.on_settings_clicked)

        self.import_sampled_data.clicked.connect(self.on_import_sampled_data_clicked)  # type: ignore
        self.add_to_dataset.clicked.connect(self.on_add_to_dataset_clicked)  # type: ignore

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.import_sampled_data)
        button_layout.addWidget(self.add_to_dataset)
        self.layout().addLayout(button_layout)

        self.layout().addWidget(QLabel("Select dataset"))
        self.layout().addWidget(self.dataset_selector)

        self.layout().addWidget(self.settings_btn)

    def _init_signals(self) -> None:
        # Prompt redraw of the canvas when tab is changed to the linear plot tab.
        self.top.tabs.currentChanged.connect(self.on_linear_tab_selected)  # type: ignore

    def _init_dataset_selector(self) -> None:
        self.dataset_selector = QComboBox()
        self.dataset_selector.wheelEvent = lambda event: None
        self.dataset_selector.setPlaceholderText("Select dataset")
        self.dataset_selector.currentTextChanged.connect(self.on_dataset_selected)  # type: ignore

    def __init__(self, top: TopLevel):
        super().__init__()

        # Assign the layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Assign the settings window variable
        self.settings = None

        # Assign reference to the top level
        self.top = top

        # Connect the monitor selected signal
        signals.dbRightClickMenuSignalBus.plotPower.connect(self.on_monitor_selected)

        # Init the dataset selector
        self._init_dataset_selector()

        # Init the figure
        self._init_figure()

        # Init buttons
        self._init_buttons()

        # Init signals
        self._init_signals()

    # region Callbacks
    def on_dataset_selected(self, name: str) -> None:
        if name and name in self.datasets:
            self.display_dataset(name)

    def on_settings_clicked(self) -> None:
        if not self.settings:
            self.settings = QWidget()
            self.settings.setWindowTitle("Plot Settings")
            self.settings.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Maximum)
            self.settings.setMaximumHeight(500)

            layout = QVBoxLayout()
            layout.addWidget(LinearPlotSettings(self, self.current_dataset))
            self.settings.setLayout(layout)

            self.settings.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            self.settings.destroyed.connect(lambda: setattr(self, "settings", None))

            self.settings.show()
        else:
            self.settings.close()
            self.settings.deleteLater()
            self.settings = None

    def change_settings_dataset(self) -> None:
        if self.settings:
            prev_layout = self.settings.layout()
            new_layout = QVBoxLayout()
            self.settings.setLayout(new_layout)
            prev_layout.deleteLater()
            new_layout.addWidget(LinearPlotSettings(self, self.current_dataset))

    def on_linear_tab_selected(self, index: int) -> None:
        if index == 1:
            self.redraw_plot()

    def on_import_sampled_data_clicked(self) -> None:
        file_paths = open_file_dialog(self)
        if not file_paths:
            return

        all_data, all_column_names, title = load_files(self, file_paths)
        if not all_data:
            return

        # Check column name consistency
        reference_labels = all_column_names[0]
        for other_labels in all_column_names[1:]:
            if other_labels[1:] != reference_labels[1:]:  # Skip x label
                QMessageBox.warning(self, "Import Warning",
                                    "Y-axis column names differ across files. Using names from first file.")
                break

        # Average Y values
        all_y_data = [data[:, 1:] for data in all_data]
        averaged_y = np.mean(np.stack(all_y_data, axis=0), axis=0)
        x_values = all_data[0][:, 0]
        y_labels = reference_labels[1:] if len(reference_labels) > 1 else [f"Column {i + 1}" for i in
                                                                           range(1, averaged_y.shape[1] + 1)]

        label_base = os.path.splitext(os.path.basename(file_paths[0]))[0] if len(file_paths) == 1 else "Averaged Data"

        # Detach and clear
        dataset = self.datasets["__main__"]
        dataset.detatch_artists_from_dataset()
        dataset.clear_title_and_labels()

        artists = []
        for i, y in enumerate(averaged_y.T):
            line_label = y_labels[i] if i < len(y_labels) else f"Column {i + 1}"
            line2d = dataset.ax.plot(x_values, y, label=line_label)[0]
            artists.append(ScalableLine2D.from_Line2D(line2d))

        # Label axes
        print(title)
        dataset.xlabel.set_text(reference_labels[0] if reference_labels else "X")
        dataset.xlabel.set_visible(True)

        # If title found, set it
        dataset.title.set_text(title if type(title) is str else "")
        dataset.title.set_visible(True)

        if averaged_y.shape[1] == 1:
            dataset.ylabel.set_text(y_labels[0])
            dataset.ylabel.set_visible(True)
        else:
            dataset.ylabel.set_text("")
            dataset.ylabel.set_visible(False)

        dataset.relim()
        self.display_dataset("__main__")
        self.add_to_dataset.setEnabled(True)

    def on_monitor_selected(self, monitors: DBObjects) -> None:
        monitorData: List[Tuple[str, np.ndarray, np.ndarray]] = []
        for monitor in monitors:
            result: Tuple[np.ndarray, np.ndarray] = monitor["dbHandler"].get_T_data(monitor["id"])
            if result is not None:
                monitorData.append((monitor["name"], *result))

        # Detatch the artists from the main dataset and clear titles and labels
        dataset = self.datasets["__main__"]
        dataset.detatch_artists_from_dataset()
        dataset.clear_title_and_labels()

        # Plot all curves
        all_artists = []
        for name, wavelengths, power in monitorData:
            line2d_artists = dataset.ax.plot(wavelengths, power, label=name)
            scaled_artists = [ScalableLine2D.from_Line2D(artist) for artist in line2d_artists]
            all_artists.extend(scaled_artists)

        dataset.xlabel.set_text("Wavelength [nm]")
        dataset.ylabel.set_text("T")
        dataset.relim()

        self.display_dataset("__main__")
        dataset.update_legend()

        # Enable the add_to_dataset_button
        self.add_to_dataset.setEnabled(True)

    def on_add_to_dataset_clicked(self) -> None:

        if not any([line.get_visible() for line in self.current_dataset.ax.lines]):
            return

        # Ask user for a dataset name
        dataset_names = list(self.datasets.keys())
        if "__main__" in dataset_names:
            dataset_names.remove("__main__")

        options = dataset_names + ["<Create New Dataset>"]
        if len(options) == 1:
            dataset_name = "<Create New Dataset>"
        else:
            dataset_name, ok = QInputDialog.getItem(
                self,
                "Select Dataset",
                "Select an existing dataset or create a new one:",
                options,
                editable=False
            )

            if not ok:
                return

        if dataset_name == "<Create New Dataset>":
            new_dataset = True
            dataset_name, ok = QInputDialog.getText(
                self,
                "New Dataset",
                "Enter name for new dataset:"
            )

            if not ok or not dataset_name:
                return
        else:
            new_dataset = False

        # Fetch reference to the main dataset
        main = self.datasets["__main__"]

        # Fetch the artists that will be transferred to the new dataset, while clearing the main dataset.
        main_artists = main.detatch_artists_from_dataset()

        # Update the x and y labels if it's a new dataset.
        if new_dataset:
            dataset = self._init_dataset(dataset_name, set_visible=True)
            if not dataset:
                return
            dataset.xlabel.set_text(self.current_dataset.xlabel.get_text())
            dataset.ylabel.set_text(self.current_dataset.ylabel.get_text())
        else:
            dataset = self.datasets[dataset_name]

        # Clear titles and labels from the main dataset.
        main.clear_title_and_labels()

        # Fetch the existing artists in the dataset
        existing_artists = dataset.ax.lines
        for artist in main_artists:
            dataset.add_artist(artist)

        # Display new dataset
        self.display_dataset(dataset_name)

        # Disable the add to dataset button.
        self.add_to_dataset.setEnabled(False)

    # endregion

    # region Events
    def resizeEvent(self, a0) -> None:
        self.redraw_plot()
        super().resizeEvent(a0)
    # endregion

    # region Plotting methods
    def update_plot(self) -> None:
        ...

    def redraw_plot(self) -> None:
        # Anchor the current plot to the center and enforce tight layout.
        self.current_dataset.ax.set_anchor("C")
        self.fig.tight_layout()

        # Redraw contents
        self.canvas.draw_idle()

    def detach_artists_from_main_dataset(self, redraw: bool = True) -> List[Line2D]:
        artists = []
        for _, artist in self.datasets["__main__"].ax.lines:
            artists.append(artist)
            artist.remove()
        if redraw:
            self.redraw_plot()
        return artists

    def clear_titles_and_labels_from_main_dataset(self, redraw: bool = True) -> None:
        main = self.datasets["__main__"]
        main.xlabel.set_text("")
        main.ylabel.set_text("")
        main.title.set_text("")
        if redraw:
            self.redraw_plot()

    def display_dataset(self, dataset_name: str) -> None:

        if self.settings:
            self.settings.close()
            self.on_settings_clicked()

        if self.current_dataset.name == dataset_name:
            self.current_dataset.update_legend()
            self.redraw_plot()
            return
        else:
            self.dataset_selector.blockSignals(True)
            self.dataset_selector.setCurrentText(dataset_name)
            self.dataset_selector.blockSignals(False)
            self.current_dataset.ax.set_visible(False)
            self.current_dataset = self.datasets[dataset_name]
            self.current_dataset.ax.set_visible(True)
            self.current_dataset.update_legend()
            self.redraw_plot()
    # endregion

    # region Overrides
    def layout(self) -> QVBoxLayout:
        return super().layout()  # type: ignore
    # endregion


# region Functions
def load_multi_column_data(file_path: str) -> Tuple[np.ndarray, List[str], Optional[str]]:
    lines: List[str] = []
    data: List[List[float]] = []
    column_names: List[str] = []
    title: Optional[str] = None

    # Read all non-empty lines
    with open(file_path, "r") as f:
        for line in f:
            stripped = line.strip()
            if stripped:
                lines.append(stripped)

    numeric_start_index = None
    num_columns = 0

    def parse_parts(line: str) -> List[str]:
        return [p.strip() for p in line.split(",") if p.strip()]

    def is_numeric_row(parts: List[str]) -> bool:
        try:
            [float(p) for p in parts]
            return True
        except ValueError:
            return False

    # --- Find first numeric line ---
    for i, line in enumerate(lines):
        parts = parse_parts(line)
        if len(parts) < 2:
            continue
        if is_numeric_row(parts):
            numeric_start_index = i
            num_columns = len(parts)
            break

    if numeric_start_index is None:
        return np.empty((0, 0)), [], None

    # --- Look for column names above ---
    for j in range(numeric_start_index - 1, -1, -1):
        parts = parse_parts(lines[j])
        print(parts)
        if len(parts) == num_columns and not is_numeric_row(parts):
            column_names = parts
            # Look for title above the column name line
            for k in range(j - 1, -1, -1):
                if len(lines[k]) > 0:
                    title = lines[k].strip()
                    break
            break

    # --- Parse data ---
    for line in lines[numeric_start_index:]:
        parts = parse_parts(line)
        if len(parts) != num_columns:
            continue
        try:
            data.append([float(p) for p in parts])
        except ValueError:
            continue

    if not data:
        return np.empty((0, 0)), [], None

    array = np.array(data)

    # --- Fallback column names ---
    if not column_names:
        column_names = [f"Column {i+1}" for i in range(array.shape[1])]

    elif len(column_names) < array.shape[1]:
        column_names += [f"Column {i+1}" for i in range(len(column_names), array.shape[1])]

    return array, column_names, title


def open_file_dialog(parent_widget: LinearPlotTab) -> List[str]:
    file_paths, _ = QFileDialog.getOpenFileNames(
        parent_widget,
        "Select one or more CSV or TXT files",
        "",
        "Data Files (*.csv *.txt);;All Files (*)"
    )
    return file_paths


def load_files(parent_widget: LinearPlotTab,
               file_paths: List[str]) -> Optional[Tuple[List[np.ndarray], List[List[str]], Optional[str]]]:
    all_data = []
    all_column_names = []
    all_x_values = []
    title = None

    for file_path in file_paths:
        try:
            data, column_names, title = load_multi_column_data(file_path)
        except Exception as e:
            QMessageBox.critical(parent_widget, "Import Error",
                                 f"Failed to load file:\n{file_path}\n\n{str(e)}")
            return [], [], None

        if data.size == 0 or data.shape[1] < 2:
            QMessageBox.warning(parent_widget,
                                "Import Warning", f"No valid data found in file:\n{file_path}")
            return [], [], None

        all_data.append(data)
        all_column_names.append(column_names)
        all_x_values.append(data[:, 0])

    # --- Check x-values are identical ---
    reference_x = all_x_values[0]
    for x in all_x_values[1:]:
        if not np.allclose(x, reference_x, rtol=1e-5, atol=1e-8):
            QMessageBox.critical(parent_widget, "Import Error",
                                 "Selected files do not have matching x-axis values.")
            return [], [], None

    return all_data, all_column_names, title


def check_label_mismatch_and_get_labels(parent_widget: LinearPlotTab,
                                        all_column_names: List[Tuple[str, str]]) -> Tuple[bool, bool, str, str]:
    ...

    # --- Check column names consistency ---
    reference_x_label, reference_y_label = all_column_names[0]
    x_label_mismatch = False
    y_label_mismatch = False

    for x_label, y_label in all_column_names[1:]:
        if x_label != reference_x_label:
            x_label_mismatch = True
        if y_label != reference_y_label:
            y_label_mismatch = True

    if x_label_mismatch:
        QMessageBox.warning(parent_widget, "Import Warning",
                            "X-axis labels differ across files. Using label from first file.")
    if y_label_mismatch:
        QMessageBox.warning(parent_widget, "Import Warning",
                            "Y-axis labels differ across files. Using label from first file.")

    return x_label_mismatch, y_label_mismatch, reference_x_label, reference_y_label
# endregion
