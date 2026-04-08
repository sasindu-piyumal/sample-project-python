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
        n = len(s)
        for i in range(n // 2):
            if s[i] != s[n - 1 - i]:
                return False
        return True