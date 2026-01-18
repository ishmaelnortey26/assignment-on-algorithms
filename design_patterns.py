from abc import ABC, abstractmethod
from dataclasses import dataclass
import time
from algorithms_files.factorial import factorial
from algorithms_files.fibonacci import fibonacci
from algorithms_files.merge_sorting import merge_sort
from algorithms_files.bubble import bubble_sort
from algorithms_files.selection import selection_sort
from algorithms_files.shuffle_deck import shuffle_deck
from algorithms_files.palindrome import palindromic_substrings
from algorithms_files.searching import compute_statistics
from algorithms_files.rsa_encryption import generate_rsa_keys,rsa_encrypt_message,rsa_decrypt_message



# Data holder for performance + output

@dataclass
class RunResult:
    """
    Stores the result of running an algorithm.

    This is useful for:
    - showing the final output in the UI
    - measuring performance (time taken)
    - keeping a history of runs

    Fields:
    - algorithm_name: name of the algorithm that ran
    - output: the result (string or dict depending on algorithm)
    - time_taken: how long the algorithm took (seconds)
    - size: input size (here we store length of input text)
    """
    algorithm_name: str = ""
    output: str = ""
    time_taken: float = 0.0
    size: int = 0



# Strategy base class

class BaseAlgorithm(ABC):
    """
    Base class for all algorithms (Strategy Pattern).

    Each algorithm must:
    - have a name
    - declare whether it needs to input (requires_input)
    - implement the run() method


    """

    def __init__(self, name, requires_input=True):
        """
        Parameters:
        - name (str): algorithm name (e.g. "RSA", "Fibonacci")
        - requires_input (bool): whether user must type input
          (ShuffleDeck does not require input, so it sets this to False)
        """
        self.name = name
        self.requires_input = requires_input

    @abstractmethod
    def run(self, raw_input, options):
        """
        Runs the algorithm.

        Parameters:
        - raw_input (str): text from the UI input box
        - options (dict): extra settings (e.g. encrypt/decrypt, order)

        Returns:
        - result (str or dict): output from the algorithm
        """
        pass



# Placeholder algorithm classes
# (Real logic comes later)

class RSA(BaseAlgorithm):
    """
    RSA algorithm strategy.

    Supports:
    - Encrypt mode
    - Decrypt mode
    - User-provided keys OR system-generated keys

    Note:
    - Real RSA functions are called externally:
      generate_rsa_keys(), rsa_encrypt_message(), rsa_decrypt_message()
    """

    def __init__(self):
        super().__init__("RSA")
        self.public_key = None
        self.private_key = None

    def run(self, raw_input, options):
        """
        Runs RSA encryption/decryption depending on options.

        Options expected:
        - action: "encrypt" or "decrypt"
        - use_user_keys: bool
        - bits: key size used when generating keys
        - public_key: (e, n) tuple for encryption (if user provides)
        - private_key: (d, n) tuple for decryption (if user provides)
        """
        action = options.get("action", "encrypt")  # "encrypt" or "decrypt"
        use_user_keys = options.get("use_user_keys", False)
        bits = options.get("bits", 16)


        # Key handling

        if use_user_keys:
            # User wants to supply their own keys
            if action == "encrypt":
                # Encryption needs the PUBLIC key (e, n)
                pub = options.get("public_key")
                if not pub:
                    return "Error: enter your PUBLIC key as e,n (example: 65537,123456789)."
                self.public_key = pub

            else:  # decrypt
                # Decryption needs the PRIVATE key (d, n)
                priv = options.get("private_key")
                if not priv:
                    return "Error: enter your PRIVATE key as d,n (example: 12345,123456789)."
                self.private_key = priv

        # If system keys needed (no keys yet), generate them
        # (This covers the case: user chose "No" OR user didn't provide valid keys)
        if self.public_key is None or self.private_key is None:
            self.public_key, self.private_key = generate_rsa_keys(bits)


        # Encrypt

        if action == "encrypt":
            message = raw_input.strip()
            if message == "":
                return "Error: enter a message to encrypt."

            # Convert message into cipher numbers using the public key
            cipher = rsa_encrypt_message(message, self.public_key)

            # Return a readable output string for UI
            return (
                "RSA ENCRYPTION\n"
                f"Generated/Used Public Key (e,n): {self.public_key}\n"
                f"Generated/Used Private Key (d,n): {self.private_key}\n\n"
                "Cipher (copy this for decrypt):\n"
                + ", ".join(str(x) for x in cipher)
            )


        # Decrypt

        if action == "decrypt":
            raw = raw_input.strip()
            if raw == "":
                return "Error: paste cipher numbers separated by commas."

            # Convert comma-separated cipher text into a list of integers
            try:
                parts = [p.strip() for p in raw.split(",")]
                cipher_list = [int(p) for p in parts if p != ""]
            except:
                return "Error: cipher must be comma-separated integers."

            # Decrypt cipher numbers back into plain text using private key
            plain = rsa_decrypt_message(cipher_list, self.private_key)

            return (
                "RSA DECRYPTION\n"
                f"Generated/Used Private Key (d,n): {self.private_key}\n\n"
                "Plain Text:\n"
                + plain
            )

        # If action is not encrypt/decrypt
        return "Error: unknown RSA action."


class Fibonacci(BaseAlgorithm):
    """
    Fibonacci algorithm strategy.

    Input:
    - an integer n

    Output:
    - Fibonacci(n)
    """

    def __init__(self):
        super().__init__("Fibonacci")

    def run(self, raw_input, options):
        """
        Runs the Fibonacci algorithm.

        raw_input should be an integer string, e.g. "7".
        """
        raw = raw_input.strip()
        if raw == "":
            return "Error: enter an integer (e.g. 7)."

        # Convert input into an integer
        try:
            n = int(raw)
        except:
            return "Error: input must be an integer."

        # Call fibonacci() function (implemented elsewhere)
        try:
            value = fibonacci(n)
        except Exception as e:
            return "Error: " + str(e)

        return f"Fibonacci({n}) = {value}"


class BubbleSort(BaseAlgorithm):
    """
    Bubble Sort algorithm strategy.

    Input:
    - comma-separated list of integers

    Options:
    - order: "Ascending" or "Descending"
    """

    def __init__(self):
        super().__init__("BubbleSort")

    def run(self, raw_input, options):
        """
        Runs bubble sort based on the chosen order.
        """
        raw = raw_input.strip()
        if raw == "":
            return "Error: enter numbers separated by commas (e.g. 5,2,9,1)."

        # Parse comma-separated list into integers
        try:
            parts = [p.strip() for p in raw.split(",")]
            nums = [int(p) for p in parts if p != ""]
        except:
            return "Error: input must be a comma-separated list of integers."

        # Determine sort direction
        order = options.get("order", "Ascending")
        descending = (order == "Descending")

        # Call the actual bubble_sort() function (implemented elsewhere)
        sorted_nums = bubble_sort(nums, descending=descending)

        return "Sorted: " + ", ".join(str(n) for n in sorted_nums)


class SelectionSort(BaseAlgorithm):
    """
    Selection Sort algorithm strategy.
    Works like BubbleSort, but calls selection_sort().
    """

    def __init__(self):
        super().__init__("SelectionSort")

    def run(self, raw_input, options):
        raw = raw_input.strip()
        if raw == "":
            return "Error: enter numbers separated by commas (e.g. 5,2,9,1)."

        try:
            parts = [p.strip() for p in raw.split(",")]
            nums = [int(p) for p in parts if p != ""]
        except:
            return "Error: input must be a comma-separated list of integers."

        order = options.get("order", "Ascending")
        descending = (order == "Descending")

        sorted_nums = selection_sort(nums, descending=descending)
        return "Sorted: " + ", ".join(str(n) for n in sorted_nums)


class MergeSort(BaseAlgorithm):
    """
    Merge Sort algorithm strategy.
    Calls merge_sort() with ascending/descending option.
    """

    def __init__(self):
        super().__init__("MergeSort")

    def run(self, raw_input, options):
        raw = raw_input.strip()
        if raw == "":
            return "Error: enter numbers separated by commas (e.g. 5,2,9,1)."

        # Parse comma-separated list of ints
        try:
            parts = [p.strip() for p in raw.split(",")]
            nums = [int(p) for p in parts if p != ""]
        except:
            return "Error: input must be a comma-separated list of integers."

        order = options.get("order", "Ascending")

        # Make it case-insensitive just in case ("descending" vs "Descending")
        descending = (order.lower() == "descending")

        sorted_nums = merge_sort(nums, descending=descending)
        return "Sorted: " + ", ".join(str(n) for n in sorted_nums)


class ShuffleDeck(BaseAlgorithm):
    """
    Shuffle Deck algorithm strategy.

    This algorithm does NOT require input from the user.
    It simply generates and shuffles a deck of cards.
    """

    def __init__(self):
        super().__init__("ShuffleDeck", requires_input=False)

    def run(self, raw_input, options):
        """
        Runs deck shuffle and returns the shuffled deck as text.
        """
        deck = shuffle_deck()
        return "Shuffled Deck:\n" + ", ".join(deck)


class Factorial(BaseAlgorithm):
    """
    Factorial algorithm strategy.

    Input:
    - integer n

    Output:
    - Factorial(n)
    """

    def __init__(self):
        super().__init__("Factorial")

    def run(self, raw_input, options):
        raw = raw_input.strip()
        if raw == "":
            return "Error: enter an integer (e.g. 5)."

        # Convert input to integer
        try:
            n = int(raw)
        except:
            return "Error: input must be an integer."

        # Call factorial() function (implemented elsewhere)
        try:
            ans = factorial(n)
        except Exception as e:
            return "Error: " + str(e)

        return f"Factorial({n}) = {ans}"


class SearchStats(BaseAlgorithm):
    """
    Statistics algorithm strategy.

    Input:
    - comma-separated list of numbers

    Output:
    - returns a dictionary of statistics so the UI can show multiple values
      (e.g. largest, smallest, median, mode, quartiles)
    """

    def __init__(self):
        super().__init__("SearchStats")

    def run(self, raw_input, options):
        raw = raw_input.strip()
        if raw == "":
            return "Error: enter numbers separated by commas (e.g. 5, 2, 9, 1)."

        # Convert comma-separated string into list of integers
        try:
            parts = [p.strip() for p in raw.split(",")]
            nums = [int(p) for p in parts if p != ""]
        except:
            return "Error: input must be a comma-separated list of numbers."

        # Compute statistics using helper function
        try:
            stats = compute_statistics(nums)
        except Exception as e:
            return "Error: " + str(e)

        # Return dict so UI can fill multiple boxes
        return stats


class PalindromeDP(BaseAlgorithm):
    """
    Palindromic Substring Counter algorithm strategy (DP approach).

    Input:
    - text string

    Output:
    - dictionary with:
        {
          "found": preview_text,
          "count": total_count
        }
    """

    def __init__(self):
        super().__init__("PalindromeDP")

    def run(self, raw_input, options):
        text = raw_input.strip()

        # If input is empty, return empty results
        if text == "":
            return {"found": "", "count": 0}

        # palindromic_substrings() should return:
        # - found: list of palindrome substrings
        # - count: total number found
        found, count = palindromic_substrings(text)

        # Keep output short so it fits nicely in the UI
        preview = ", ".join(found[:10])
        if len(found) > 10:
            preview += f" ... (+{len(found)-10} more)"

        return {"found": preview, "count": count}



# Factory (Factory Method pattern)

class AlgorithmCreator:
    """
    Factory class that creates algorithm objects based on a name.

    This follows the Factory Method pattern:
    - You give it a string name (e.g. "RSA")
    - It returns the correct algorithm object (e.g. RSA())
    """

    def create(self, name):
        """
        Creates and returns an algorithm instance based on name.

        Raises:
        - ValueError if the algorithm name is unknown.
        """
        name = name.strip()

        if name == "RSA":
            return RSA()
        if name == "Fibonacci":
            return Fibonacci()
        if name == "BubbleSort":
            return BubbleSort()
        if name == "SelectionSort":
            return SelectionSort()
        if name == "MergeSort":
            return MergeSort()
        if name == "ShuffleDeck":
            return ShuffleDeck()
        if name == "Factorial":
            return Factorial()
        if name == "SearchStats":
            return SearchStats()
        if name == "PalindromeDP":
            return PalindromeDP()

        raise ValueError("Unknown algorithm name: " + name)


# Facade (Facade pattern)

class AlgorithmManager:
    """
    Facade class that the UI talks to.

    The UI does NOT need to know:
    - which class implements which algorithm
    - how timing/history is handled

    The UI simply does:
        manager.setAlgorithm("RSA")
        output, run_result = manager.execute(user_input, options)
    """

    def __init__(self):
        """
        Sets up:
        - creator: factory used to build algorithm objects
        - current_algorithm: the selected algorithm object
        - history: list of RunResult objects for performance tracking
        """
        self.creator = AlgorithmCreator()
        self.current_algorithm = None
        self.history = []

    def setAlgorithm(self, name):
        """
        Selects an algorithm by name (creates the object using the factory).
        """
        self.current_algorithm = self.creator.create(name)

    def execute(self, raw_input, options=None):
        """
        Runs the currently selected algorithm and records performance.

        Parameters:
        - raw_input (str): input from UI
        - options (dict): extra settings, like sort order or RSA mode

        Returns:
        - (output, result)
          output: algorithm output (string or dict)
          result: RunResult object (timing + metadata)
        """
        if options is None:
            options = {}

        # If no algorithm selected, return a friendly message
        if self.current_algorithm is None:
            return "No algorithm selected.", None

        # If algorithm doesn't need input (ShuffleDeck), ignore the input box
        if not self.current_algorithm.requires_input:
            raw_input = ""

        # Start timing
        start = time.perf_counter()

        # Run the algorithm
        output = self.current_algorithm.run(raw_input, options)

        # End timing
        end = time.perf_counter()

        # Store results in RunResult dataclass
        result = RunResult()
        result.algorithm_name = self.current_algorithm.name
        result.output = output
        result.time_taken = end - start
        result.size = len(raw_input)

        # Save to history so we can view performance later
        self.history.append(result)

        return output, result
