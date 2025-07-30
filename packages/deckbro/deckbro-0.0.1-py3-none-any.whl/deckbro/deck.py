import xml.etree.ElementTree as ET
from typing import Any, Type
from copy import deepcopy

ET.register_namespace("","http://www.w3.org/2000/svg")

class SVGNode:

    def __init__(self):
        pass

    def value(self, npath : list[str]) -> ET.Element:
        raise NotImplementedError()


class Card : 

    def __init__(self, identifier : str, front : SVGNode, back : SVGNode, count : int = 1):
        self.identifier = identifier 
        self.front = front 
        self.back = back 
        self.count = count

        d = Deck.instance()

        if identifier in d.cards:
            raise IdentifierError(f"Card identifier {identifier} is already taken by another card in deck.")

        d.cards[identifier] = self


class Config : 
    """This class holds configuration for the Deck. Only non-obvious members are documented.

    unit : the SVG unit string (like, "mm" or "px") in use accross ALL svg used for the deck.
    Will also be used when rendering to svgs and other formats where unit may matter.
    In config, sizes expressed in this selected unit.
    """

    class Sheets : 
        """
        rows : number of rows of cards per sheet
        cols : number of columns of cards per sheet 
        gap : spacing between each row/column.
        """
        def __init__(self):
            self.height : float = 297
            self.width : float = 210
            self.rows : int = 6 
            self.cols : int = 2
            self.gap : float = 0.5
            self.bg_color : str = "#FFFFFF"

    class Cards:
        def __init__(self):
            self.height : float = 48
            self.width : float = 96
            self.bg_color : str = "#FFFFFF"

    class Render:  
        """
        cards : if set to True, renders each card faces pair (front, back) as svg files named 
        "gen_CARD_IDENTIFIER.svg" and "gen_CARD_IDENTIFIER.back.svg" respectively.

        sheets : if set to True (or if pdf is set to True), renders svg sheets named gen_sheet_X.svg where X is the number of the sheet.
        if X is pair, then it is a sheet containing fronts only, the sheet X+1 contains corresponding backs organized for a 
        flip-long-side double-sided printing.

        pdf : if set to True, also sets sheets to True. In addition, uses Inkscape CLI to render each gen_sheet_X.svg file into a gen_sheet_X.pdf
        file. Then, uses pdfunite to unite all those pdf files, in order, into a gen_sheet.pdf file. This file can be fed in a printer using 
        flip-long-side double-sided printing.

        outdir : the directory where all generated files should go.
        """
        def __init__(self):
            self.cards : bool = True
            self.sheets : bool = True
            self.pdf : bool = True 
            self.outdir : str = "build"

    def __init__(self):
        self.unit : str = "mm"
        self.sheets : Config.Sheets = Config.Sheets()
        self.cards : Config.Cards = Config.Cards()
        self.render : Config.Render = Config.Render()

class Deck:
    """The main class of the library. Used to hold all cards, components etc data.
    Deck instance can -and should, unless you know what you are doing- be accessed through

    Deck.instance() static method.

    cards : a dict of cards, indexed on their identifier. 
        Unless you changed corresponding config, cards are auto registered into deck instance upon creation.
    components : a dict of components, indexed on their identifier
        Unless you changed corresponding config, components are auto registered into deck instance upon creation.
    aliases : see Component doc for explanations
    rewrite : see Component doc for explanations
    checkers : a list of Checkers to apply to deck when checking.
        Unless you changed corresponding config, checkers are auto registered into deck instance upon creation.
    """

    _instance : "Deck | None" = None 

    @staticmethod
    def instance() -> "Deck":
        if Deck._instance is None :
            Deck._instance = Deck()
        return Deck._instance

    def __init__(self):
        self.cards : dict[str, Card] = {}
        self.config : Config = Config()