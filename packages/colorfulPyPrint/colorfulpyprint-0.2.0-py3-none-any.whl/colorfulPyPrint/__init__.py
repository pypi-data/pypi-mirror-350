import sys

try:
    import colorama
    # only init if stdout is a tty (protects non-interactive uses)
    if sys.stdout.isatty():
        colorama.init()
except ImportError:
    pass  # colorama not installed, ANSI codes will be raw
