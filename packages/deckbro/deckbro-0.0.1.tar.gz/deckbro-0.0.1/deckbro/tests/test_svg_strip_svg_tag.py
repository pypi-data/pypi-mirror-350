import xml.etree.ElementTree as ET
from deckbro.svg import svg_strip_svg_tag, svg_from_string




def test_svg_strip_tag_no_tag():
    svg =  """<rect width="48" height="48" rx="0" fill="#efefef"/>""" 
    
    res = ET.tostring(svg_strip_svg_tag(svg_from_string(svg)), encoding="unicode")
    expected = """<rect width="48" height="48" rx="0" fill="#efefef" />"""

    assert res == expected

def test_svg_strip_tag_tag():
    svg =  """<svg xmlns="http://www.w3.org/2000/svg" width="96" height="48" viewBox="0 0 96 48" fill="none">
<rect width="48" height="48" rx="0" fill="#efefef"/>
<rect width="48" height="48" x="48" fill="#fefefe"/>
</svg>""" 

    res = ET.tostring(svg_strip_svg_tag(svg_from_string(svg)), encoding="unicode")
    print("TEST")
    print(res)
    expected = """<g>
<rect width="48" height="48" rx="0" fill="#efefef"/>
<rect width="48" height="48" x="48" fill="#fefefe"/>
</g>""" 
    assert res == expected