class BColors:
    """
    ANSI escape sequences for colored text in terminal.
    Usage:
        print(bcolors.WARNING + "This is a warning message" + bcolors.end)
        print(bcolors.FAIL + "This is an error message" + bcolors.end)
        print(bcolors.RESET + "This is normal text" + bcolors.end)
        print(bcolors.BOLD + "This is bold text" + bcolors.end)
        print(bcolors.UNDERLINE + "This is underlined text" + bcolors.end)
    """
    # ANSI escape sequences for colored text in terminal
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR
    END = '\033[0m' #RESET COLOR
    BOLD = '\033[1m' #BOLD
    UNDERLINE = '\033[4m' #UNDERLINE
    UNDERLINE_OFF = '\033[24m' #UNDERLINE OFF
    BOLD_OFF = '\033[22m' #BOLD OFF
    REVERSE = '\033[7m' #REVERSE
    REVERSE_OFF = '\033[27m' #REVERSE OFF
    STRIKETHROUGH = '\033[9m' #STRIKETHROUGH
    STRIKETHROUGH_OFF = '\033[29m' #STRIKETHROUGH OFF

    # Foreground colors
    BLACK = '\033[30m' #BLACK
    WHITE = '\033[37m' #WHITE
    RED = '\033[31m' #RED
    GREEN = '\033[32m' #GREEN
    YELLOW = '\033[33m' #YELLOW
    BLUE = '\033[34m' #BLUE
    PURPLE = '\033[35m' #PURPLE
    LIGHTBLUE = '\033[36m' #LIGHT BLUE
    CYAN = '\033[36m' #CYAN
    MAGENTA = '\033[35m' #MAGENTA
    
    # Dark colors
    DARKGRAY = '\033[90m' #DARK GRAY
    DARKRED = '\033[91m' #DARK RED
    DARKGREEN = '\033[92m' #DARK GREEN
    DARKYELLOW = '\033[93m' #DARK YELLOW
    DARKBLUE = '\033[94m' #DARK BLUE
    DARKPURPLE = '\033[95m' #DARK PURPLE
    DARKCYAN = '\033[96m' #DARK CYAN
    DARKMAGENTA = '\033[95m' #DARK MAGENTA
    DARKWHITE = '\033[97m' #DARK WHITE
    DARKBLACK = '\033[90m' #DARK BLACK

    # Light colors
    LIGHTGRAY = '\033[37m' #LIGHT GRAY
    LIGHTRED = '\033[91m' #LIGHT RED
    LIGHTGREEN = '\033[92m' #LIGHT GREEN
    LIGHTYELLOW = '\033[93m' #LIGHT YELLOW
    LIGHTBLUE = '\033[94m' #LIGHT BLUE
    LIGHTPURPLE = '\033[95m' #LIGHT PURPLE
    LIGHTCYAN = '\033[96m' #LIGHT CYAN
    LIGHTMAGENTA = '\033[95m' #LIGHT MAGENTA
    LIGHTWHITE = '\033[97m' #LIGHT WHITE
    LIGHTBLACK = '\033[90m' #LIGHT BLACK
    LIGHTWHITE = '\033[97m' #LIGHT WHITE
    LIGHTGRAY = '\033[37m' #LIGHT GRAY


class Color:
    def __init__(self, name, hex_value):
        self.name = name
        self.hex_value = hex_value

    def __repr__(self):
        return f"Color(name={self.name}, hex_value={self.hex_value})"
    

class ColorPalette:
    def __init__(self, name, colors):
        self.name = name
        self.colors = colors

    def __repr__(self):
        return f"ColorPalette(name={self.name}, colors={self.colors})"
    

class ColorGradient:
    def __init__(self, start_color, end_color, steps):
        self.start_color = start_color
        self.end_color = end_color
        self.steps = steps

    def __repr__(self):
        return f"ColorGradient(start_color={self.start_color}, end_color={self.end_color}, steps={self.steps})"