from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDFS
import xml.etree.ElementTree as ET
import re
import sys
from bs4 import BeautifulSoup
import requests
import pandas as pd

def change_node_value(srurl, d_translate):
    if srurl not in d_translate:
        l1 = srurl.split("|")
        html = l1[0]+"%7c" + l1[1]
        r = requests.get(html)
        soup = BeautifulSoup(r.content, 'html.parser')
        viaf_id = soup.findAll("title")[0].text
        viaf_link = "http://viaf.org/viaf/" + viaf_id
        d_translate[srurl] = viaf_link
        return viaf_link, d_translate
    else:
        viaf_link = d_translate[srurl]
        return viaf_link, d_translate

def return_child_num(node):
    return len(node.getchildren())


def parse_bf(root, d_translate):
    if return_child_num(root) == 0:
        return d_translate
    else:
        for child in root:
            if child.tag == "{http://id.loc.gov/ontologies/bibframe/}identifiedBy":
                for grandchild in child:
                    if grandchild.tag == "{http://id.loc.gov/ontologies/bibframe/}Identifier":
                        for aid in grandchild:
                            if aid.attrib:
                                pro_id = (aid.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'])
                                if pro_id.startswith("http://viaf.org/viaf/sourceID/"):
                                    v_link, d_translate = change_node_value(pro_id, d_translate)
                                    aid.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'] = v_link
            else:
                parse_bf(child,  d_translate)


def viaf_check(inputfn,outputfn):
    tree1 = ET.parse(inputfn)
    root1 = tree1.getroot()
    d_translate = {}
    d = parse_bf(root1, d_translate)
    tree.write(outputfn)
    return

if __name__ == "__main__":
    viaf_check(sys.argv[1], sys.argv[2])