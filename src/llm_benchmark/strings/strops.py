class StrOps:
    @staticmethod
    def str_reverse(s: str) -> str:
        """Reverse a string

        Args:
            s (str): String to reverse

        Returns:
            str: Reversed string
        """
        return s[::-1]

    @staticmethod
    def palindrome(s: str) -> bool:
        """Check if a string is a palindrome

        Args:
            s (str): String to check

        Returns:
            bool: True if the string is a palindrome, False otherwise
        """
        # Comparing the string with its reverse is generally more efficient
        # and Pythonic for this task. String slicing for reversal [::-1]
        # creates a new reversed string, and then a direct comparison is made.
        return s == s[::-1]