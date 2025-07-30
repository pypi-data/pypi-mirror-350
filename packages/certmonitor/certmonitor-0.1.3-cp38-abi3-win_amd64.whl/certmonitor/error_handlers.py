# error_handlers.py


class ErrorHandler:
    """
    Class for handling errors in a flexible manner.
    """

    @staticmethod
    def handle_error(error_type: str, message: str, host: str, port: int) -> dict:
        """
        Handles errors encountered during certificate retrieval.

        Args:
            error_type (str): The type of error.
            message (str): The error message.
            host (str): The host where the error occurred.
            port (int): The port where the error occurred.

        Returns:
            dict: A dictionary containing the error details.
        """
        return {
            "error": error_type,
            "message": message,
            "host": host,
            "port": port,
        }
