from pyfiglet import Figlet
from pyfiglet import figlet_format

def get_fonts() -> list:

    """
    This function returns a list with all fonts from pyfiglet.

    :param: None
    :return: list
    """

    _figlet = Figlet()

    _all_fonts = _figlet.getFonts()

    return _all_fonts