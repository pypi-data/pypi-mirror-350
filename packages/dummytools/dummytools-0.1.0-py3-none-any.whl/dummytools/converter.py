def decimal_to_binary(number: int) -> str:
    """
    Convert a decimal number to binary.

    Args:
        number (int): The decimal number to convert.

    Returns:
        str: The binary representation of the decimal number.
    """
    if not isinstance(number, int):
        raise TypeError("Input must be an integer")
    if number < 0:
        raise ValueError("Number must be non-negative")
    return bin(number)[2:]  # Remove the '0b' prefix


def binary_to_decimal(binary: str) -> int:
    """
    Convert a binary number (as a string) to decimal.

    Args:
        binary (str): The binary number to convert.

    Returns:
        int: The decimal representation of the binary number.
    """
    if not isinstance(binary, str):
        raise TypeError("Input must be a string of binary digits")
    if not all(bit in "01" for bit in binary):
        raise ValueError("Invalid binary number")
    return int(binary, 2)
