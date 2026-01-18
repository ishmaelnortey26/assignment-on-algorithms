"""
This module defines the SidePanel widget used in the AlgoLab GUI application.
The SidePanel acts as a vertical navigation menu that allows the user to select
different algorithm demonstrations (e.g., sorting, recursion, encryption).

"""
import os
import sys
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QGroupBox,
    QPushButton, QApplication
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal

class SidePanel(QWidget):
    """
    SidePanel is a custom QWidget that provides a vertical, scrollable menu
    for selecting algorithms within the application.

    The widget emits a signal whenever an algorithm button is clicked,
    allowing the main application to react without tight coupling.
    """
    algorithmSelected = pyqtSignal(str)

    def __init__(self):
        """
        Initializes the SidePanel widget.

        This method sets up:
        - widget dimensions
        - custom styling (QSS)
        - icon directory paths
        - layout structure
        - algorithm sections and buttons
        """
        super().__init__()
        self.setFixedWidth(200)
        # Apply custom styles (QSS)
        self.setStyleSheet(self.styles())

        # Determine the directory containing this file
        # Used to load icon resources
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.icons_dir = os.path.join(base_dir, "icons")

        # Main layout for the side panel
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Container widget inside the scroll area
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setAlignment(Qt.AlignTop)

         # load font
        font_path = os.path.join(base_dir, "fonts", "Pokemon Hollow.ttf")
        print("FONT PATH:", font_path, "Exists?", os.path.exists(font_path))

        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            title_font = QFont(family)
        else:
            print("Failed to load font, using default.")
            title_font = QFont()  # fallback

        # Application title
        title = QLabel("AlgoLab")
        title.setObjectName("title")
        title.setFont(QFont(family))
        print("Loaded font family:", family)

        # title.setStyleSheet("font-family: Pokemon Solid, Segoe UI;")
        container_layout.addWidget(title)

        # Encryption section
        container_layout.addWidget(self.section("Encryption", [
            ("RSA Encryption", "RSA", "RSA.png")
        ]))

        # Recursion section
        container_layout.addWidget(self.section("Recursion", [
            ("Fibonacci", "Fibonacci", "Fibonacci.png"),
            ("Factorial", "Factorial", "Factorial.png")
        ]))

        # Sorting algorithms section
        container_layout.addWidget(self.section("Sorting", [
            ("Bubble Sort", "BubbleSort", "Bubbles.png"),
            ("Selection Sort", "SelectionSort", "Selection.png"),
            ("Merge Sort", "MergeSort", "Merge.png")
        ]))

        # Randomised algorithms section
        container_layout.addWidget(self.section("Randomised", [
            ("Shuffle Card", "ShuffleDeck", "ace.png")
        ]))

        # Miscellaneous algorithms section
        container_layout.addWidget(self.section("Others", [
            ("Palindrome", "PalindromeDP", "binoculars.png"),
            ("Statistics", "SearchStats", "Statistics.png")
        ]))

        # Exit button (handled by parent application logic)
        # close = QPushButton("Exit")
        # close.setObjectName("algoButton1")
        # container_layout.addWidget(close)

        # Add the container widget to the main layout
        main_layout.addWidget(container)

    def _on_algo_clicked(self):
        """
        Slot function that is called when any algorithm button is clicked.

        This method:
        1. Detects which button was clicked
        2. Reads the algorithm key stored inside that button
        3. Emits a signal with the selected algorithm key

        This allows the main window to know which algorithm
        the user selected from the side panel.
        """

        # Get the button that triggered this function
        btn = self.sender()

        # Retrieve the custom property stored in the button
        # (e.g. "rsa", "fibonacci", "bubble_sort")
        algo_key = btn.property("algo_key")

        # If a valid algorithm key exists
        if algo_key:
            # Emit the signal with the selected algorithm key
            self.algorithmSelected.emit(algo_key)

    def section(self, title, items):
        """
        Creates a titled section containing algorithm buttons.

        Parameters:
        - title (str): The section heading displayed to the user.
        - items (list): A list of tuples in the form
          (display_text, algorithm_key, icon_filename).

        Returns:
        - QGroupBox: A group box containing styled algorithm buttons.
        """

        box = QGroupBox(title)
        layout = QVBoxLayout()

        # Reduce spacing for a compact vertical menu
        layout.setSpacing(0)
        layout.setContentsMargins(10, 0, 0, 0)

        for text, algo_key, icon in items:
            btn = QPushButton(text)
            btn.setObjectName("algoButton")
            btn.setCursor(Qt.PointingHandCursor)

            # Store algorithm identifier in button properties
            btn.setProperty("algo_key", algo_key)
            btn.clicked.connect(self._on_algo_clicked)

            # Load icon if it exists
            icon_path = os.path.join(self.icons_dir, icon)
            # print("ICON CHECK:", icon, "=>", icon_path, "exists?", os.path.exists(icon_path))
            if os.path.exists(icon_path):
                btn.setIcon(QIcon(icon_path))
                btn.setIconSize(QSize(18, 18))
            layout.addWidget(btn)

        box.setLayout(layout)
        return box

    def styles(self):
        """
        Returns the Qt Style Sheet (QSS) used to style the SidePanel.

        QSS allows separation of logic and appearance, similar to CSS
        in web development.
        """
        return """
        QWidget {
            background: #ffffff;
            
            font-size: 14px;
        }

        #title {
            color: blue;
            font-size: 40px;
            font-weight: bold;
            padding: 5px 10px;
           
        }

        QGroupBox {
            font-weight: bold;
            margin-top: 10px;
            padding: 10px;
            border: 1px solid #d0d0d0;
            border-radius: 6px;
        }

        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px;
        }

        QPushButton#algoButton {
            text-align: left;
            padding: 2px 5px;
            border: none;
            background: transparent;
        }

        QPushButton#algoButton:hover {
            background: #e0e0e0;
            border-radius: 4px;
        }

        QPushButton#algoButton:pressed {
            background: #c8c8c8;
        }

        QPushButton#algoButton1 {
            text-align: left;
            padding: 2px 5px;
            border: 1px;
            color: blue;
        }

        QPushButton#algoButton1:pressed {
            color: white;
        }
        """



if __name__ == "__main__":
    """
    Standalone execution block used for testing the SidePanel widget
    independently from the rest of the application.
    """
    # Enable high DPI scaling for modern displays
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)



    app = QApplication(sys.argv)
    w = SidePanel()
    w.show()
    sys.exit(app.exec_())
