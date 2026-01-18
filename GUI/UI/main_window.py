"""
AlgoLab Main Window (GUI)

This file defines the main application window for AlgoLab.
It sets up the overall layout:
    - Left side panel (algorithm selection)
    - Middle panel (algorithm visualization / UI)
    - Right panel (performance & description)

This class acts as the *coordinator* between:
    - the GUI panels
    - the backend AlgorithmManager (Facade pattern)
"""

# GUI/main_window.py
import sys
from time import perf_counter

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QLabel, QStackedWidget
)

# Backend / Facade that executes algorithms
# from design_patterns import AlgorithmManager

# GUI panels
from design_patterns import AlgorithmManager
from side_panel import SidePanel
from right_panel import PerformancePanel

# Middle panels (algorithm-specific UIs)
from Bubble import BubbleSortMiddlePanel
from middle_ui_fac import FactorialMiddlePanel
from middle_ui_fib import FibonacciMiddlePanel
from middle_ui_shu import ShuffleCardsMiddlePanel
from Palindrome import PalindromeSubstringMiddlePanel
from middle_ui_sta import StatisticsMiddlePanel
from middle_ui_RSA import RSAMiddlePanel


class MainUI(QMainWindow):
    """
    Main application window.

    Responsibilities:
    - Create the main layout (left / middle / right)
    - Switch algorithm pages when user selects one
    - Pass input to AlgorithmManager
    - Display results and performance info
    """

    def __init__(self):
        """Initialize the main window and all UI components."""
        super().__init__()

        # Window title and size
        self.setWindowTitle("AlgoLab")
        self.resize(1100, 650)

        # Facade: central backend controller for algorithms
        self.manager = AlgorithmManager()

        # ROOT LAYOUT

        # Root widget (required for QMainWindow)
        root = QWidget()
        self.setCentralWidget(root)

        # Horizontal layout: left | middle | right
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(5)

        # LEFT PANEL

        # Side panel where user selects algorithms
        self.side_panel = SidePanel()
        root_layout.addWidget(self.side_panel)

        #  MIDDLE PANEL

        # Stacked widget holds all algorithm UIs
        # Only one page is visible at a time
        self.stack = QStackedWidget()
        root_layout.addWidget(self.stack, 1)  # stretch=1 makes it expand

        #  RIGHT PANEL

        # Performance & description panel
        self.right_panel = PerformancePanel()
        root_layout.addWidget(self.right_panel)

        # CREATE ALGORITHM PAGES

        self.page_factorial = FactorialMiddlePanel()
        self.page_fibonacci = FibonacciMiddlePanel()
        self.page_rsa = RSAMiddlePanel()
        self.page_shuffle = ShuffleCardsMiddlePanel()
        self.page_stats = StatisticsMiddlePanel()
        self.page_palindrome = PalindromeSubstringMiddlePanel()
        self.page_sorting = BubbleSortMiddlePanel()

        # Add all pages to the stacked widget
        for page in (
            self.page_factorial,
            self.page_fibonacci,
            self.page_rsa,
            self.page_shuffle,
            self.page_stats,
            self.page_palindrome,
            self.page_sorting,
        ):
            self.stack.addWidget(page)

        # ALGORITHM → PAGE MAP

        # Maps algorithm names to the UI page that should be shown
        self.pages = {
            "Factorial": self.page_factorial,
            "Fibonacci": self.page_fibonacci,
            "RSA": self.page_rsa,
            "ShuffleDeck": self.page_shuffle,
            "SearchStats": self.page_stats,
            "PalindromeDP": self.page_palindrome,

            # All sorting algorithms share the same UI
            "BubbleSort": self.page_sorting,
            "SelectionSort": self.page_sorting,
            "MergeSort": self.page_sorting,
        }

        # ALGORITHM INFO (RIGHT PANEL)
        # Text shown when an algorithm is selected
        self.algo_info = {
            "RSA": (
                "Varies (key-size dependent)",
                "Public-key encryption/decryption..It uses two keys: one to encrypt data and another to decrypt it, making secure communication possible.",


            ),
            "Fibonacci": (
                "O(n)",
                "The Fibonacci algorithm builds a sequence where each number is the sum of the two before it.eg..0, 1, 1, 2, 3, 5, 8, ....",


            ),
            "Factorial": (
                "O(n)",
                "Multiplies a number by all positive integers below it..eg..5! = 5 × 4 × 3 × 2 × 1 = 120",

            ),
            "BubbleSort": (
                "O(n²)",
                "Bubble Sort repeatedly compares neighboring values and swaps them if they are in the wrong order."
                "Larger values slowly “bubble” to the end of the list.",


            ),
            "SelectionSort": (
                "O(n²)",
                "Selection Sort repeatedly selects the smallest value from the unsorted part of the list and moves it to the front..",

            ),
            "MergeSort": (
                "O(n log n)",
                "Merge Sort divides the list into smaller parts, sorts them, and then merges them back together.",

            ),
            "ShuffleDeck": (
                "O(n)",
                "This algorithm randomly rearranges a deck of cards so that every order is equally likely.",

            ),
            "SearchStats": (
                "O(n log n)",
                "This algorithm calculates basic statistical values such as minimum, maximum median, and averages from a dataset.",

            ),
            "PalindromeDP": (
                "O(n²)",
                "This algorithm finds all substrings that read the same forwards and backwards..eg..level,racecar.",

            ),
        }

        # Listen for user selecting an algorithm
        self.side_panel.algorithmSelected.connect(self.on_algorithm_selected)
        self.on_algorithm_selected("RSA")

    # HELPER METHODS


    def _clear_current_page(self):
        """Clears input and output fields on the current page."""
        page = self.stack.currentWidget()

        # Clear input widgets
        for attr in ("input_list", "message_in", "input_text"):
            if hasattr(page, attr):
                getattr(page, attr).clear()

        # Clear output widgets
        for attr in (
            "output", "output_box", "result_output",
            "total_output", "found_output"
        ):
            if hasattr(page, attr):
                getattr(page, attr).clear()

    def _reset_performance_panel(self):
        """Resets the right performance panel."""
        self.right_panel.algorithm_lbl.setText("Big O: —")
        self.right_panel.time_lbl.setText("Time: —")
        self.right_panel.desc_lbl.setText("")


    # EVENT HANDLERS

    def on_algorithm_selected(self, algo_key):
        """
        Called when the user selects an algorithm
        from the side panel.
        """

        # Tell backend which algorithm is selected
        self.manager.setAlgorithm(algo_key)

        # Switch to correct middle page
        page = self.pages.get(algo_key)
        if page:
            self.stack.setCurrentWidget(page)

        # Clear previous data
        self._clear_current_page()
        self._reset_performance_panel()

        # Connect run button once (shared pages supported)
        for page in set(self.pages.values()):
            if hasattr(page, "runClicked"):
                page.runClicked.connect(self.on_run_clicked)

        # Special handling for sorting modes
        if algo_key in ("BubbleSort", "SelectionSort", "MergeSort"):
            page = self.pages.get(algo_key)
            if page and hasattr(page, "set_sort_mode"):
                page.set_sort_mode(algo_key)

        # Update right panel info
        info = self.algo_info.get(algo_key)
        if info:
            name, desc, category, complexity = info
            self.right_panel.set_algorithm(name, desc)
        else:
            self.right_panel.set_algorithm(algo_key, "")

    def on_run_clicked(self):
        """
        Executes the selected algorithm when
        the user clicks the Run button.
        """
        page = self.stack.currentWidget()

        raw_input = page.get_input() if hasattr(page, "get_input") else ""
        options = page.get_options() if hasattr(page, "get_options") else {}

        output, result = self.manager.execute(raw_input, options)

        # START TIMER
        start = perf_counter()
        # Run the algorithm (backend)
        output, result = self.manager.execute(raw_input, options)

        # ---- END TIMER ----
        end = perf_counter()
        elapsed_seconds = end - start

        # Show timing on the right panel (format nicely)

        if elapsed_seconds < 1:
            self.right_panel.time_lbl.setText(f"Time: {elapsed_seconds * 1000:.3f} ms")
        else:
            self.right_panel.time_lbl.setText(f"Time: {elapsed_seconds:.4f} s")

        # Handle different result types

        # Palindrome DP
        if isinstance(output, dict) and "found" in output:
            if hasattr(page, "set_results"):
                page.set_results(output["found"], output["count"])

        # Statistics
        elif isinstance(output, dict):
            if hasattr(page, "set_results"):
                page.set_results(output)

        # Simple output
        else:
            if hasattr(page, "set_output"):
                page.set_output(str(output))



# APPLICATION ENTRY POINT

if __name__ == "__main__":
    """
    Application entry point.
    Sets up high-DPI support and starts the event loop.
    """

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(app.exec_())
