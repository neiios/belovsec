def bool_with_color(value):
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"
    if value:
        return f"{BOLD}{GREEN}True{RESET}"
    else:
        return f"{BOLD}{RED}False{RESET}"
