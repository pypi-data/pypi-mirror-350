from .convert_pdf_to_instructions import convert_pdf_to_instructions
from ..html.convert_instructions_to_dict import convert_instructions_to_dict
from .mapping import pdf_base_mapping_dict
from selectolax.parser import HTMLParser
def pdf2dict(content,mapping_dict=None):
    instructions = convert_pdf_to_instructions(content)
    if mapping_dict is None:
        mapping_dict=pdf_base_mapping_dict
    dct = convert_instructions_to_dict(instructions, mapping_dict)
    return dct