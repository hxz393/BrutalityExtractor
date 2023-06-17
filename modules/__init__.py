from modules.math_until import *
from modules.module_use import *
from modules.lang import *

# 定义配置路径、默认配置
CONFIG_PATH = Path('config/config.ini')
DEFAULT_CONFIG = {
    'DEFAULT': {
        'path_zip': '',
        'password': '',
        'parallel': '1',
        'no_warnning': '0',
        'is_delete': '0',
        'log_level': 'INFO',
        'log_size': '10',
        'log_count': '10',
        'is_extra': '0',
        'is_redundant': '0',
        'is_empty': '0',
        'xcl_dir': '',
        'xcl_file': '',
        'no_tooltip': '0',
        'mini_skin': '0',
        'theme': 'pulse',
        'lang': 'ENG',
        'alpha': '1.00'
    }
}
CP = configparser.ConfigParser()

# 如果配置文件存在，读取配置文件
if CONFIG_PATH.exists():
    CP = config_read(CONFIG_PATH)

# 检查是否存在 "main" section，如果不存在则添加
if not CP.has_section("main"):
    CP.add_section("main")

# 更新 "DEFAULT" section，不论是否已经存在。最后写入配置文件
CP.read_dict(DEFAULT_CONFIG)
with open(CONFIG_PATH, 'w') as configfile:
    CP.write(configfile)

# 直接配置获取值
path_zip_config = CP['main'].get('path_zip')
path_dest_config = CP['main'].get('path_dest')
password_config = CP['main'].get('password')
parallel_config = CP['main'].getint('paralle')
no_warnning_config = CP['main'].getint('no_warnning')
is_delete_config = CP['main'].getint('is_delet')
log_level_config = CP['main'].get('log_level')
log_size_config = CP['main'].getint('log_size')
log_count_config = CP['main'].getint('log_count')
is_extra_config = CP['main'].getint('is_extra')
is_redundant_config = CP['main'].getint('is_redundant')
is_empty_config = CP['main'].getint('is_empty')
xcl_dir_config = CP['main'].get('xcl_dir')
xcl_file_config = CP['main'].get('xcl_file')
no_tooltip_config = CP['main'].getint('no_tooltip')
mini_skin_config = CP['main'].getint('mini_skin')
theme_config = CP['main'].get('theme')
lang_config = CP['main'].get('lang')
alpha_config = CP['main'].getfloat('alpha')

# 图标
FONT_SIZE = 10 if mini_skin_config else 16
ICO_SIZE = 16 if mini_skin_config else 48
MAIN_ICO = 'AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAgBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUVFFwtLSxslTk4aRE1NGl9OThluTk4Zb05OGmFNTRhIUFAYKU5OEw0AAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAVVUAA01NHCRNTRlsS0sZtktLGOFLSxn0S0sZ/EtLGf5LSxn+S0sZ/EtLGPZMTBnkS0sZvU1NGXdNTRcrMzMzBQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUhIGxxMTBh8S0sY2UpKGftKShn/SkoZ/0pKGf9KShn/SkoZ/0pKGf9KShn/SkoZ/0pKGf9KShn/SUkZ/ElJGeBJSRmKTU0cJAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD8/AARJSRlFSEgYxEhIGPtISBj/SEgY/0hIGP9ISBj/SEgY/0hIGP9ISBj/SEgY/0hIGP9ISBj/SEgY/0hIGP9ISBj/SEgY/0dHGP1HRxjRSEgYVFVVKgYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABVVSoGRkYXYUhIGORbWy3/V1cp/0dHGP9GRhj/RkYX/0ZGF/9GRhf/SUkb/2BgM/96elL/hIRc/3Z2Tf9ZWSv/R0cY/0ZGF/9GRhf/RkYX/0ZGF/9GRhbsRkYYdExMGQoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPz8ABEVFF2NFRRfseXlR/97ez//Hx7H/UVEj/0REF/9ERBf/REQX/1hYLP+oqIv/5ubb//j49P/8/Pj/9vbx/9zczv+NjWn/Skod/0NDFv9DQxb/Q0MW/0REF/9LSx3zXV0weJ+ffwgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFCQhhJQUEW5lZWKv/W1sb//////9PTwv9OTiP/QUEW/0FBFv9ZWS//x8e0//z8+//7+/n/6+vj/+jo3//39/P///////X18P+Wlnb/REQZ/0REGf9paUL/p6eK/8zMuv/e3tHv9vbxX////wIAAAAAAAAAAAAAAAAAAAAAPT0XIT8/Fco/PxX/jY1s//v7+P/4+PT/hoZl/z8/Fv8+PhX/RkYc/7S0m//9/fz/7Ozk/5SUdP9dXTb/WFgx/35+W//c3M7////+/+3t5f92dlD/mJh5/+vr4//+/v7////////////+/v7b////MAAAAAAAAAAAAAAAADMzAAU+PhSHOzsU/EZGHv/Ly7n//////9HRwf9KSiL/PDwU/zw8FP9paUT/8PDq//r69v+NjW7/Pj4W/zs7FP87OxT/PDwU/21tSf/s7OT////+/+jo3f/39/P////+/+/v6f/Kyrj/srKc/76+qv7V1cWgsrKyCgAAAAAAAAAAPj4WLTo6E+A5ORP/W1s2/+zs5P/9/fz/lJR3/zk5E/85ORP/OTkT/5WVeP/+/v3/39/T/05OKf84OBP/ODgT/zg4E/84OBP/PDwW/6ioj//+/v3///////7+/v/V1cf/a2tJ/0FBG/85ORT/PT0X/0tLJe1HRx9AAAAAAAAAAAI3NxJ9NjYS/TY2Ev9wcE//+Pj1//X18P9nZ0X/NjYS/zY2Ev83NxP/rKyV///////GxrX/PDwY/zU1Ev81NRL/NTUS/zU1Ev81NRL/Z2dH//T08P//////5+fe/2FhQP81NRL/NTUS/zU1Ev81NRL/NDQR/jU1EpgzMwAFODgOEjMzEMUzMxH/MzMR/319YP/8/Pr/6urj/1NTMf8zMxH/MzMR/zQ0Ev+pqZL//////8vLvP88PBn/MzMR/zMzEf8yMhH/MjIR/zIyEf9lZUX/9fXw///////W1sr/QkIg/zIyEf8yMhH/MjIR/zIyEf8yMhH/MjIQ2DMzER4yMg8zMDAQ6zAwEP8wMBD/f39l//39/P/m5t7/S0ss/zAwEP8wMBD/MDAQ/4+Pdv/+/v3/5+fe/1FRMf8wMBD/MDAQ/zAwEP8vLxD/MDAQ/4uLcP/9/fz//////+/v6P9YWDn/Ly8Q/y8vEP8vLxD/Ly8Q/y8vEP8uLg/1MTERSDAwEVktLQ/6Li4P/y4uD/92dlr/+/v5/+rq4/9PTzD/Li4P/y0tD/8tLQ//ZGRG//T07//9/fv/np6H/zMzFP8tLQ//LS0P/y0tD/9BQSL/zc2/////////////+vr3/29vU/8tLQ//LCwP/ywsD/8sLA//LCwP/ywsD/4tLQ91LCwOeSsrDv4rKw7/KysO/2RkSP/39/P/8vLt/1paPf8rKw7/KysO/ysrDv85ORv/x8e3///////y8u3/i4ty/zs7Hf8xMRP/REQm/6mplf/7+/n/8/Ps//n59v/9/fz/gYFo/yoqDv8qKg7/KioO/yoqDv8qKg7/KioO/ysrD5gpKQ6MKSkO/ykpDv8pKQ7/Tk4y/+zs5f/6+vj/cnJY/ykpDv8pKQ7/KSkO/ykpDv9nZ03/7e3n///////39/T/0dHE/8DAr//a2s///Pz6//j49v+ioon/6Ojh/////v+Li3H/KCgN/ygoDf8oKA3/KCgN/ygoDf8oKA3/KSkNrCkpDo4nJw3/JycN/ycnDf84OB3/1NTJ/////v+cnIf/KCgO/ycnDf8mJg3/JiYN/ysrEf+Cgmr/7u7o///////////////////////7+/n/r6+e/1ZWOv/p6eL//v79/4iIb/8mJg3/JiYN/yYmDf8mJg3/JiYN/yYmDf8nJw2uJycNgSUlDP8lJQz/JSUM/ykpD/+qqpf//////83NwP80NBn/JSUM/yUlDP8lJQz/JSUM/yoqEP9jY0r/ubmp/+Dg1//l5d7/09PI/5KSff84OB7/UFA2/+/v6v/9/fz/e3tl/yUlDP8lJQz/JSUM/yUlDP8lJQz/JSUM/yYmDKElJQxmJCQM/CUlDP8lJQz/JCQM/25uVv/5+fb/8fHs/1tbQv8kJAz/JCQM/yQkDP8kJAz/JCQM/yUlDP8sLBP/PT0k/0FBKP81NRz/JycO/yQkDP9gYEf/9/fz//r6+P9ra1P/JCQM/yQkDP8kJAz/JCQM/yQkDP8kJAz/JiYNhCcnC0EkJAzzJCQM/yQkDP8kJAz/PT0k/9vb0f/+/v7/pqaU/ykpEP8kJAz/JCQM/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM/3p6Y//9/fv/8vLu/1ZWPf8kJAz/JCQM/yQkDP8kJAz/JCQM/yQkDPooKAtZIyMRHSQkC9ckJAz/JCQM/yQkDP8nJw7/l5eD//39/P/p6eL/UlI5/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM/yQkDP8lJQ3/n5+M///////h4dn/Pz8m/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM5icnCy0zMwAFJSUNnCQkDP8kJAz/JCQM/yQkDP9KSjD/4+Pa//7+/v+wsJ//Li4V/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM/y8vFv/Hx7n//////8HBs/8tLRP/JCQM/yQkDP8kJAz/JCQM/yQkDP8kJAy1KioVDAAAAAAmJg5IIyML8SQkDP8kJAz/JCQM/ycnDv+Ojnn/+/v5//X18f94eGH/JiYO/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM/yQkDP8kJAz/S0sy/+np4//+/v3/jY14/yUlDP8kJAz/JCQM/yQkDP8kJAz/IyMM+CQkDWEAAAAAAAAAACQkEg4lJQ2wJCQM/yQkDP8kJAz/JCQM/zk5H//Gxrj////+/+Pj2v9ZWUD/JSUN/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM/yYmDf+MjHb//f37/+3t5/9TUzr/JCQM/yQkDP8kJAz/JCQM/yQkDP8kJAzGKioKGAAAAAAAAAAAAAAAACcnC0EkJAzoJCQM/yQkDP8kJAz/JCQM/1VVPP/g4Nj////+/9XVyf9SUjj/JSUN/yQkDP8kJAz/JCQM/yQkDP8kJAz/RUUs/9vb0v////7/tram/y0tE/8kJAz/JCQM/yQkDP8kJAz/IyML8SYmC1cAAAABAAAAAAAAAAAAAAAAMzMABSUlDHwjIwz4JCQM/yQkDP8kJAz/JiYN/2pqUv/p6eL//v7+/9jYzv9mZk7/KysS/yQkDP8kJAz/JCQM/zo6IP+zs6P//f38/+3t5/9dXUT/JCQM/yQkDP8kJAz/JCQM/yQkDPslJQyUMzMZCgAAAAAAAAAAAAAAAAAAAAAAAAAALS0PESUlDJ4jIwz7JCQM/yQkDP8kJAz/JycP/3BwV//m5t/////+/+/v6f+srJv/bGxU/1xcQv93d1//xsa5//v7+v/5+ff/lZWA/ykpEf8kJAz/JCQM/yQkDP8kJAz9JSUMsicnCRoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKioKGCQkDKEjIwz5JCQM/yQkDP8kJAz/JycO/15eRv/NzcH/+/v5/////v/5+fb/9fXx//v7+f//////9vbz/6Ojj/8zMxn/JCQM/yQkDP8kJAz/JCQM/CQkDLQkJA4jAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJiYMFCUlDYgkJAvuJCQM/yQkDP8kJAz/JSUM/zs7Iv+Hh3L/zs7C/+zs5f/y8u7/6urk/8rKvv95eWL/Ly8W/yQkDP8kJAz/JCQM/yQkDPQmJg2ZLS0JHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHx8ACCUlDFEkJA3DIyMM+CQkDP8kJAz/JCQM/yUlDf80NBr/S0sy/1RUPP9JSTD/MjIZ/yUlDf8kJAz/JCQM/yMjDPolJQzOJSUNYCoqFQwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASwsCxcmJgxjJCQMuyQkC+skJAz8JCQM/yQkDP8kJAz/JCQM/yQkDP8kJAz/JCQM/SQkC+8kJAvDJCQLbyoqER4AAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEkJBIOJiYONSYmDGkmJg2ZJCQMuyUlDMwlJQzNJSUMviUlDJ4nJw1vJiYMOyoqDhIAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/8AD//8AAP/8AAA/+AAAH/AAAA/gAAAHwAAAA8AAAAOAAAABgAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAGAAAABwAAAAcAAAAPgAAAH8AAAD/gAAB/8AAA//gAAf/+AAf8='
THEME_LIST = ["yeti", "simplex", "morph", "cerculean", "sandstone", "united", "cosmo", "flatly", "journal", "litera", "lumen", "minty", "pulse"]
theme_config = theme_config if theme_config in THEME_LIST else 'yeti'

# 初始化日志配置
LOG_LEVEL_LIST = ['ERROR', 'WARNING', 'INFO', 'DEBUG']
log_level_config = log_level_config if log_level_config in LOG_LEVEL_LIST else 'INFO'

# 初始化语言配置
LANG_LIST = ['ENG', 'CHS']
lang_config = lang_config if lang_config in LANG_LIST else 'ENG'
LANG = LANG_DICT[lang_config]

# 支持文件类型列表
ZIP_FILE_TYPE_DICT = {
    'application/x-bzip2': '.bz2',
    'application/x-gzip': '.gz',
    'application/x-rar': '.rar',
    'application/x-tar': '.tar',
    'application/x-xz': '.xz',
    'application/zip': '.zip',
    'application/x-7z-compressed': '.7z'
}
