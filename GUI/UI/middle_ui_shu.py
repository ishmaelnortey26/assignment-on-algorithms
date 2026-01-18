"""
shuffle_cards_middle_panel.py

This module defines the ShuffleCardsMiddlePanel widget used in the AlgoLab GUI.
The panel provides a simple user interface for demonstrating a card shuffling
algorithm.

The panel allows the user to:
- select a deck type
- trigger the shuffle operation
- view the shuffled card order
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QGroupBox, QPushButton, QComboBox, QTextEdit
)
from PyQt5.QtCore import Qt,pyqtSignal

class ShuffleCardsMiddlePanel(QWidget):
    """
    ShuffleCardsMiddlePanel is a custom QWidget that represents the central
    user interface for the Shuffle Cards algorithm.

    This panel does not implement the shuffling algorithm itself.
    Instead, it collects user selections and displays the shuffled output
    produced by the main application logic.
    """
    runClicked = pyqtSignal()

    def __init__(self):
        """
        Initializes the Shuffle Cards panel.

        Sets up:
        - layout structure
        - deck selection controls
        - shuffle trigger button
        - output display area
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
        card = QGroupBox("Shuffle Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 12, 12, 12)
        card_layout.setSpacing(12)

        # Deck selection section
        lbl = QLabel("Choose a deck type")
        lbl.setObjectName("hint")
        card_layout.addWidget(lbl)

        # Horizontal layout for the combo box
        combo_row = QHBoxLayout()

        # Combo box allows the user to select a deck configuration
        self.deck_combo = QComboBox()
        self.deck_combo.setObjectName("comboBox")
        self.deck_combo.setFixedWidth(220)

        # Example deck options
        self.deck_combo.addItems([
            "standard 52 cards",
            "short deck (36 cards)",
            "custom deck"
        ])

        combo_row.addWidget(self.deck_combo, alignment=Qt.AlignLeft)
        combo_row.addStretch(1)
        card_layout.addLayout(combo_row)

        card_layout.addSpacing(10)

        # Shuffle button
        btn_row = QHBoxLayout()

        self.shuffle_btn = QPushButton("SHUFFLE CARDS")
        self.shuffle_btn.setObjectName("runButton")
        self.shuffle_btn.clicked.connect(self.runClicked.emit)
        self.shuffle_btn.setCursor(Qt.PointingHandCursor)
        self.shuffle_btn.setFixedWidth(160)

        btn_row.addWidget(self.shuffle_btn, alignment=Qt.AlignLeft)
        btn_row.addStretch(1)
        card_layout.addLayout(btn_row)

        card_layout.addSpacing(6)

        # Output section
        out_lbl = QLabel("Shuffled Order")
        out_lbl.setObjectName("hint")
        card_layout.addWidget(out_lbl)

        # Read-only text area for displaying shuffled cards
        self.output = QTextEdit()
        self.output.setObjectName("textBox")
        self.output.setReadOnly(True)
        self.output.setFixedHeight(180)
        self.output.setPlaceholderText("[♠10, ♣3, ♥8, ♦2, ...]")
        card_layout.addWidget(self.output)

        # Add the card to the root layout
        root.addWidget(card)
        root.addStretch(1)

    def get_input(self):
        """
        Returns user input for the Shuffle Deck algorithm.

        Since the shuffle operation does not require any text input
        from the user, this method simply returns an empty string.

        Keeping this method allows all algorithm panels to follow
        the same interface structure.
        """

        # Shuffle Deck does not need user input
        return ""

    def get_options(self):
        """
        Returns user-selected options for the Shuffle Deck algorithm.

        This method returns an empty dictionary because no additional
        options (like mode or parameters) are required at this stage.

        Maintaining this method ensures consistency across all panels.
        """

        # No options required
        return {}

    def set_output(self, text):
        """
        Displays the shuffled deck output in the UI.

        Parameters:
        - text (str): A string representing the shuffled card order

        This method:
        - Updates the output display area
        - Supports QTextEdit or QLineEdit depending on the UI design
        """

        # Display the shuffled deck in the output area
        self.output.setPlainText(text)  # Use setText() if QLineEdit is used

    def styles(self):
        """
        Returns the Qt Style Sheet (QSS) used to style the panel.

        Styling is kept separate from application logic to improve
        readability and maintainability.
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

        QLineEdit#lineEdit, QTextEdit#textBox {
            background: #ffffff;
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            padding: 8px;
        }

        QComboBox#comboBox {
            background: #ffffff;
            border: 1px solid #f7f7f7;
            border-radius: 6px;
            padding: 6px 10px;
        }

        QComboBox#comboBox::drop-down {
            border: none;
            width: 26px;
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
    w = ShuffleCardsMiddlePanel()
    w.setWindowTitle("Middle Panel - Shuffle Cards (UI Only)")
    w.resize(700, 520)
    w.show()
    sys.exit(app.exec_())
