from bs4 import BeautifulSoup
from requests import get


def request_data(url):
    _headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
    _response = get(url, headers=_headers).content
    return _response


def get_chapter_table(url):
    _chapter_table = []
    _html_content = request_data(url)
    _soup = BeautifulSoup(_html_content, "html.parser")  # 解析HTML
    titles = _soup.find_all("div", class_="listmain")[0].find_all("dd")
    for title in titles:
        _chapter_table.append({"chapter": title.text.strip(), "url": (base_url + title.next.attrs['href'])})
    return _chapter_table


def get_chapter_text(url):
    _web_text = request_data(url)
    try:
        _contents = BeautifulSoup(_web_text, "html.parser").find_all("div", id="chaptercontent")[0]
    except:
        _contents = BeautifulSoup(_web_text, "html.parser").find_all("div", id="content", class_="showtxt")[0]
    return _contents


def text_filter(page_text):
    for element in page_text.find_all("p", class_="readinline"):
        element.extract()
    for element in page_text.find_all("script"):
        element.extract()
    page_text = page_text.text.replace("　", "\n")
    page_text = page_text.replace(" ", "\n")
    # page_text = page_text.replace("(https://www.2mcnxs.com/html/book/17/17167/601116274.html)", "")
    page_text = page_text.replace("天才一秒记住本站地址：www.2mcnxs.com。顶点小说手机版阅读网址：2mcnxs.com", "")
    return page_text


base_url = "https://www.2mcnxs.com/"
chapter_table_url = "https://www.2mcnxs.com/html/book/17/17167/"  # 目标网页URL
chapter_table = get_chapter_table(chapter_table_url)
book_name = "我的治愈系游戏"
book_author = "我会修空调"

for chapter in chapter_table[12:]:
    try:
        text_page = get_chapter_text(chapter["url"])
        chapter_text = text_filter(text_page)
        print(f"获取到章节 {chapter['chapter']} ")
        with open(f"{book_name}_{book_author}.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{chapter['chapter']}\n")
            f.write(chapter_text)
    except:
        print(f"章节解析失败 {chapter['chapter']}")
