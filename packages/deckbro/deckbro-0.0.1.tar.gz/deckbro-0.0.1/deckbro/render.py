
import xml.etree.ElementTree as ET
from .deck import SVGNode, Config, Deck, Card
from copy import deepcopy
from os.path import join, dirname, isdir
from os import mkdir
import shutil
from typing import Sequence
import subprocess
from .svg import svg_strip_svg_tag, svg_from_string


def create_svg(width : float, height : float, unit : str, bg_color: str) -> ET.Element:
    svgstr = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>

<svg
    width="{width}{unit}"
    height="{height}{unit}"
    viewBox="0 0 {width} {height}"
    version="1.1"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:svg="http://www.w3.org/2000/svg">
<rect x="0" y="0" width="{width}" height="{height}" fill="{bg_color}"/>

</svg>
"""
    return svg_from_string(svgstr)


def render_card_face(config : Config, cid : str, node : SVGNode) -> ET.Element:

    svg = create_svg(
        config.cards.width,
        config.cards.height,
        config.unit,
        config.cards.bg_color
        )

    svg.append(node.value([cid]))
    
    return svg 


def render_card(config : Config, card : Card) -> tuple[ET.Element, ET.Element]:
    #renders a c
    # Create an empty svg card for the file
    
    return (
        render_card_face(config, card.identifier + (" (front)"), card.front),
        render_card_face(config, card.identifier + (" (back)"), card.back)
    )

def svg_strip_root(root : ET.Element) -> list[ET.Element]:
    children = root.findall("./*")
    return children



def svg_insert_elements_as_group(svg : ET.Element, elements : list[ET.Element], transform : str | None = None) -> None:

    group = ET.Element("g")

    if transform is not None : 
        group.set("transform", transform)
    
    for e in elements : 
        group.append(e)

    svg.append(group)


def svg_transform(svg : ET.Element, transform : str | None):
    
    group = ET.Element("g")

    if transform is not None : 
        group.set("transform", transform)
    
    group.append(svg)
    return group
    

def svg_insert_svg(svg : ET.Element, other : ET.Element, transform : str | None):
    
    stripped = svg_strip_root(other)
    svg_insert_elements_as_group(svg, stripped, transform)


def render_sheets(d : Deck, cards : Sequence[ET.Element | None], 
    sheet_template : str,
    columns :int,
    rows : int,
    cwidth : float,
    cheight : float,
    vgap : float, 
    hgap : float,
    ) -> list[ET.Element]:
    """Create card sheets
    cards : a list of card filenames
    sheet_template : a string representing the sheet format to use.
    columns, rows : dimension of the grid to place cards on
    cwidth, cheight : dimensions of the card that goes on the grid. In the unit of the sheet.
    vgap, hgap : vertical and horizontal gaps to separate cards on the grid. In the unit of the sheet.

    Grid is automatically centered on sheets.
    """

    grid_width = columns * cwidth + hgap * (columns - 1)
    grid_height = rows * cheight + vgap *  (rows - 1)

    assert grid_width < d.config.sheets.width
    assert grid_height < d.config.sheets.height

    start_x_offset = (d.config.sheets.width - grid_width) / 2
    start_y_offset = (d.config.sheets.height - grid_height) / 2

    work_cards = list(cards)
    
    sheets : list[ET.Element] = []

    cards_per_sheet = columns * rows

    while len(work_cards) > 0:
        sheet = svg_from_string(sheet_template)

        # for each row
        for c_index in range(min(len(work_cards) , cards_per_sheet)):
            card = work_cards[c_index]

            if card is None:
                #We ignore empty cards
                continue
            assert card is not None, "This should never be triggered btw, this is just to please the type checker."

            print("building card", card)
            print("len card", len(card))
            #row and column of the card on sheet grid
            c = c_index % columns
            r = c_index // columns

            translate_x = start_x_offset + c * (cwidth + hgap)
            translate_y = start_y_offset + r * (cheight + vgap) 

            sheet.append(svg_transform(svg_strip_svg_tag(card) , f"translate({translate_x} {translate_y})"))
                
        #append current sheet
        sheets.append(sheet)
        #remove processed cards
        work_cards = work_cards[cards_per_sheet:]

    return sheets


def reorder_backs[T](blist : Sequence[T], cols : int) -> list[T | None]:
    """Returns a list of backs where they are correctly ordered for generating long-side flip backsheet for printing.
    it can also possibly insert blank ("") backs if offset is needed.
    """
    wlist = list(blist)
    rbacks : list[T | None] = []

    while len(wlist) > cols : 
        rbacks += list(reversed(wlist[:cols]))
        wlist = wlist[cols:]
    
    if len(wlist) > 0:
        rbacks += [None] * (cols - len(wlist)) + list(reversed(wlist))

    return rbacks

def padded[T](l : Sequence[T | None], cards_per_sheet : int) -> list[T | None]:
    """Returns a copy of l padded at the end so it len(l) % cards_per_sheet == 0"""
    if len(l) % cards_per_sheet == 0:
        return list(l)
    else :
        return list(l) + [None] * (cards_per_sheet - len(l) % cards_per_sheet)

def interleave_front_back[T](clist : Sequence[T | None], blist : Sequence[T | None], cards_per_sheet : int) -> list[T | None]:
    """Given a clist of card to assemble and a blist of their backs, as well as the number
    of cards per sheet, returns a list in which cards and backs are interleaved and padded so that 
    sheets are correctly matched for twoside printing."""

    wclist = padded(clist, cards_per_sheet)
    wblist = padded(blist, cards_per_sheet)

    rlist : list[T | None] = []

    while len(wclist) > 0:
        rlist += wclist[:cards_per_sheet]
        rlist += wblist[:cards_per_sheet]

        wclist = wclist[cards_per_sheet:]
        wblist = wblist[cards_per_sheet:]

    return rlist


def export_page_pdf(svgfile : str, pdffile : str):

    subprocess.run(["inkscape", f"--export-filename={pdffile}", "--export-area-page", svgfile])


def unite_pdf_files(files : list[str], destfile : str):
    
    subprocess.run(["pdfunite"] + files + [destfile])




def render() -> None:


    # Render all cards 
    d = Deck.instance()

    if isdir(d.config.render.outdir):
        shutil.rmtree(d.config.render.outdir)
    mkdir(d.config.render.outdir)

    # Build all sheets
    fronts : list[ET.Element | None] = []
    backs : list[ET.Element] = []

    #Rendering cards
    for c in d.cards.values() :
        front, back = render_card(d.config, c)
        if d.config.render.cards :
            with open(join(d.config.render.outdir,  f"gen_{c.identifier}.svg"), "w") as f:
                f.write(ET.tostring(front, encoding="unicode"))
            
            with open(join(d.config.render.outdir, f"gen_{c.identifier}.back.svg"), "w") as f:
                f.write(ET.tostring(back, encoding="unicode"))
        
        for _ in range(c.count) : 
            fronts.append(front)
            backs.append(back)

    #Rendering sheets
    sheet_template = str(ET.tostring(
        create_svg(
            d.config.sheets.width,
            d.config.sheets.height,
            d.config.unit,
            d.config.sheets.bg_color
        ), encoding="unicode"
    ))

    blist = reorder_backs(backs, d.config.sheets.cols)

    allcards = interleave_front_back(fronts, blist, d.config.sheets.cols * d.config.sheets.rows)
    if d.config.render.sheets or d.config.render.pdf : 
        sheets = render_sheets(d,
            allcards, 
            sheet_template,
            d.config.sheets.cols,
            d.config.sheets.rows,
            d.config.cards.width,
            d.config.cards.height,
            d.config.sheets.gap,
            d.config.sheets.gap
        )

        target_dir = d.config.render.outdir
        
        pdf_files : list[str] = []

        for i, sh in enumerate(sheets) : 
            svg_file = join(target_dir, f"gen_sheet_{str(i)}.svg")
            pdf_file = join(target_dir, f"gen_sheet_{str(i)}.pdf")
        
            with open(svg_file, "w") as f:
                f.write(ET.tostring(sh, encoding="unicode"))
            
            if d.config.render.pdf:
                export_page_pdf(svg_file, pdf_file)
                pdf_files.append(pdf_file)

        if len(pdf_files) > 0:
            unite_pdf_files(pdf_files, join(target_dir, "gen_sheets.pdf"))
    