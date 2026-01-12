"""
statistics_middle_panel.py

This module defines the StatisticsMiddlePanel widget used in the AlgoLab GUI.
The panel provides a user interface for computing basic statistics from a list
of numbers entered by the user.

The UI supports selecting one operation at a time via radio buttons:
- Largest (max)
- Smallest (min)
- Mode
- Median
- 1st Quartile (Q1)
- 3rd Quartile (Q3)
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QGroupBox, QLineEdit, QPushButton, QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt

class StatisticsMiddlePanel(QWidget):
    """
    StatisticsMiddlePanel is a custom QWidget that provides the central UI
    for the statistics/search part of the assignment.

    Responsibilities:
    - accept a comma-separated list of numbers from the user
    - allow the user to choose a single statistic operation
    - emit a RUN signal so the main window can compute results
    - display the chosen statistic value in a read-only output field
    """

    def __init__(self):
        """
        Initializes the statistics panel UI.

        Sets up:
        - input field for a list of numbers
        - radio-button selection of operation
        - RUN button (signal only)
        - result label and result output field
        - styling via Qt Style Sheets (QSS)
        """
        super().__init__()

        # Apply QSS styling to the widget
        self.setStyleSheet(self.styles())

        # Root layout for the panel
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 5, 0, 5)
        root.setSpacing(10)

        # Card container
        card = QGroupBox("Statistics")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 12, 12, 12)
        card_layout.setSpacing(12)

        # Input section
        in_lbl = QLabel("Enter list of numbers separated with comma (,)")
        in_lbl.setObjectName("hint")
        card_layout.addWidget(in_lbl)

        # Input field for number list (comma-separated)
        self.input_list = QLineEdit()
        self.input_list.setObjectName("lineEdit")
        self.input_list.setPlaceholderText("e.g. 10, 2, 5, 5, 9")
        card_layout.addWidget(self.input_list)

        # Operation selection
        op_lbl = QLabel("Select operation")
        op_lbl.setObjectName("opTitle")
        card_layout.addWidget(op_lbl)

        # Create radio buttons for statistics operations
        self.rb_max = QRadioButton("Largest")
        self.rb_min = QRadioButton("Smallest")
        self.rb_mean = QRadioButton("Mode")
        self.rb_median = QRadioButton("Median")
        self.rb_mode = QRadioButton("1st Quartile")
        self.rb_mode2 = QRadioButton("3nd Quartile")

        # Default selected option
        self.rb_max.setChecked(True)

        # ButtonGroup ensures only one radio button is selected at a time
        self.op_group = QButtonGroup(self)
        for rb in (self.rb_max, self.rb_min, self.rb_mean, self.rb_median, self.rb_mode, self.rb_mode2):
            self.op_group.addButton(rb)
            card_layout.addWidget(rb)

        card_layout.addSpacing(12)

        # RUN button
        run_row = QHBoxLayout()

        self.run_btn = QPushButton("RUN")
        self.run_btn.setObjectName("runButton")
        self.run_btn.setCursor(Qt.PointingHandCursor)
        self.run_btn.setFixedWidth(90)
        run_row.addWidget(self.run_btn, alignment=Qt.AlignLeft)
        run_row.addStretch(1)
        card_layout.addLayout(run_row)



        # Label shows which operation is currently selected
        self.result_label = QLabel("Median")
        self.result_label.setObjectName("hint")
        card_layout.addWidget(self.result_label)

        # Output field for result value (read-only)
        self.result_output = QLineEdit()
        self.result_output.setObjectName("lineEdit")
        self.result_output.setReadOnly(True)
        self.result_output.setFixedWidth(120)
        card_layout.addWidget(self.result_output, alignment=Qt.AlignLeft)

        # Update the result label whenever the selection changes
        # # self.op_group.buttonClicked.connect(self._update_result_label)
        # self._update_result_label()  # set label on startup

        # Add the card to the root layout
        root.addWidget(card)
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

         QLabel#opTitle {
             font-weight: bold;
             font-size: 18px;
             margin-top: 8px;
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
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    w = StatisticsMiddlePanel()
    w.setWindowTitle("Middle Panel - Statistics (UI Only)")
    w.resize(720, 560)
    w.show()
    sys.exit(app.exec_())

