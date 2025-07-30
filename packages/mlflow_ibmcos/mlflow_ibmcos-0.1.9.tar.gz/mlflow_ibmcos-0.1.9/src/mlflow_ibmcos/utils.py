from pydantic import validate_call


class Color:
    """
    Class to define color codes for terminal output.
    """

    RED_BOLD = "\x1b[1;31m"
    GREEN_BOLD = "\x1b[1;32m"
    YELLOW = "\x1b[0;33m"
    RESET = "\x1b[0m"


@validate_call
def print_colored_message(message: str, color: str) -> None:
    """
    Prints a message in the specified color.

    Args:
        message (str): The message to print.
        color (str): The color code for the message.
    """
    print(f"{color}{message}{Color.RESET}")
