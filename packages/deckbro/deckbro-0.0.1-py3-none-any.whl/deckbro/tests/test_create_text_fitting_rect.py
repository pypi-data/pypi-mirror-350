import pytest 

from deckbro.svg import create_text_fitting_rect, SVGFile
from deckbro.deck import Deck 
from os.path import dirname, join, exists
from os import mkdir
from shutil import rmtree
import xml.etree.ElementTree as ET

@pytest.fixture()
def artifacts_dir() -> str:
    artifacts_dir = join(dirname(__file__), "artifacts")

    Deck.instance().config.render.outdir = artifacts_dir

    if not exists(artifacts_dir):
        mkdir(artifacts_dir)

    return artifacts_dir

@pytest.fixture
def target_rect() -> ET.Element :

    rect = ET.Element("rect")
    rect.set("width", "200")
    rect.set("height", "100")
    rect.set("stroke", "#099099")
    rect.set("rx", "44")

    return rect

def test_create_text_fitting_rect_already_fitting(artifacts_dir, target_rect):

    text = create_text_fitting_rect(target_rect, "SOME TEXT")


    textstr = ET.tostring(text, encoding="unicode")
    
    with open(join(artifacts_dir, "test_create_text_fitting_rect_already_fitting.svg"), "w") as f:
        f.write(textstr)

    with open(join(dirname(__file__), "expected/create_text_fitting_rect/already_fitting.svg")) as f:
        expected = f.read()

    assert textstr == expected


def test_create_text_fitting_rect_shrink(artifacts_dir, target_rect):

    lorem_ipsum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam nibh. Mauris ac mauris sed pede pellentesque fermentum. Maecenas adipiscing ante non diam sodales hendrerit."""

    text = create_text_fitting_rect(target_rect, lorem_ipsum)

    textstr = ET.tostring(text, encoding="unicode")
    
    with open(join(artifacts_dir, "test_create_text_fitting_rect_shrink.svg"), "w") as f:
        f.write(textstr)

    with open(join(dirname(__file__), "expected/create_text_fitting_rect/shrink.svg")) as f:
        expected = f.read()

    assert textstr == expected