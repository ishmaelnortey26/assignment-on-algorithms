"""
rsa_middle_panel.py

This module defines the RSAMiddlePanel widget used in the AlgoLab GUI.
The panel provides a user interface for RSA encryption and decryption.

Responsibilities of this panel:
- Collect message input (plain text or cipher text)
- Let the user choose Encrypt or Decrypt mode
- Optionally allow the user to supply their own keys
- Emit a signal when the RUN button is clicked

"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QTextEdit, QLineEdit, QPushButton, QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt,pyqtSignal

class RSAMiddlePanel(QWidget):
    """
    RSAMiddlePanel is a custom QWidget that represents the central UI
    for RSA encryption and decryption.

    The panel emits a signal when the user clicks RUN. The main window
    (controller) should listen for this signal, run RSA logic, then call
    set_output(...) to display results.
    """
    runClicked = pyqtSignal()

    def __init__(self):
        """
        Initializes the RSA panel UI.

        Sets up:
        - message input box
        - encrypt/decrypt selection
        - optional key inputs
        - output display
        - consistent styling via Qt Style Sheets (QSS)
        """
        super().__init__()

        # Apply QSS styling to the widget
        self.setStyleSheet(self.styles())

        # Root layout for the panel
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 5, 0, 5)
        root.setSpacing(10)

        # Card container
        card = QGroupBox("RSA Encryption and Decryption")

        # Layout inside the card container
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(12, 12, 12, 12)
        card_layout.setSpacing(10)

        # Message input
        hint = QLabel("Enter message to encrypt or decrypt")
        hint.setObjectName("hint")
        card_layout.addWidget(hint)

        # Multi-line text input for the message/ciphertext
        self.message_in = QTextEdit()
        self.message_in.setObjectName("textBox")
        self.message_in.setFixedHeight(120)
        card_layout.addWidget(self.message_in)

        # Mode selection (Encrypt / Decrypt)
        mode_row = QHBoxLayout()
        mode_row.setSpacing(12)

        mode_lbl = QLabel("Mode:")
        mode_lbl.setFixedWidth(60)
        mode_row.addWidget(mode_lbl)

        self.rb_encrypt = QRadioButton("Encrypt")
        self.rb_decrypt = QRadioButton("Decrypt")

        # Default action: Encrypt
        self.rb_encrypt.setChecked(True)

        # Group ensures only one radio button can be selected
        self.mode_group = QButtonGroup(self)
        self.mode_group.addButton(self.rb_encrypt)
        self.mode_group.addButton(self.rb_decrypt)

        mode_row.addWidget(self.rb_encrypt)
        mode_row.addWidget(self.rb_decrypt)
        mode_row.addStretch(1)
        card_layout.addLayout(mode_row)

        # Key usage selection (Use your own keys?)
        keys_row = QHBoxLayout()
        keys_row.setSpacing(12)

        keys_lbl = QLabel("Use Your Own Keys?")
        keys_lbl.setFixedWidth(160)
        keys_row.addWidget(keys_lbl)

        self.rb_keys_yes = QRadioButton("Yes")
        self.rb_keys_no = QRadioButton("No")

        # Default: use generated keys (user does not provide keys)
        self.rb_keys_no.setChecked(True)

        self.keys_group = QButtonGroup(self)
        self.keys_group.addButton(self.rb_keys_yes)
        self.keys_group.addButton(self.rb_keys_no)

        keys_row.addWidget(self.rb_keys_yes)
        keys_row.addWidget(self.rb_keys_no)
        keys_row.addStretch(1)
        card_layout.addLayout(keys_row)

        # Key input fields (disabled by default)
        # Public key input is used for encryption: expects "e,n"
        pub_lbl = QLabel("Public key (format: e,n)")
        card_layout.addWidget(pub_lbl)

        self.public_key = QLineEdit()
        self.public_key.setObjectName("lineEdit")
        card_layout.addWidget(self.public_key)

        # Private key input is used for decryption: expects "d,n"
        priv_lbl = QLabel("Private key (format: d,n)")
        card_layout.addWidget(priv_lbl)

        self.private_key = QLineEdit()
        self.private_key.setObjectName("lineEdit")
        card_layout.addWidget(self.private_key)

        # Disable key fields unless the user selects "Yes"
        self.public_key.setEnabled(False)
        self.private_key.setEnabled(False)

        # RUN button
        run_row = QHBoxLayout()

        self.run_btn = QPushButton("RUN")
        self.run_btn.setObjectName("runButton")
        self.run_btn.clicked.connect(self.runClicked.emit)
        self.run_btn.setCursor(Qt.PointingHandCursor)
        self.run_btn.setFixedWidth(90)
        run_row.addWidget(self.run_btn, alignment=Qt.AlignLeft)
        run_row.addStretch(1)
        card_layout.addLayout(run_row)

        # Output display
        self.output = QTextEdit()
        self.output.setObjectName("textBox")
        self.output.setReadOnly(True)
        self.output.setFixedHeight(140)
        card_layout.addWidget(self.output)

        # Add the card to the root layout
        root.addWidget(card)

        # Enable / disable key inputs when the user toggles "Yes"
        self.rb_keys_yes.toggled.connect(self._toggle_keys_enabled)

    # UI BEHAVIOUR(INTERNAL HELPERS)
    def _toggle_keys_enabled(self, checked: bool):
        """
        Enables or disables the key input fields based on user choice.

        Parameters:
        - checked (bool): True when "Use Your Own Keys? = Yes" is selected
        """
        self.public_key.setEnabled(checked)
        self.private_key.setEnabled(checked)

    def get_input(self):
        """
        Returns the message entered by the user.

        This method:
        - Reads the text from the message input box
        - Returns it as a string for encryption or decryption


        """

        # Get the full text entered from the message QTextEdit
        return self.message_in.toPlainText()

    def get_options(self):
        """
        Collects and returns all RSA-related options selected by the user.

        This method determines:
        - Whether the user wants to encrypt or decrypt
        - Whether the user wants to use their own keys or system-generated keys
        - Which keys to use (public or private), if provided

        Returns:
        - options (dict): A dictionary containing RSA configuration options
        """

        # Determine selected action
        action = "encrypt" if self.rb_encrypt.isChecked() else "decrypt"

        # Check whether user wants to provide their own keys
        use_user_keys = self.rb_keys_yes.isChecked()

        # Base options dictionary
        options = {
            "action": action,
            "use_user_keys": use_user_keys,
            "bits": 16  # Key size used when system generates keys automatically
        }

        # If user chooses to supply their own keys
        if use_user_keys:
            try:
                if action == "encrypt":
                    # Expect public key input in the form: "e,n"
                    parts = [p.strip() for p in self.public_key.text().split(",")]

                    if len(parts) == 2:
                        e = int(parts[0])
                        n = int(parts[1])
                        options["public_key"] = (e, n)

                else:
                    # Expect private key input in the form: "d,n"
                    parts = [p.strip() for p in self.private_key.text().split(",")]

                    if len(parts) == 2:
                        d = int(parts[0])
                        n = int(parts[1])
                        options["private_key"] = (d, n)

            except Exception:
                pass

        return options

    def set_output(self, text):
        """
        Displays the RSA output (encrypted or decrypted message) in the UI.

        Parameters:
        - text (str): The result produced by the RSA algorithm

        This method:
        - Converts the output to string (for safety)
        - Displays it in the output text area
        """

        # Display the result in the output QTextEdit
        self.output.setPlainText(str(text))


    # UI behaviour


    def _refresh_key_fields(self, *_):
        """
        Enables or disables RSA key input fields based on user selection.

        This method:
        - Checks whether the user selected Encrypt or Decrypt
        - Checks whether the user wants to use their own keys
        - Enables only the relevant key input fields
        - Disables all others to prevent incorrect input

        The `*_` parameter allows this method to safely receive
        extra arguments from Qt signals.
        """

        # Determine current action
        action = "encrypt" if self.rb_encrypt.isChecked() else "decrypt"

        # Check whether user enabled custom keys
        use = self.cb_user_keys.isChecked()

        # Disable all key-related input fields by default
        for w in (self.e_input, self.n_public_input, self.d_input, self.n_private_input):
            w.setEnabled(False)

        # If user does not want to use custom keys, stop here
        if not use:
            return

        # Enable only the fields required for the selected action
        if action == "encrypt":
            # Encryption needs public key (e, n)
            self.e_input.setEnabled(True)
            self.n_public_input.setEnabled(True)
        else:
            # Decryption needs private key (d, n)
            self.d_input.setEnabled(True)
            self.n_private_input.setEnabled(True)

    def styles(self):
        """
        Returns the Qt Style Sheet (QSS) used to style the RSA panel.

        QSS is used to keep UI styling separate from UI logic.
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

        /* Inputs */
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

        /* Primary action button */
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
            border-radius: 6px;
        }

        QPushButton#runButton:pressed {
            background: #1f4fb3;
        }
        """

if __name__ == "__main__":

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    w = RSAMiddlePanel()
    w.setWindowTitle("Middle Panel - RSA (UI Only)")
    w.resize(650, 520)
    w.show()
    sys.exit(app.exec_())


