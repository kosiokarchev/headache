import os
import typing as tp

from lxml import etree as ET, html, objectify


class DoXML:
    def __init__(self, base_dir='xml'):
        self.base_dir = base_dir

        index = ET.parse(os.path.join(self.base_dir, 'index.xml'))
        transform = ET.XSLT(ET.parse(os.path.join(self.base_dir, 'combine.xslt')))
        schema = ET.XMLSchema(file=os.path.join(self.base_dir, 'compound.xsd'))

        self.doxml = objectify.fromstring(ET.tostring(transform(index)), parser=objectify.makeparser(schema=schema))

    def find_element_by_name(self, name: str, hasdocs=True) -> tp.Sequence[objectify.ObjectifiedElement]:
        return self.doxml.xpath(f'//*[name[text() = "{name}"]]' + ('[detaileddescription]' if hasdocs else ''))

    def format_docstring(self, el: objectify.ObjectifiedElement) -> tp.Optional[str]:
        try:
            return '\n'.join(html.fromstring(ET.tostring(para)).text_content() for para in el.para)
        except AttributeError:
            return None
        # return html.fromstring(ET.tostring(el)).text_content()

    def get_docs(self, name: str) -> tp.Optional[str]:
        return (self.format_docstring(els[0].detaileddescription)
                if (els := self.find_element_by_name(name)) else None)
