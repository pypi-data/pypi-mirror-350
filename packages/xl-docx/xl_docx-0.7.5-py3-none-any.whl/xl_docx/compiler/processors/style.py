from xl_docx.compiler.processors.base import BaseProcessor
import re
from lxml import etree
from cssselect import GenericTranslator


class StyleProcessor(BaseProcessor):
    """处理样式相关的XML标签"""
    def __init__(self):
        self.styles = {}
        
    def compile(self, xml: str) -> str:
        xml = self._parse_styles(xml)
        xml = self._apply_styles(xml)
        return xml
        
    def _parse_styles(self, xml: str) -> str:
        def process_style_match(match):
            style_content = match.group(1)
            rules = [rule.strip() for rule in style_content.split('}') if rule.strip()]
            for rule in rules:
                if '{' in rule:
                    selector, styles = rule.split('{')
                    selector = selector.strip()
                    styles = ''.join([style.strip() for style in styles.strip().split('\n')])
                    self.styles[selector] = styles
            return ''
            
        return self._process_tag(xml, r'<style>(.*?)</style>', process_style_match)

    def _apply_styles(self, xml: str) -> str:
        xml = re.sub(r'<\?xml[^>]*\?>', '', xml)
        
        template_tags = []
        def replace_template_tag(match):
            tag = match.group(0)
            template_tags.append(tag)
            return f"<!--TEMPLATE_TAG_{len(template_tags)-1}-->"
            
        xml = re.sub(r'{%.*?%}', replace_template_tag, xml)
        
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            root = etree.fromstring(xml.encode(), parser)
            translator = GenericTranslator()
            
            for selector, style_str in self.styles.items():
                xpath_expr = translator.css_to_xpath(selector)
                matched_elements = root.xpath(xpath_expr)
                
                for elem in matched_elements:
                    current_style = elem.get('style', '')
                    if current_style:
                        current_styles = self._parse_style_str(current_style)
                        new_styles = self._parse_style_str(style_str)
                        current_styles.update(new_styles)
                        merged_style = self._build_style_str(current_styles)
                        elem.set('style', merged_style)
                    else:
                        elem.set('style', style_str)
            
            result = etree.tostring(root, method='html', encoding='unicode')
            
            for i, tag in enumerate(template_tags):
                result = result.replace(f"<!--TEMPLATE_TAG_{i}-->", tag)
                
            return result
            
        except etree.XMLSyntaxError as e:
            raise e