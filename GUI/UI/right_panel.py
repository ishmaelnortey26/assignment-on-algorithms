"""
performance_panel.py

This module defines the PerformancePanel widget used in the AlgoLab GUI.
The PerformancePanel displays metadata and performance information for
the currently selected algorithm, including:
- algorithm name
- execution time
- descriptive text
- a visual SVG illustration

The panel is designed to be updated dynamically by other UI components.
"""

import sys
import os

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QGroupBox, QFrame, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QSvgWidget

class PerformancePanel(QWidget):
    """
    PerformancePanel is a custom QWidget responsible for displaying
    algorithm performance and descriptive information.

    This panel does not execute algorithms itself. Instead, it provides
    an update-ready interface that can be controlled by other panels
    (e.g., a side menu or run button).
    """

    def __init__(self, icons_dir=None):
        """
        Initializes the PerformancePanel widget.

        Sets up:
        - layout structure
        - static labels for metadata
        - a central SVG image
        - a description area
        - custom styling using Qt Style Sheets (QSS)
        """
        super().__init__()
        self.setFixedWidth(220)

        # Apply custom QSS styling
        self.setStyleSheet(self.styles())

        # Root vertical layout for the panel
        root = QVBoxLayout(self)
        root.setContentsMargins(1, 1, 1, 1)
        root.setSpacing(10)

        # Card container
        card = QGroupBox("PERFORMANCE")

        box = QVBoxLayout(card)
        box.setContentsMargins(14, 28, 14, 14)
        box.setSpacing(4)

        # Displays the currently selected algorithm name
        self.algorithm_lbl = QLabel("Big O: —")
        self.algorithm_lbl.setObjectName("perfMeta")
        box.addWidget(self.algorithm_lbl)

        # Displays execution time (updated after running algorithm)
        self.time_lbl = QLabel("Time: —")
        self.time_lbl.setObjectName("perfMeta")
        box.addWidget(self.time_lbl)

        # Divider line
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setObjectName("divider")
        box.addWidget(divider)

        # SVG illustration
        # Determine directory of this file
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Use provided icon directory or default to local 'icons' folder
        icons_dir = icons_dir or os.path.join(base_dir, "icons")

        # Load SVG image used as a visual placeholder
        svg_path = os.path.join(icons_dir, "apps3.svg")

        self.center_image = QSvgWidget(svg_path)
        self.center_image.setFixedSize(170, 400)
        box.addWidget(self.center_image, alignment=Qt.AlignLeft)

        # Description section
        desc_hdr = QLabel("Description")
        desc_hdr.setObjectName("descHeader")
        box.addWidget(desc_hdr)

        # Label that displays algorithm description text
        self.desc_lbl = QLabel("")
        self.desc_lbl.setObjectName("descBody")
        self.desc_lbl.setWordWrap(True)
        self.desc_lbl.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        box.addWidget(self.desc_lbl)

        # Add the card to the root layout
        root.addWidget(card)

    def set_algorithm(self, name, description):
        self.algorithm_lbl.setText(f"Big O: {name}")
        self.desc_lbl.setText(description)
        self.time_lbl.setText("Time: —")

    def styles(self):
        return """
        QWidget {

            font-family: Segoe UI;
            font-size: 14px;
            color: #111;
        }

        QGroupBox#perfCard {
            background: #FFFDE1;
            border: 1px solid #dcdcdc;
            border-radius: 8px;
            font-weight: 700;
        }

        QGroupBox#perfCard::title {
            subcontrol-origin: margin;
            left: 12px;
            top: 8px;
            padding: 0 6px;
            font-size: 12px;
            letter-spacing: 2px;
            color: white;
        }

        QLabel#perfMeta {
            font-size: 13px;
            font-weight: 600;
        }

        QFrame#divider {

            color: #e1e3e8;
            max-height: 1px;
        }

        QLabel#chip {
            font-size: 12px;
            font-weight: 600;
            background: #f5f6f8;
            border: 1px solid #e1e3e8;
            border-radius: 999px;
            padding: 4px 10px;
        }

        QLabel#descHeader {
            font-size: 13px;
            font-weight: 800;
            margin-top: 6px;
        }

        QLabel#descBody {
            font-size: 13px;
            font-weight: 400;
            color: #333;
            line-height: 1.25;
        }
         QGroupBox {
            font-weight: bold;
            margin-top: 10px;
            padding: 10px;
            border: 1px solid #d0d0d0;
            border-radius: 6px;
            background: #ffffff;
        }
        """




if __name__ == "__main__":
    """
    Standalone execution block for testing the PerformancePanel widget
    independently from the rest of the application.
    """
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    panel = PerformancePanel()
    panel.show()
    sys.exit(app.exec_())


