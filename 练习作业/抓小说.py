from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from requests import get


def request_data(url):
    """
    从指定的URL请求数据。

    参数:
    url: 字符串，指定要请求数据的URL地址。

    返回值:
    返回请求到的二进制数据。
    """
    # 设置请求头，伪装为Chrome浏览器发送请求
    _headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
    # 发送GET请求并获取响应内容
    _response = get(url, headers=_headers).content
    return _response


def get_chapter_table(url):
    """
    从指定的URL获取章节表

    参数:
    url: str - 需要获取章节表的网页URL

    返回值:
    list - 包含章节名和对应URL的字典列表
    """
    _chapter_table = []
    _html_content = request_data(url)  # 从URL获取HTML内容
    _soup = BeautifulSoup(_html_content, "html.parser")  # 解析HTML内容
    # 找到章节列表的HTML元素
    titles = _soup.find_all("div", class_="listmain")[0].find_all("dd")
    for title in titles:
        # 提取章节名和URL，并添加到章节表中
        _chapter_table.append({"chapter": title.text.strip(), "url": (base_url + title.next.attrs['href'])})
    return _chapter_table


def get_chapter_text(chapter):
    """
    获取指定章节的文本内容。

    参数:
    - chapter: 字典类型，包含章节的url和章节名称。

    返回值:
    - 无返回值，但会将获取到的章节文本内容存储在chapter字典的"chapter_text"键中。
    """
    # 从指定URL请求章节数据
    _web_text = request_data(chapter["url"])
    # 使用ID为"content"且class为"showtxt"的div元素获取章节内容
    _contents = BeautifulSoup(_web_text, "html.parser").find_all("div", id="content", class_="showtxt")[0]
    # 对获取到的内容进行过滤，并将过滤后的文本内容存储在chapter字典的"chapter_text"键中
    chapter["chapter_text"] = text_filter(_contents)
    chapter["chapter_text_length"] = count_valid_characters(chapter["chapter_text"])
    # 打印章节信息，包括章节名称和内容长度
    print(f"获取到章节 {chapter['chapter']}  章节长度 {chapter['chapter_text_length']}")


def text_filter(page_text):
    """
    过滤给定网页文本中的特定元素，并进行格式化处理。

    参数:
    page_text - BeautifulSoup对象，代表从网页抓取的原始文本。

    返回值:
    _formatted_text - 格式化处理后的文本字符串，去除了特定的不需要的元素和格式。
    """
    _formatted_text = ""

    # 移除所有class为'readinline'的<p>元素
    for element in page_text.find_all("p", class_="readinline"):
        element.extract()

    # 移除所有的<script>元素
    for element in page_text.find_all("script"):
        element.extract()

    # 替换特定的空格和字符串，为后续的文本处理做准备
    page_text = page_text.text.replace("　", "\n")
    page_text = page_text.replace("        ", "\n")
    page_text = page_text.replace("天才一秒记住本站地址：www.2mcnxs.com。顶点小说手机版阅读网址：2mcnxs.com", "")

    lines = []
    # 对处理后的文本去除多余的空行
    for line in page_text.splitlines():
        line = line.strip()
        if line:
            lines.append(line + "\n")

    # 将整理后的文本行重新组合为一个字符串
    _formatted_text = _formatted_text.join(lines)
    return _formatted_text


def count_valid_characters(text):
    """
    统计给定字符串中有效文字的数量。

    参数:
    text (str): 待统计的字符串。

    返回值:
    int: 字符串中有效文字的数量。
    """
    import re
    # 正则表达式匹配常见有效文字：汉字、字母（大小写）、数字
    _pattern = r'[\u4e00-\u9fffA-Za-z0-9]'

    # 使用正则表达式的findall方法查找所有匹配项
    _matches = re.findall(_pattern, text)

    return len(_matches)


# 网站根地址和目标章节表URL
chapter_table_url = "https://www.2mcnxs.com/html/book/17/17167/"  # 目标网页URL
base_url = urlparse(chapter_table_url).netloc

# 获取章节表
chapter_table = get_chapter_table(chapter_table_url)

# 获取书籍名称和作者
chapter_table_page = BeautifulSoup(get(chapter_table_url).text, "html.parser")
book_author = chapter_table_page.find("meta", property="og:novel:author").text
book_name = chapter_table_page.find("meta", property="og:novel:book_name").text
print(f"书籍名称：{book_name} 作者：{book_author}")

# 使用线程池并发地获取所有章节的文本
tpool = ThreadPoolExecutor(max_workers=30)
tpool.map(get_chapter_text, chapter_table)
tpool.shutdown(wait=True)

# 将所有章节文本写入一个文本文件
for chapter in chapter_table[12:]:  # 跳过最新更新章节
    with open(f"{book_name}_{book_author}.txt", "a", encoding="utf-8") as f:
        f.write(f"《{book_name}》    作者： {book_author}")
        f.write(f"\n\n\n{chapter['chapter']}\n本章字数： {chapter['chapter_text_length']}\n\n")  # 每章之前添加标题和空行
        f.write(chapter["chapter_text"])
