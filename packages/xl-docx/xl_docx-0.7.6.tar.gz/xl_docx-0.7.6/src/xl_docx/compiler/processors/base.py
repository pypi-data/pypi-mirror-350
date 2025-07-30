import re


class BaseProcessor:
    """XML处理器基类"""
    @classmethod
    def compile(cls, xml):
        raise NotImplementedError

    @staticmethod
    def retrieve(dict_, keys):
        """字典解构赋值
        params = {'a': 1, 'b': 2}
        a, b = get(params, ['a', 'b'])
        a, c = get(params, ['a', 'c'])
        """
        tmp = ()
        for key in keys:
            tmp += (dict_.get(key),)
        return tmp

    @classmethod
    def _process_tag(cls, xml, pattern, process_func):
        """通用标签处理方法"""
        return re.sub(pattern, process_func, xml, flags=re.DOTALL)

    @classmethod
    def _extract_attrs(cls, attrs_str, attr_names):
        """提取属性值"""
        result = []
        for name in attr_names:
            match = re.search(f'{name}="([^"]*)"', attrs_str)
            result.append(match.group(1) if match else None)
        return tuple(result)
    
    @classmethod
    def _get_value(cls, pattern, xml):
        match = re.search(pattern, xml)
        return match.group(1) if match else None
    
    @classmethod
    def _build_props(cls, props, indent=''):
        """构建属性字符串"""
        if not props:
            return ''
        return f'\n{indent}' + f'\n{indent}'.join(props) + f'\n{indent}'
    
    @classmethod
    def _parse_style_str(cls, style_str):
        """解析样式字符串为字典
        例如: "font-size:12px;color:red" -> {"font-size": "12px", "color": "red"}
        """
        if not style_str:
            return {}
        return dict(pair.split(':') for pair in style_str.split(';') if pair.strip())
    
    @classmethod
    def _build_style_str(cls, styles):
        """将样式字典转换为字符串
        例如: {"font-size": "12px", "color": "red"} -> "font-size:12px;color:red"
        """
        if not styles:
            return ''
        return ';'.join(f"{k}:{v}" for k, v in styles.items())

    @classmethod
    def _build_attr_str(cls, attrs):
        """将属性字典转换为字符串
        例如: {"font-size": "12px", "color": "red"} -> "font-size:12px;color:red"
        """
        if not attrs:
            return ''
        return ' '.join(f"{k}='{v}'" for k, v in attrs.items())