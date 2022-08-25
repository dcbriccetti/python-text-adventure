from colorama import Fore


def colored(color: str, message: str) -> str:
    return color + message + Fore.RESET


def bright(message: str) -> str:
    return colored(Fore.LIGHTWHITE_EX, message)

