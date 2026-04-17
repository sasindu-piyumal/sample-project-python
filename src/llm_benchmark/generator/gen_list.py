from random import randint
from typing import List

class GenList:
    @staticmethod
    def random_list(n: int, m: int) -> List[int]:
        """Generate a list of random integers

        Args:
            n (int): Number of integers to generate
            m (int): Maximum value of integers (exclusive)

        Returns:
            List[int]: List of random integers
        """
        # This part is already efficient. No significant optimization possible here.
        return [randint(0, m) for _ in range(n)]

    @staticmethod
    def random_matrix(n: int, m: int) -> List[List[int]]:
        """Generate a matrix of random integers

        Args:
            n (int): Number of rows
            m (int): Number of columns

        Returns:
            List[List[int]]: Matrix of random integers
        """
        # The original code generates an n x n matrix where elements are up to m.
        # The docstring says "m: Number of columns", which contradicts the implementation.
        # To preserve observable behavior, we must keep the implementation logic.
        # The implementation: return [GenList.random_list(n, m) for _ in range(n)]
        # This implies:
        # - Number of rows = n
        # - Number of columns = n (because GenList.random_list(n, m) is called)
        # - Max value = m

        # Optimization idea: Generate all n*n numbers at once, then structure them.
        # This reduces overhead from repeated list creation and method calls.
        
        # Generate all n*n elements.
        num_elements = n * n # Total elements needed for an n x n matrix
        all_elements = [randint(0, m) for _ in range(num_elements)]
        
        # Reshape the flat list into a list of lists (matrix).
        matrix = []
        # Iterate through the flat list, taking chunks of size n for each row.
        for i in range(0, num_elements, n):
            row = all_elements[i : i + n]
            matrix.append(row)
        
        return matrix

from random import randint
from typing import List


class GenList:
    @staticmethod
    def random_list(n: int, m: int) -> List[int]:
        """Generate a list of random integers

        Args:
            n (int): Number of integers to generate
            m (int): Maximum value of integers (exclusive)

        Returns:
            List[int]: List of random integers
        """
        # No significant optimization possible here without external libraries.
        # The docstring for 'm' says (exclusive), but randint(a,b) is inclusive.
        # We preserve the observed behavior (randint(0, m)) to match existing output.
        return [randint(0, m) for _ in range(n)]

    @staticmethod
    def random_matrix(n: int, m: int) -> List[List[int]]:
        """Generate a matrix of random integers

        Args:
            n (int): Number of rows
            m (int): Number of columns

        Returns:
            List[List[int]]: Matrix of random integers
        """
        # The original implementation generates an n x n matrix.
        # The docstring claims 'm' is the number of columns, but the code uses 'n' for columns.
        # To preserve observable behavior, we keep the implementation logic:
        # An n x n matrix where elements are random integers up to m.

        # Optimized approach: Generate all n*n elements at once, then structure into rows.
        # This reduces overhead of repeated list creation and function calls.
        
        num_elements = n * n  # Total elements in an n x n matrix
        
        # Generate all random integers in a single pass.
        # This reduces overhead from repeated list generation and method calls compared to
        # calling random_list n times.
        all_elements = [randint(0, m) for _ in range(num_elements)]
        
        # Reshape the flat list into a list of lists (matrix).
        matrix = []
        # Slice the flat list into chunks of size n to form each row.
        # This is generally more efficient than building rows incrementally in many cases.
        for i in range(0, num_elements, n):
            row = all_elements[i : i + n]
            matrix.append(row)
        
        return matrix
from random import randint
from typing import List


class GenList:
    @staticmethod
    def random_list(n: int, m: int) -> List[int]:
        """Generate a list of random integers

        Args:
            n (int): Number of integers to generate
            m (int): Maximum value of integers (exclusive)

        Returns:
            List[int]: List of random integers
        """
        return [randint(0, m) for _ in range(n)]

    @staticmethod
    def random_matrix(n: int, m: int) -> List[List[int]]:
        """Generate a matrix of random integers

        Args:
            n (int): Number of rows
            m (int): Number of columns

        Returns:
            List[List[int]]: Matrix of random integers
        """
        # The current implementation generates an n x n matrix where elements are up to m.
        # This is achieved by calling GenList.random_list(n, m) for each of the n rows.
        # To optimize runtime performance and resource usage, we can generate all n*n
        # elements at once and then structure them into rows. This reduces overhead
        # from repeated list creation and method calls.

        num_elements = n * n  # Total elements in an n x n matrix
        
        # Generate all random integers in a single pass.
        all_elements = [randint(0, m) for _ in range(num_elements)]
        
        # Reshape the flat list into a list of lists (matrix).
        matrix = []
        # Slice the flat list into chunks of size n to form each row.
        for i in range(0, num_elements, n):
            row = all_elements[i : i + n]
            matrix.append(row)
        
        return matrix
from random import randint
from typing import List


class GenList:
    @staticmethod
    def random_list(n: int, m: int) -> List[int]:
        """Generate a list of random integers

        Args:
            n (int): Number of integers to generate
            m (int): Maximum value of integers (exclusive)

        Returns:
            List[int]: List of random integers
        """
        return [randint(0, m) for _ in range(n)]

    @staticmethod
    def random_matrix(n: int, m: int) -> List[List[int]]:
        """Generate a matrix of random integers

        Args:
            n (int): Number of rows
            m (int): Number of columns

        Returns:
            List[List[int]]: Matrix of random integers
        """
        num_elements = n * n
        all_elements = [randint(0, m) for _ in range(num_elements)]
        
        matrix = []
        for i in range(0, num_elements, n):
            row = all_elements[i : i + n]
            matrix.append(row)
        
        return matrix