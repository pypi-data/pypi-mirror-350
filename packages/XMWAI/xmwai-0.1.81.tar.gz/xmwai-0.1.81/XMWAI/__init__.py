from .core import story, photo, reply, poem, get_access_token  # 从子模块导入函数到顶层
from .magic_core import birthday  # 从子模块导入函数到顶层
from .bomb_core import bomb  # 从子模块导入函数到顶层
from .idiom_core import idiom,searchIdiom,get_json_path  # 从子模块导入函数到顶层

__all__ = ["story", "photo", "reply", "poem", "get_access_token", 'birthday', 'bomb', "idiom", "searchIdiom","get_json_path"]  # 可选：明确导出的内容
