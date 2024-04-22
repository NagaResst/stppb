from bs4 import BeautifulSoup
from requests import get

base_url = "https://www.bqg88.cc/"
url = "https://www.bqg88.cc/xs/163205/"  # 目标网页URL

chapter_table = []

response = get(url, headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"})  # 发送请求

if response.status_code == 200:
    html_content = response.text
else:
    print(f"请求失败，状态码：{response.status_code}")
    exit()

soup = BeautifulSoup(html_content, "html.parser")  # 解析HTML

titles = soup.find_all("div", class_="listmain")[0].find_all("dd")

for title in titles:
    chapter_table.append({"chapter": title.text.strip(), "url": (base_url + title.next.attrs['href'])})

for chapter in chapter_table:
    try:
        web_text = get(chapter["url"], headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}).text
        contents = BeautifulSoup(web_text, "html.parser").find_all("div", id="chaptercontent")[0]
        for element in contents.find_all("p", class_="readinline"):
            element.extract()
        chapter_text = contents.text.replace("　", "\n")
        with open(f"发家致富从1993开始.txt", "a", encoding="utf-8") as f:
            f.write(chapter_text)
    except:
        print(f"章节解析失败 {chapter['chapter']}")
