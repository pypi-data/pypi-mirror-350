import re

def extract_xml_content(text, xml_tag):
    result = ''
    pattern = rf'^<{xml_tag}>$\n*([\D\d\s]+?)\n*^<\/{xml_tag}>$'
    match = re.search(pattern, text, re.MULTILINE)
    if match:
        result = match.group(1)
    if not result:
        return ''
    return result