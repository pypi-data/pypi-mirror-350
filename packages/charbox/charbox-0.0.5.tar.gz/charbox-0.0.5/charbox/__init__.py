from .transformer.transformer import CharBox
from .transformer.transformer import Name, HairColor, EyeColor

def init(show_credits: bool = True) -> None:
    """
    Initializes the CharBox library.
    """
    CharBox.init(show_credits=show_credits)

__all__ = ["init", "Name", "HairColor", "EyeColor"]