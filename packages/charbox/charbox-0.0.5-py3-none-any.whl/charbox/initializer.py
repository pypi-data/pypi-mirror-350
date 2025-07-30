import altcolor
from .config import can_use
from .name import generator as name
from .haircolor import generator as haircolor
from .eyecolor import generator as eyecolor

altcolor.init(show_credits=False)

def init(show_credits: bool = True) -> None:
    """
    Initializes the CharBox library.
    """
    
    global can_use
    check1 = name.init()
    check2 = haircolor.init()
    check3 = eyecolor.init()
    
    if show_credits:
        altcolor.cPrint(color="BLUE", text="Thanks for using 'CharBox' by Taireru LLC! Check out our other products at https://tairerullc.vercel.app/pages/products")
    
    if check1 and check2 and check3:
        can_use = True
    
    if not can_use:
        raise ModuleNotFoundError("No module named 'charbox'")