import re
import threading
from itertools import combinations

import regex
import unicodedata
from html.parser import HTMLParser


from re_common.v2.baselibrary.utils.string_smi import JaroDamerauLevenshteinMaxSim


def bj2qj(src):
    if src is None:
        return src

    DBC_SPACE = ' '
    SBC_SPACE = '　'
    DBC_CHAR_START = 33
    DBC_CHAR_END = 126
    CONVERT_STEP = 65248

    buf = []
    for char in src:
        if char == DBC_SPACE:
            buf.append(SBC_SPACE)
        elif DBC_CHAR_START <= ord(char) <= DBC_CHAR_END:
            buf.append(chr(ord(char) + CONVERT_STEP))
        else:
            buf.append(char)

    return ''.join(buf)


def qj2bj(src):
    """
    全角转半角
    :param src:
    :return:
    """
    if src is None:
        return src

    SBC_CHAR_START = 0xFF01
    SBC_CHAR_END = 0xFF5E
    CONVERT_STEP = 0xFEE0
    DBC_SPACE = ' '
    SBC_SPACE = '　'

    buf = []
    for char in src:
        if SBC_CHAR_START <= ord(char) <= SBC_CHAR_END:
            buf.append(chr(ord(char) - CONVERT_STEP))
        elif char == SBC_SPACE:
            buf.append(DBC_SPACE)
        else:
            buf.append(char)

    return ''.join(buf)


def get_diacritic_variant(char1):
    # 将字符转换为标准的 Unicode 形式
    normalized_char1 = unicodedata.normalize('NFD', char1)

    # 获取基本字符（去掉变音符号）
    base_char1 = ''.join(c for c in normalized_char1 if unicodedata.category(c) != 'Mn')

    # 判断基本字符是否相同
    return base_char1


def get_alphabetic_ratio(text: str) -> float:
    # 返回字母型字符所占比例
    if not text:
        return 0

    text = re.sub(r'\d+', '', text)

    # 正则表达式匹配字母型文字（包括拉丁字母、希腊字母、西里尔字母、阿拉伯字母等）
    alphabetic_pattern = (
        r"[\u0041-\u005A\u0061-\u007A"  # 拉丁字母 (A-Z, a-z)
        r"\u00C0-\u00FF"  # 带重音符号的拉丁字母 (À-ÿ)
        r"\u0080–\u00FF"  # 拉丁字母补充1
        r"\u0100–\u017F"  # 拉丁字母扩展A
        r"\u1E00-\u1EFF"  # 拉丁扩展 (Latin Extended Additional)
        r"\u0180-\u024F"  # 拉丁扩展-B (Latin Extended-B)
        r"\u2C60-\u2C7F"  # 拉丁扩展-C (Latin Extended Additional)
        r"\uA720-\uA7FF"  # 拉丁扩展-D (Latin Extended Additional)
        r"\uAB30-\uAB6F"  # 拉丁扩展-E (Latin Extended Additional)
        r"]"
    )

    # 使用正则表达式过滤出语言文字
    clean_text = regex.sub(r"[^\p{L}]", "", text)

    if len(clean_text) == 0:
        return 1.0

    # 匹配所有字母型字符
    alphabetic_chars = re.findall(alphabetic_pattern, clean_text)

    # 返回字母型字符所占比例
    return len(alphabetic_chars) / len(clean_text)


class HTMLTextExtractor(HTMLParser):
    _thread_local = threading.local()  # 线程局部存储

    def __init__(self):
        super().__init__()
        self.reset_state()

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip = True

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = False

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.text.append(data)

    def reset_state(self):
        self.reset()
        self.text = []
        self.skip = False

    def get_text(self):
        return ''.join(self.text).strip()

    @classmethod
    def get_parser(cls):
        # 每个线程获取独立实例
        if not hasattr(cls._thread_local, 'parser'):
            cls._thread_local.parser = cls()
        return cls._thread_local.parser


def clean_html(html):
    parser = HTMLTextExtractor.get_parser()
    parser.reset_state()
    parser.feed(html)
    parser.close()
    return parser.get_text()


def remove_spaces_between_chinese_characters(text):
    """
    匹配中文间的空格并替换为空字符串

    这里没有选取 后面的一些扩展分区 是那些分区比较分散 都写进来消耗性能,
    认为只包含这些也够用了
    """
    pattern = r'(?<=[\u3400-\u9fff])\s+(?=[\u3400-\u9fff])'
    return re.sub(pattern, '', text)



sim_utils = JaroDamerauLevenshteinMaxSim()

def group_similar_texts(texts, threshold=0.9):
    """根据相似度对文本进行分组"""
    from re_common.v2.baselibrary.utils.string_clear import rel_clear
    n = len(texts)
    # 创建邻接表表示图
    graph = [[] for _ in range(n)]
    # 计算所有文本对的相似度并构建图
    for i, j in combinations(range(n), 2):
        similarity = sim_utils.get_sim(rel_clear(texts[i]), rel_clear(texts[j]))
        if similarity >= threshold:
            graph[i].append(j)
            graph[j].append(i)

    visited = [False] * n
    groups = []

    # 使用DFS找到连通分量
    def dfs(node, group):
        visited[node] = True
        group.append(node)
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor, group)

    # 找到所有连通分量
    for i in range(n):
        if not visited[i]:
            current_group = []
            dfs(i, current_group)
            groups.append(current_group)

    return groups


def get_group_abstract(lists):
    """
    这是一个 分组程序 ，会根据简单的连通图分组
    lists: [(id,txt),...]
    return: all_list 返回一个二维列表 每个列表里面是id 每个列表为一个分组
    """
    abstract_list = [i[1] for i in lists]
    keyid_list = [i[0] for i in lists]
    groups = group_similar_texts(abstract_list, threshold=0.9)
    all_list = []
    for group in groups:
        t_list = []
        for text_idx in group:
            t_list.append(keyid_list[text_idx])
        all_list.append(t_list)
    return all_list
