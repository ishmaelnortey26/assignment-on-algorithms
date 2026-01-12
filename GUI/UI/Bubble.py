"""
bubble_sort_middle_panel.py

This module defines the BubbleSortMiddlePanel widget used in the AlgoLab GUI.
The panel serves as the main interaction area where the user:
- enters a list of numbers
- selects sorting options (ascending / descending)
- runs the selected sorting algorithm
- views the sorted output

The panel is designed to be reusable for multiple sorting algorithms
(Bubble Sort, Selection Sort, Merge Sort) by updating its title dynamically.
"""

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QGroupBox, QLineEdit, QPushButton, QRadioButton, QButtonGroup
)

class BubbleSortMiddlePanel(QWidget):
    """
    BubbleSortMiddlePanel is a custom QWidget that represents the
    central control panel for sorting algorithms.

    It collects user input, sorting preferences, and displays
    the resulting sorted output. The panel emits a signal when
    the RUN button is clicked so that the main application can
    execute the selected algorithm.
    """

    def __init__(self):
        """
        Initializes the middle panel UI for sorting algorithms.

        This method sets up:
        - layout structure
        - input fields
        - sorting option controls
        - output display
        - consistent styling using Qt Style Sheets (QSS)
        """
        super().__init__()
        # Apply QSS styling to the widget
        self.setStyleSheet(self.styles())

        # Root layout for the panel
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 5, 0, 5)
        root.setSpacing(10)

        # Card container
        self.card = QGroupBox("Bubble Sort")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(12, 12, 12, 12)
        card_layout.setSpacing(12)

        # Instruction text
        hint = QLabel("Enter a list of numbers separated with a comma (,)")
        hint.setObjectName("hint")
        card_layout.addWidget(hint)

        # Input field for the list of numbers
        self.input_list = QLineEdit()
        self.input_list.setObjectName("lineEdit")
        self.input_list.setPlaceholderText("e.g. 5, 2, 9, 1")
        card_layout.addWidget(self.input_list)

        # Sorting order selection
        sort_lbl = QLabel("Sort type:")
        sort_lbl.setObjectName("hint")
        card_layout.addWidget(sort_lbl)

        # Radio buttons for sorting order
        self.rb_asc = QRadioButton("Ascending")
        self.rb_desc = QRadioButton("Descending")
        self.rb_asc.setChecked(True)

        # Group radio buttons to ensure only one can be selected
        self.sort_group = QButtonGroup(self)
        self.sort_group.addButton(self.rb_asc)
        self.sort_group.addButton(self.rb_desc)

        card_layout.addWidget(self.rb_asc)
        card_layout.addWidget(self.rb_desc)

        card_layout.addSpacing(12)

        # RUN button row
        run_row = QHBoxLayout()

        self.run_btn = QPushButton("RUN")
        self.run_btn.setObjectName("runButton")
        self.run_btn.setCursor(Qt.PointingHandCursor)
        self.run_btn.setFixedWidth(90)

        run_row.addWidget(self.run_btn, alignment=Qt.AlignLeft)
        run_row.addStretch(1)
        card_layout.addLayout(run_row)

        # Output section
        out_lbl = QLabel("Sorted Output")
        out_lbl.setObjectName("hint")
        card_layout.addWidget(out_lbl)

        # Read-only output field
        self.output = QLineEdit()
        self.output.setObjectName("lineEdit")
        self.output.setReadOnly(True)
        card_layout.addWidget(self.output)

        # Add the card to the root layout
        root.addWidget(self.card)
        root.addStretch(1)

    def styles(self):
        """
        Returns the Qt Style Sheet (QSS) used to style the panel.

        Styling is kept separate from logic to improve maintainability
        and readability.
        """
        return """
        QWidget {
            background: #ffffff;
            font-family: Segoe UI;
            font-size: 14px;
        }

        QLabel#hint {
            font-weight: bold;
        }

        QGroupBox {
            font-weight: bold;
            margin-top: 10px;
            padding: 10px;
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            background: #ffffff;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px;
        }

        QLineEdit#lineEdit {
            background: #ffffff;
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            padding: 8px;
        }

        QLineEdit#lineEdit:disabled {
            background: #eeeeee;
            color: #777777;
        }

        QRadioButton {
            spacing: 8px;
        }

        QRadioButton::indicator {
            width: 14px;
            height: 14px;
        }

        QPushButton#runButton {
            text-align: center;
            padding: 6px 12px;
            border: none;
            border-radius: 6px;
            background: #2f6fed;
            color: white;
            font-weight: bold;
        }

        QPushButton#runButton:hover {
            background: #255dd0;
        }

        QPushButton#runButton:pressed {
            background: #1f4fb3;
        }
        """


if __name__ == "__main__":
    """
    Standalone execution block for testing the middle panel UI
    independently from the rest of the application.
    """
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    w = BubbleSortMiddlePanel()
    w.setWindowTitle("Middle Panel - Sorting (UI Only)")
    w.resize(700, 520)
    w.show()
    sys.exit(app.exec_())



