from xl_docx.compiler.processors.base import BaseProcessor
import re


class DirectiveProcessor(BaseProcessor):
    """处理Vue指令相关的XML标签"""
    @classmethod
    def compile(cls, xml: str) -> str:
        xml = cls._process_v_if(xml)
        xml = cls._process_v_for(xml)
        return xml
        
    @classmethod
    def _process_v_if(cls, xml: str) -> str:
        def process_if(match):
            tag_name, condition, remaining_attrs = match.groups()
            close_tag_pattern = f'</\s*{tag_name}\s*>'
            close_match = re.search(close_tag_pattern, xml[match.end():])
            if close_match:
                content_between = xml[match.end():match.end() + close_match.start()]
                return f'{{% if {condition} %}}<{tag_name}{remaining_attrs}>{content_between}</{tag_name}>{{% endif %}}'
            return match.group(0)
            
        return cls._process_tag(xml, r'<([^>]*)\s+v-if="([^"]*)"([^>]*)>', process_if)

    @classmethod
    def _process_v_for(cls, xml: str) -> str:
        def process_for(match):
            tag_name, loop_expr, remaining_attrs = match.groups()
            item, items = loop_expr.split(' in ')
            item = item.strip()
            items = items.strip()
            
            close_tag_pattern = f'</\s*{tag_name}\s*>'
            close_match = re.search(close_tag_pattern, xml[match.end():])
            if close_match:
                content_between = xml[match.end():match.end() + close_match.start()]
                return f'{{% for {item} in {items} %}}<{tag_name}{remaining_attrs}>{content_between}</{tag_name}>{{% endfor %}}'
            return match.group(0)
            
        return cls._process_tag(xml, r'<([^>]*)\s+v-for="([^"]*)"([^>]*)>', process_for)

    @classmethod
    def decompile2222222222222222222222(cls, xml: str) -> str:
        """将Jinja2模板转换回Vue指令"""
        xml = cls._decompile_v_if(xml)
        xml = cls._decompile_v_for(xml)
        return xml

    @classmethod
    def _decompile_v_if(cls, xml: str) -> str:
        def process_if(match):
            condition, tag_content = match.groups()
            # 提取标签名和属性
            tag_match = re.match(r'<([^\s>]+)([^>]*)>(.*)</\1>', tag_content)
            if tag_match:
                tag_name, attrs, content = tag_match.groups()
                return f'<{tag_name} v-if="{condition}"{attrs}>{content}</{tag_name}>'
            return match.group(0)

        return cls._process_tag(xml, r'{%\s*if\s+([^%]+)\s*%}(.*?){%\s*endif\s*%}', process_if)

    @classmethod
    def _decompile_v_for(cls, xml: str) -> str:
        def process_for(match):
            loop_expr, tag_content = match.groups()
            # 提取标签名和属性
            tag_match = re.match(r'<([^\s>]+)([^>]*)>(.*)</\1>', tag_content)
            if tag_match:
                tag_name, attrs, content = tag_match.groups()
                item, items = loop_expr.split(' in ')
                return f'<{tag_name} v-for="{item.strip()} in {items.strip()}"{attrs}>{content}</{tag_name}>'
            return match.group(0)

        return cls._process_tag(xml, r'{%\s*for\s+([^%]+)\s*%}(.*?){%\s*endfor\s*%}', process_for)
