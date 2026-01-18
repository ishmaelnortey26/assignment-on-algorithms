"""
factorial_middle_panel.py

This module defines the FactorialMiddlePanel widget used in the AlgoLab GUI.
The panel provides a simple user interface for calculating the factorial
of a given number.

The panel is responsible only for collecting input and displaying output.
The actual factorial computation is expected to be handled by the main
application logic or algorithm module.
"""
import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QGroupBox, QLineEdit, QPushButton
)

class FactorialMiddlePanel(QWidget):
    """
    FactorialMiddlePanel is a custom QWidget that represents the central
    user interface for factorial calculation.

    It allows the user to:
    - enter a single integer value
    - trigger the calculation via a button
    - view the computed factorial result

    The panel emits a signal when the CALCULATE button is clicked so that
    the main application can perform the computation.
    """
    runClicked = pyqtSignal()

    def __init__(self):
        """
        Initializes the factorial calculator panel.

        This method sets up:
        - layout structure
        - input field for the number
        - output display
        - consistent UI styling using Qt Style Sheets (QSS)
        """
        super().__init__()

        # Apply QSS styling to the widget
        self.setStyleSheet(self.styles())


        # Root layout for the panel
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 5, 0, 5)
        root.setSpacing(10)

        # Card container
        card = QGroupBox("Factorial Calculator")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 12, 12, 12)
        card_layout.setSpacing(12)


        # Instruction label
        hint = QLabel("Enter a number")
        hint.setObjectName("hint")
        card_layout.addWidget(hint)

        # Input field
        self.input_n = QLineEdit()
        self.input_n.setObjectName("lineEdit")
        self.input_n.setFixedWidth(120)
        card_layout.addWidget(self.input_n, alignment=Qt.AlignLeft)

        # Calculate button row
        run_row = QHBoxLayout()
        self.run_btn = QPushButton("CALCULATE")
        self.run_btn.setObjectName("runButton")
        self.run_btn.clicked.connect(self.runClicked.emit)
        self.run_btn.setCursor(Qt.PointingHandCursor)
        self.run_btn.setFixedWidth(120)

        run_row.addWidget(self.run_btn, alignment=Qt.AlignLeft)
        run_row.addStretch(1)
        card_layout.addLayout(run_row)

        # Output section
        out_lbl = QLabel("Factorial value")
        out_lbl.setObjectName("hint")
        card_layout.addWidget(out_lbl)

        # Read-only output field for displaying result
        self.output = QLineEdit()
        self.output.setObjectName("lineEdit")
        self.output.setReadOnly(True)
        self.output.setFixedWidth(800)
        card_layout.addWidget(self.output, alignment=Qt.AlignLeft)

        # Add the card to the root layout
        root.addWidget(card)
        root.addStretch(1)

    def get_input(self):
        """
        Returns the user input for the factorial calculation.

        This method:
        - Reads the number entered by the user
        - Returns it as a string for processing by the factorial logic


        """

        # Get and return the input value
        return self.input_n.text()  # or .toPlainText() depending on widget type

    def get_options(self):
        """
        Returns user-selected options for the factorial algorithm.

        Factorial does not require any additional options,
        so this method returns an empty dictionary.


        """

        # No options required for factorial
        return {}

    def set_output(self, text):
        """
        Displays the factorial result in the output field.

        Parameters:
        - text (str): The calculated factorial value

        This method:
        - Updates the output widget
        - Shows the result to the user
        """

        # Display the factorial result
        self.output.setText(text)

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
    Standalone execution block for testing the factorial panel UI
    independently from the rest of the application.
    """
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    w = FactorialMiddlePanel()
    w.setWindowTitle("Middle Panel - Factorial (UI Only)")
    w.resize(600, 500)
    w.show()
    sys.exit(app.exec_())

