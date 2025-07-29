import sys


class Console:
    """
    A utility class for writing messages to standard output and standard error streams.

    This class provides static methods to write messages to `sys.stdout` and `sys.stderr`
    with customizable end characters. It serves as a simple abstraction for console output
    operations, ensuring consistent handling of messages in command-line applications.
    """

    @staticmethod
    def write_stdout(message: str = "", end: str = "\n"):
        """
        Writes a message to the standard output stream (sys.stdout).

        :param message: str - The message to write. Defaults to an empty string.
        :param end: str - The string to append after the message. Defaults to a newline ('\n').
        :return: None - No return value; output is written to sys.stdout.
        """
        sys.stdout.write(f"{message}{end}")

    @staticmethod
    def write_stderr(message: str = "", end: str = "\n"):
        """
        Writes a message to the standard error stream (sys.stderr).

        :param message: str - The message to write. Defaults to an empty string.
        :param end: str - The string to append after the message. Defaults to a newline ('\n').
        :return: None - No return value; output is written to sys.stderr.
        """
        sys.stderr.write(f"{message}{end}")
