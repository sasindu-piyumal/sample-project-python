import logging
import os
from llm_benchmark.algorithms.primes import Primes
from llm_benchmark.algorithms.sort import Sort
from llm_benchmark.control.double import DoubleForLoop
from llm_benchmark.control.single import SingleForLoop
from llm_benchmark.generator.gen_list import GenList
from llm_benchmark.sql.query import SqlQuery
from llm_benchmark.datastructures.dslist import DsList
from llm_benchmark.strings.strops import StrOps

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Create logs directory if it doesn't exist
LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR, exist_ok=True)

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
LOG_DATEFORMAT = "%Y-%m-%d %H:%M:%S"

# Initialize root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Remove any existing handlers to avoid duplicate logs
logger.handlers.clear()

# Configure FileHandler
file_handler = logging.FileHandler(os.path.join(LOGS_DIR, "main.log"))
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATEFORMAT)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Configure StreamHandler (console output)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATEFORMAT)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Log initialization message
logger.info("Logging infrastructure initialized")


def single():
    print("SingleForLoop")
    print("-------------")

    print(f"sum_range(10): {SingleForLoop.sum_range(10)}")
    print(f"max_list([1, 2, 3]): {SingleForLoop.max_list([1, 2, 3])}")
    print(f"sum_modulus(100, 3): {SingleForLoop.sum_modulus(100, 3)}")
    print()


def double():
    print("DoubleForLoop")
    print("-------------")

    print(f"sum_square(10): {DoubleForLoop.sum_square(10)}")
    print(f"sum_triangle(10): {DoubleForLoop.sum_triangle(10)}")
    print(
        f"count_pairs(random_list(30, 10)): {DoubleForLoop.count_pairs(GenList.random_list(30, 10))}"
    )
    print(
        "count_duplicates(10, 10)",
        DoubleForLoop.count_duplicates(
            GenList.random_list(10, 2), GenList.random_list(10, 2)
        ),
    )
    print(
        f"sum_matrix(random_matrix(10, 10)): {DoubleForLoop.sum_matrix(GenList.random_matrix(10, 10))}"
    )
    print()


def sql():
    print("SQL")
    print("---")

    print(f"query_album('Presence'): {SqlQuery.query_album('Presence')}")
    print(f"query_album('Roundabout'): {SqlQuery.query_album('Roundabout')}")
    print()

    print("join_albums()")
    albums = SqlQuery.join_albums()
    if albums:
        print(albums[0])
    print()

    print("top_invoices()")
    print(SqlQuery.top_invoices())
    print()

def primes():
    print("Primes")
    print("------")

    print(f"is_prime(1700): {Primes.is_prime_ineff(1700)}")
    print(f"sum_primes(210): {Primes.sum_primes(210)}")
    print(f"prime_factors(840): {Primes.prime_factors(840)}")
    print()

def sort():
    print("Sort")
    print("----")

    v = [5, 3, 2, 1, 4]
    print(f"sort_list({v}): ", end="")
    Sort.sort_list(v)
    print(v)

    v = [5, 3, 2, 1, 4]
    print(f"dutch_flag_partition({v}, 3): ", end="")
    Sort.dutch_flag_partition(v, 3)
    print(v)

    v = [5, 3, 2, 1, 4]
    print(f"max_n({v}, 3): {Sort.max_n(v, 3)}")
    print()


def dslist():
    print("DsList")
    print("----")

    test_list = [1, 2, 3, 4, 5]
    print("Original list:", test_list)

    modified_list = DsList.modify_list(test_list)
    print("Modified list:", modified_list)

    search_result = DsList.search_list(test_list, 3)
    print("Search result for 3:", search_result)

    sorted_list = DsList.sort_list(test_list)
    print("Sorted list:", sorted_list)

    reversed_list = DsList.reverse_list(test_list)
    print("Reversed list:", reversed_list)

    rotated_list = DsList.rotate_list(test_list, 2)
    print("Rotated list by 2 positions:", rotated_list)

    merged_list = DsList.merge_lists(test_list, [6, 7, 8])
    print("Merged list with [6, 7, 8]:", merged_list)

def strops():
    print("Strops")
    print("----")

    test_str = "racecar"
    print("Original string:", test_str)

    reversed_str = StrOps.str_reverse(test_str)
    print("Reversed string:", reversed_str)

    is_palindrome = StrOps.palindrome(test_str)
    print("Is palindrome:", is_palindrome)


def main():
    single()
    double()
    sql()
    primes()
    sort()
    dslist()
    strops()


if __name__ == "__main__":
    main()
