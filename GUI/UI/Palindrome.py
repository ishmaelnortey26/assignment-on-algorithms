"""
palindrome_substring_middle_panel.py

This module defines the PalindromeSubstringMiddlePanel widget used in the AlgoLab GUI.
The panel provides a user interface for counting palindromic substrings within
a word or sentence entered by the user.

The panel is responsible only for:
- collecting input text
- emitting a signal when the user clicks the COUNT button
- displaying results provided by the algorithm layer (found substrings + total)
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QGroupBox, QTextEdit, QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt,pyqtSignal

class PalindromeSubstringMiddlePanel(QWidget):
    """
    PalindromeSubstringMiddlePanel is a custom QWidget that represents the
    central UI for the Palindrome Substring Counter feature.

    It allows the user to:
    - enter a word or sentence
    - run the palindrome substring counting logic
    - view found palindromic substrings (summary) and total count

    The panel emits a signal when the user clicks the COUNT button so that
    the main application can perform the computation.
    """
    runClicked = pyqtSignal()

    def __init__(self):
        """
        Initializes the palindrome substring panel UI.

        Sets up:
        - input text area
        - run button
        - output fields for found substrings and total count
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
        card = QGroupBox("Palindrome Substring Counter")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 12, 12, 12)
        card_layout.setSpacing(12)

        # Input section
        in_lbl = QLabel("Enter a word or sentence")
        in_lbl.setObjectName("hint")
        card_layout.addWidget(in_lbl)

        # Multiline input for text (supports sentences)
        self.input_text = QTextEdit()
        self.input_text.setObjectName("textBox")
        self.input_text.setFixedHeight(110)
        card_layout.addWidget(self.input_text)

        # Run button
        btn_row = QHBoxLayout()

        self.count_btn = QPushButton("COUNT SUBSTRING")
        self.count_btn.setObjectName("runButton")
        self.count_btn.clicked.connect(self.runClicked.emit)
        self.count_btn.setCursor(Qt.PointingHandCursor)
        self.count_btn.setFixedWidth(180)

        btn_row.addWidget(self.count_btn, alignment=Qt.AlignLeft)
        btn_row.addStretch(1)
        card_layout.addLayout(btn_row)

        # Output: found substrings
        found_lbl = QLabel("Palindrome Substrings found")
        found_lbl.setObjectName("hint")
        card_layout.addWidget(found_lbl)

        # Read-only output field showing found palindromes (summary or list)
        self.found_output = QLineEdit()
        self.found_output.setObjectName("lineEdit")
        self.found_output.setReadOnly(True)
        self.found_output.setMinimumHeight(44)
        card_layout.addWidget(self.found_output)

        # -------------------------------------------------
        # Output: total count
        # -------------------------------------------------
        total_lbl = QLabel("Total Palindromes")
        total_lbl.setObjectName("bigLabel")
        card_layout.addWidget(total_lbl)

        # Small output field showing the total number of palindromes
        self.total_output = QLineEdit()
        self.total_output.setObjectName("lineEdit")
        self.total_output.setReadOnly(True)
        self.total_output.setFixedWidth(80)
        card_layout.addWidget(self.total_output, alignment=Qt.AlignLeft)

        # Add the card to the root layout
        root.addWidget(card)

        # Push everything upwards (keeps the UI neat)
        root.addStretch(1)

    def get_input(self):
        """
        Returns the user input from the text box.

        This method:
        - Reads the text entered by the user
        - Returns it as a normal Python string

        It is usually called by the controller or logic layer
        to fetch user input for processing.
        """

        # Get and return all text from the QTextEdit widget
        return self.input_text.toPlainText()

    def get_options(self):
        """
        Returns user-selected options for the algorithm.

        Since Fibonacci does not require any additional options
        (like mode, order, or settings), this method returns
        an empty dictionary.

        Keeping this method allows all algorithm panels to
        follow the same interface structure.
        """

        # No options needed for Fibonacci
        return {}

    def set_results(self, found_text, total_count):
        """
        Displays the results of the algorithm in the UI.

        Parameters:
        - found_text (str): A string showing the found palindromes
          or a summary of results
        - total_count (int): The total number of palindromes found

        This method:
        - Updates the output fields in the UI
        - Converts numbers to string before displaying
        """

        # Display the list or summary of palindromes
        self.found_output.setText(found_text)

        # Display total count (convert integer to string)
        self.total_output.setText(str(total_count))

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

        QLabel#bigLabel {
            font-weight: bold;
            font-size: 22px;
            margin-top: 6px;
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

        QLineEdit#lineEdit, QTextEdit#textBox {
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
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    w = PalindromeSubstringMiddlePanel()
    w.setWindowTitle("Middle Panel - Palindrome (UI Only)")
    w.resize(720, 550)
    w.show()
    sys.exit(app.exec_())

