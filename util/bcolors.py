class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def header(text: str) -> str:
        return f"{BColors.HEADER}{text}{BColors.ENDC}"

    @staticmethod
    def okblue(text: str) -> str:
        return f"{BColors.OKBLUE}{text}{BColors.ENDC}"

    @staticmethod
    def okcyan(text: str) -> str:
        return f"{BColors.OKCYAN}{text}{BColors.ENDC}"

    @staticmethod
    def okgreen(text: str) -> str:
        return f"{BColors.OKGREEN}{text}{BColors.ENDC}"

    @staticmethod
    def warning(text: str) -> str:
        return f"{BColors.WARNING}{text}{BColors.ENDC}"

    @staticmethod
    def fail(text: str) -> str:
        return f"{BColors.FAIL}{text}{BColors.ENDC}"

    @staticmethod
    def bold(text: str) -> str:
        return f"{BColors.BOLD}{text}{BColors.ENDC}"

    @staticmethod
    def underline(text: str) -> str:
        return f"{BColors.UNDERLINE}{text}{BColors.ENDC}"

    @staticmethod
    def color(text: str, color: str) -> str:
        return f"{color}{text}{BColors.ENDC}"

    @staticmethod
    def color_text(text: str, color: str) -> str:
        return f"{color}{text}{BColors.ENDC}"

    @staticmethod
    def color_text_bold(text: str, color: str) -> str:
        return f"{color}{BColors.BOLD}{text}{BColors.ENDC}"

    @staticmethod
    def color_text_underline(text: str, color: str) -> str:
        return f"{color}{BColors.UNDERLINE}{text}{BColors.ENDC}"

    @staticmethod
    def color_text_bold_underline(text: str, color: str) -> str:
        return f"{color}{BColors.BOLD}{BColors.UNDERLINE}{text}{BColors.ENDC}"
