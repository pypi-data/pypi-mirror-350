from .deck import SVGNode, Deck
import xml.etree.ElementTree as ET
from os.path import join, dirname
import subprocess
from importlib.resources import files


ET.register_namespace("","http://www.w3.org/2000/svg")


identifier = 400000000

def gen_id() -> int :
    global identifier
    identifier += 1
    return identifier

def svg_from_string(string : str) -> ET.Element:
    return ET.fromstring(string)

def svg_strip_svg_tag(root : ET.Element) -> ET.Element:

        print("ROOT TAG", root.tag)
        if root.tag == "{http://www.w3.org/2000/svg}svg":
            children = root.findall("./*")
            group = ET.Element("g")

            for c in children:
                group.append(c)

            return group
        else : 
            return root
            



class SVGFile(SVGNode):

    def __init__(self, path : str):
        """Loads SVG tree from an svg file. Path is relative to software invokation."""
        self.path = path

    def value(self, npath : str) -> ET.Element:

        svgtree = ET.parse(self.path)
        root = svgtree.getroot()
        return svg_strip_svg_tag(root)  


def find_first_of(string : str, targets : list[str]) -> tuple[int, str]:
    """finds the first occurrence of any targets in string
    in case two target overlap, the one with lowest index is selected first. In case of equal indices, the longest is selected.
    returns the index and the string if found, otherwise len(string) as index and an empty string"""
    # we look for first and then str 
    found = ""
    index = len(string)

    for t in targets :
        idx = string.find(t)
        if idx >= 0 and (idx < index or (idx == index and len(found) < len(t))):
            found = t 
            index = idx 
    return (index, found)

def replace_all(string : str, pairs : dict[str, str]) -> str:
    """given a set of pair (target : value) and a string S,
    replaces each occurrence of each target in S with its associated value.
    values are excluded from parsing, meaning : 
    replace_all("abbbc", {"a":"b", "b":"d"})
    returns "bdddc" and not "ddddc" : the b created from a is NOT considered a target.

    should multiple target overlap, the LOWEST INDEX one and then the LONGEST one is chosen : 

    replace_all("aabc", {"a":"d", "aa":"e"})
    returns "ebc" and not "dbc", as "aa" is longer than "a".


    replace_all("aabc", {"aa":"d", "abc":"e"})
    returns "dbc" and not "abc", as "aa" has a lower index than "abc".
    """

    done = ""
    remaining = string
    
    targets = list(pairs.keys())

    while len(remaining) > 0:
        #find occurrence
        #CUT the 
        index, found = find_first_of(remaining, targets)


        if index >= len(remaining):
            done += remaining
            remaining = ""
        else :
            done += remaining[:index]
            done += pairs[found] 
            remaining = remaining[len(found) + index:]
    return done



def list_ids(svg : ET.Element) -> set[str]:

    res : set[str] = set()

    the_id = svg.get("id", "")

    if the_id != "" : 
        res.add(the_id)

    for e in svg.findall("./*"):
        res |= list_ids(e)
        
    return res


def prefixed_ids(svg : ET.Element, prefix : str) -> ET.Element:
    
    ids = list_ids(svg)

    pairs : dict[str, str] = {}

    for i in ids : 
        pairs[i] = prefix + i

    return svg_from_string(replace_all(ET.tostring(svg, encoding="unicode"), pairs))


def uids(svg : ET.Element) -> ET.Element:

    strid = str(gen_id())
    return prefixed_ids(svg, strid + "-")

class StrSub(SVGNode):
    
    def __init__(self, svg : SVGNode, subs : dict[str, str]):
        """
        Converts the SVG tree into a string and perform simulataneous string substitutions, replacing keys from subs by their associated values.
        To have more details on how substitution behaves, see replace_all function's doc.
        """
        self.svg = svg 
        self.subs = subs

    def value(self, npath : list[str]) -> ET.Element:

        svg = ET.tostring(self.svg.value(npath + ["StrSub::svg"]), encoding="unicode")

        svg = replace_all(svg, self.subs)

        return ET.fromstring(svg) 

def Transform(SVGNode):

    def __init__(self, svg : SVGNode, transform : str):
        """
        Applies the given svg transformation string onto svg by embedding in a group : 
        <g transform=TRANSFORM>
        svg
        </g>
        """
        self.svg = svg 
        self.transform = transform

    def value(self, npath : list[str]) -> ET.Element:

        group = ET.Element("g")

        group.set("transform", transform)
        
        group.append(svg.value(npath + ["Transform::svg"]))

        return group

def Group(SVGNode):

    def __init__(self, svgs : list[SVGNode]):
        """
        groups several SVG trees together into a svg g element.
        Each tree has its internal ids rewritten to be unique.
        """
        self.svgs = svgs
    
    def value(self, npath : list[str]) -> ET.Element:
        group = ET.Element("g")
        
        for i, s in enumerate(svgs) : 
            group.append(uids(s.value(npath + [f"Group[{i}]"])))

        return group



def render_html_to_pdf(html_in, pdf_out) -> None :
    subprocess.run(["chromium"] 
        + ["--headless"]
        + ["----virtual-time-budget=15000"]
        + [f"--print-to-pdf={pdf_out}"]
        + [html_in]
    )
 
def convert_pdf_to_svg(pdf_in, svg_out) -> None :
    subprocess.run(["pdftocairo", "-svg", pdf_in, svg_out])
    

def style_to_dict(style : str) -> dict[str, str]:
    styles = style.split(";")
    
    res : dict[str, str] = {}

    for s in styles:
        split = s.split(":")
        if len(split) == 2:
            res[split[0]] = split[1]
    return res


def rect_get_stroke_color(rect : ET.Element, default : str) -> str :

    color = rect.get("stroke", default)

    style = style_to_dict(rect.get("style", ""))

    if "stroke" in style :
        color = style["stroke"]

    return color



def create_text_fitting_rect(rect : ET.Element, text : str, style : str) -> ET.Element:
    #get rect attributes
    width = rect.get("width")
    height = rect.get("height")

    rx = float(rect.get("rx", "0"))
    ry = float(rect.get("ry", "0"))
    fsize = str(float(height) / (max(rx, ry) if rx != 0 or ry != 0 else 1.0))
    color = rect_get_stroke_color(rect, "#000000")

    # Build template


    with files("deckbro").joinpath("text_rect_template.html").open("r") as f: 
        html = f.read()

    html = replace_all(html, {
        "120pt": width + "pt",
        "60pt" : height + "pt",
        "#1e1e1e" : color,
        "TEXT" : text,
        "20pt" : fsize + "pt",
        "STYLE" : style
    })

    tmp_filebase = join(Deck.instance().config.render.outdir, "tmp_create_text_in_rect")
    with open(tmp_filebase + ".html", "w") as f :
        f.write(html)

    render_html_to_pdf(tmp_filebase + ".html", tmp_filebase + ".pdf")
   
    convert_pdf_to_svg(tmp_filebase + ".pdf", tmp_filebase + ".svg")

    svgtree = ET.parse(tmp_filebase + ".svg")
    root = svgtree.getroot()
    return svg_strip_svg_tag(root)  


def replace_rects_by_text(svg : ET.Element, rect_id : str, text :  str, style : str):
    
    children = svg.findall("./*")

    new_elems : list[ET.Element] = []

    for c in children :
        if c.get("id", "") == rect_id:
            x = c.get("x", 0)
            y = c.get("y", 0)

            group = ET.Element("g")
            group.set("transform", f"translate({x}, {y})")

            group.append(create_text_fitting_rect(c, text, style))

            new_elems.append(uids(group))
        else : 
            replace_rects_by_text(c, rect_id, text, style)
            new_elems.append(c)
        svg.remove(c)

    for ne in new_elems:
        svg.append(ne)


class RFText(SVGNode) : 
    
    def __init__(self, svg : SVGNode, subs : dict[str, str | tuple[str, str]]):
        """
        Substitutes each rectangle in svg identified by a key from subs by the associated str value, ensuring the text 
        is fitting inside the rectangle by shrinking the font if needed. Rectangles are parametrized as follows :
        - Width and height of rectangle define boundaries. Rounded corners are ignored and rectangle is considered not rounded.
        - stroke color defines font color of the text
        - initial (max) font size is defined as height/max(rx, ry). Defaults to height if neither rx nor ry is defined.
        
        if the associated value is a tuple(str, str), the fist string is the text, while the second is a CSS set of rules that 
        will be inline-added to the div used for text rendering. It can be used to change font family or justify text for example.
        ("some text", "text-align:justify;")
        Those rules will take precedence over the rules set by the rectangle geometry. It is not recommended to
        add display-ruling rules.
        """ 
        self.svg = svg
        self.subs = subs 

    def value(self, npath : list[str]) -> ET.Element:

        print("SVG RFText")
        v = self.svg.value(npath + [f"RFText::svg"])

        for s in self.subs :
            print("APPLYING SUB", s)
            sub = self.subs[s]


            replace_rects_by_text(v, s,  sub if type(sub) is str else sub[0], "" if type(sub) is str else sub[1])

        return v