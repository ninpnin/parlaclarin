"""
Parla Clarin generation
"""
import pandas as pd
import progressbar, copy
from lxml import etree
from pyparlaclarin.utils import infer_metadata

# Generate parla clarin header
def parlaclarin_header(title="Untitled", authority="N/A", source_title="Untitled",
    correction_summary="No correction of source texts was performed.", edition=None):
    # TODO: assert that there are no extra keys


    #teiHeader = etree.Element("teiHeader")
    teiHeader = root.find("//.teiHeader")
    
    # fileDesc
    #fileDesc = etree.SubElement(teiHeader, "fileDesc")
    
    #titleStmt = etree.SubElement(fileDesc, "titleStmt")
    #titleElem = etree.SubElement(titleStmt, "title")
    #titleElem.text = title
    
    #if edition is not None:
    #    editionStmt = etree.SubElement(fileDesc, "editionStmt")
    #    editionElem = etree.SubElement(editionStmt, "edition")
    #    editionElem.text = edition

    #extent = etree.SubElement(fileDesc, "extent")
    #publicationStmt = etree.SubElement(fileDesc, "publicationStmt")
    #authorityElem = etree.SubElement(publicationStmt, "authority")
    #authorityElem.text = authority
    
    #sourceDesc = etree.SubElement(fileDesc, "sourceDesc")
    #sourceBibl = etree.SubElement(sourceDesc, "bibl")
    #sourceTitle = etree.SubElement(sourceBibl, "title")
    #sourceTitle.text = source_title
    
    # encodingDesc
    #encodingDesc = etree.SubElement(teiHeader, "encodingDesc")
    #editorialDecl = etree.SubElement(encodingDesc, "editorialDecl")
    #correctionElem = etree.SubElement(editorialDecl, "correction")
    #correctionP = etree.SubElement(correctionElem, "p")
    #correctionP.text = correction_summary
    
    return teiHeader

def parlaclarin_preface(title="Untitled", date="2020-01-01"):
    front = etree.Element("front")
    preface = etree.SubElement(front, "div", type="preface")
    etree.SubElement(preface, "head").text = title
    if type(date) == list:
        dates = date
        for date in dates:
            etree.SubElement(preface, "docDate", when=date).text = date
    else:
        etree.SubElement(preface, "docDate", when=date).text = date

    return front

def parlaclarin_body():
    return etree.Element("div")

def create_u(text="", attrib=None):
    u = etree.Element("u")
    u.text = text
    if attrib is not None:
        for key, value in attrib.items():
            u.attrib[key] = value
    return u

def create_note(text="", attrib=None):
    u = etree.Element("note")
    u.text = text
    if attrib is not None:
        for key, value in attrib.items():
            u.attrib[key] = value
    return u

def create_tei(document_header, preface, body):
    """
    Create a Parla-Clarin TEI element from a list of segments.

    Args:
        txts: a list of lists of strings, corresponds to content blocks and paragraphs, respectively.
        metadata: Metadata of the parliamentary session
    """    
    tei = etree.Element("TEI")
    tei.append(document_header)
    
    text = etree.SubElement(tei, "text")
    text.append(preface)
    
    body_wrapper = etree.SubElement(text, "body")
    body_wrapper.append(body)
    
    return tei

def create_parlaclarin(global_header, teis):
    if type(teis) != list:
        tei = teis
        return create_parlaclarin(global_header, [tei])
    
    teiCorpus = etree.Element("teiCorpus", xmlns="http://www.tei-c.org/ns/1.0")
    teiCorpus.append(global_header)
    
    for tei in teis:
        teiCorpus.append(tei)
    
    teiCorpusTree = etree.ElementTree(teiCorpus)
    
    for xml_element in teiCorpusTree.iter():
        content = xml_element.xpath('normalize-space()')

        if not content and len(xml_element.attrib) == 0:
            xml_element.getparent().remove(xml_element)
            
    s = etree.tostring(teiCorpusTree, pretty_print=True, encoding="utf-8", xml_declaration=True).decode("utf-8")
    return s
