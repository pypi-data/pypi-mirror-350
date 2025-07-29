import re
from typing import Literal, Optional
from termcolor import colored


def get_full_class_name(obj) -> str:
    """Returns the full class name including the module for an object."""
    module = obj.__class__.__module__
    return obj.__class__.__name__ if module is None or module == str.__class__.__module__ \
        else f'{module}.{obj.__class__.__name__}'


text_color_options = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'grey']
on_color_options = ['on_red', 'on_green', 'on_yellow', 'on_blue', 'on_magenta', 'on_cyan', 'on_white', 'on_grey']

# Combine inline options for text_color and on_color combinations
inline_options = text_color_options + [
    f"{a}_on_{b.split('_')[1]}" for a in text_color_options for b in on_color_options if a != b.split('_')[1]
]


def print_custom(
        msg: str,
        text_color: Optional[Literal['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'grey']] = None,
        on_color: Optional[Literal[
            'on_red', 'on_green', 'on_yellow', 'on_blue', 'on_magenta', 'on_cyan', 'on_white', 'on_grey']] = None,
        end: str = '\n',
        bold: bool = False,
        underline: bool = False
) -> None:
    """
    Prints a custom message with a combo of multiple text and background colors, and attributes like bold and underline.

    E.g. print_custom("<cyan:Hello!> My name is <bold_ul_red_on_grey:John>. "
                      "My <bold_green:birthday> is on <bold_magenta_on_grey:Feb 29>!",
                      text_color='grey', on_color='on_yellow')

        'Hello!' is in green
        'John' will be bold, underlined & red on grey
        'birthday' will be bold green
        'Feb 29' will be bold, & magenta on grey

        Everything else will be grey because text_color='grey' with a yellow background because on_color='yellow'
        (Note: text_color and on_color defaults to your terminal colors if None)

        IMPORTANT: bold_ and ul_ always need to be in front of colors
    """
    attrs = {'bold'} if bold else set()
    if underline:
        attrs.add('underline')

    # REGEX Advice
    # by default, the . (dot) in a regex does not match \n. It matches any character except a newline character.
    # If you want to include newline characters in the .* pattern, you can use the re.DOTALL
    # Split message by inline tags
    msg_list = re.split(r'<(.*?)>', str(msg), flags=re.DOTALL)

    for m in msg_list:
        m_split = m.split(':', maxsplit=1)
        if m_split[0].replace('bold_', '').replace('ul_', '') in inline_options:
            # Extract inline attributes like bold and underline
            inline_attrs = set(attrs)
            if 'bold_' in m_split[0]:
                inline_attrs.add('bold')
            if 'ul_' in m_split[0]:
                inline_attrs.add('underline')

            # Extract inline colors
            temp = m_split[0].replace('bold_', '').replace('ul_', '').split('_on_')
            m_color = temp[0]
            m_on_color = f'on_{temp[1]}' if len(temp) > 1 else on_color
            print(colored(m_split[1], color=m_color, on_color=m_on_color, attrs=attrs | inline_attrs), end="")
        else:
            print(colored(m, color=text_color, on_color=on_color, attrs=attrs), end="")
    print("", end=end)


def input_custom(
        msg: str,
        text_color: Optional[Literal['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'grey']] = None,
        on_color: Optional[Literal[
            'on_red', 'on_green', 'on_yellow', 'on_blue', 'on_magenta', 'on_cyan', 'on_white', 'on_grey']] = None,
        bold: bool = False,
        underline: bool = False
) -> str:
    """Prints a prompt with custom color and formatting and returns the user's input."""
    print_custom(msg.strip(), text_color=text_color, on_color=on_color, bold=bold, underline=underline, end="")
    return input(" ")


def print_error(msg: str, end: str = '\n', bold: Optional[bool] = None, underline: Optional[bool] = None) -> None:
    """Prints an error message in red with an X symbol."""
    print_custom(f'\u274C  {msg}', text_color='red', on_color='on_grey', end=end, bold=bold, underline=underline)


def print_exception(exception_obj: Exception, end: str = '\n', bold: Optional[bool] = None,
                    underline: Optional[bool] = None) -> None:
    """Prints an exception message in red."""
    print_custom(f'\u274C  {get_full_class_name(exception_obj)}: {exception_obj}',
                 text_color='red', on_color='on_grey', end=end, bold=bold, underline=underline)


def print_warning(msg: str, end: str = '\n', bold: Optional[bool] = None, underline: Optional[bool] = None) -> None:
    """Prints a warning message in yellow with a warning symbol."""
    print_custom(f'\u26A0  {msg}', text_color='yellow', on_color='on_grey', end=end, bold=bold, underline=underline)


def print_red(msg, end='\n', bold=None, underline=None):
    print_custom(msg, text_color='red', end=end, bold=bold, underline=underline)


def print_green(msg, end='\n', bold=None, underline=None):
    print_custom(msg, text_color='green', end=end, bold=bold, underline=underline)


def print_yellow(msg, end='\n', bold=None, underline=None):
    print_custom(msg, text_color='yellow', end=end, bold=bold, underline=underline)


def print_blue(msg, end='\n', bold=None, underline=None):
    print_custom(msg, text_color='blue', end=end, bold=bold, underline=underline)


def print_magenta(msg, end='\n', bold=None, underline=None):
    print_custom(msg, text_color='magenta', end=end, bold=bold, underline=underline)


def print_cyan(msg, end='\n', bold=None, underline=None):
    print_custom(msg, text_color='cyan', end=end, bold=bold, underline=underline)


def print_white(msg, end='\n', bold=None, underline=None):
    print_custom(msg, text_color='white', end=end, bold=bold, underline=underline)


def print_grey(msg, end='\n', bold=None, underline=None):
    print_custom(msg, text_color='grey', end=end, bold=bold, underline=underline)


def print_info(msg, end='\n'):
    """Prints a message in cyan with a thunderbolt symbol."""
    print_cyan(f'\u26A1 {msg}', end=end, bold=True)


def print_done(msg, end='\n'):
    """Prints a message in green with a checkmark symbol."""
    print_green(f'\u2705  {msg}', end=end, bold=True)


def print_cmd(msg, end='\n'):
    print_magenta(f'Running cmd \u2B9A ', end="", bold=True)
    print_cyan(f'{msg}', end=end, bold=True)


# Colored Inputs
# input_red is not allowed as it is used for print_error
def input_red(msg):
    return input_custom(msg, text_color='red', on_color='on_grey')


def input_green(msg):
    return input_custom(msg, text_color='green', on_color='on_grey')


def input_yellow(msg):
    return input_custom(msg, text_color='yellow', on_color='on_grey')


def input_blue(msg):
    return input_custom(msg, text_color='blue', on_color='on_grey')


def input_magenta(msg):
    return input_custom(msg, text_color='magenta', on_color='on_grey')


def input_cyan(msg):
    return input_custom(msg, text_color='cyan', on_color='on_grey')


def input_white(msg):
    return input_custom(msg, text_color='white', on_color='on_grey')


def input_grey(msg):
    return input_custom(msg, text_color='grey', on_color='on_white')


# Multiline input
def multiline_input(prompt="", end_signal="q!"):
    print_custom(f"<bold_cyan:{prompt}>\n"
                 f"<yellow:Enter multi-line text (to finish, in an empty line type '><bold_magenta:{end_signal}>"
                 f"<yellow:' and hit enter)>:")
    lines = []
    while True:
        line = input()
        if line.strip() == end_signal:
            break
        lines.append(line)
    return "\n".join(lines)
