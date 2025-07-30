import os
import locale
import gettext
from pathlib import Path

def get_system_language():
    """获取系统语言"""
    try:
        # 获取系统语言环境
        lang, _ = locale.getdefaultlocale()
        if lang:
            # 返回完整的语言代码（如 'zh_CN'）
            return lang
    except:
        pass
    return 'en_US'

def setup_i18n():
    """设置国际化"""
    # 获取包所在目录
    package_dir = Path(__file__).parent
    locales_dir = package_dir / 'locales'
    
    # 获取系统语言
    lang = get_system_language()
    
    # 如果系统语言不是中文，则使用英文
    if not lang.startswith('zh'):
        lang = 'en_US'
    
    # 先不开 i18n，使用英文
    lang = 'en_US'
    
    # 设置翻译
    translation = gettext.translation(
        'moffetthub',
        localedir=locales_dir,
        languages=[lang],
        fallback=True
    )
    
    # 安装翻译函数
    translation.install()
    
    return translation.gettext

# 创建翻译函数
def _(text):
    """直接返回英文文本，不进行翻译"""
    return text

_ = setup_i18n() 