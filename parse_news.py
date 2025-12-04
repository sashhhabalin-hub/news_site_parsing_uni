import os
import json
from collections import defaultdict
from bs4 import BeautifulSoup

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_html(filename: str):
    path = os.path.join(SCRIPT_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def look_like_news(title: str):
    return "2023" in title and "," in title


def parse_news(html: str):
    soup = BeautifulSoup(html, "html.parser")

    known_sections = {
        "Общество",
        "Мир",
        "Недвижимость",
        "Происшествия",
        "Спорт",
        "Здоровье",
        "Политика",
        "Экономика",
        "Интернет и технологии",
        "Наука и техника",
        "Авто",
        "Туризм",
        "Страна",
        "Культура",
    }

    result = defaultdict(list)
    anchors = soup.find_all("a")

    for a in anchors:
        section_name = a.get_text(strip=True)
        if section_name not in known_sections:
            continue
        news_tag = a.find_next("a")
        if news_tag is None:
            continue
        title = news_tag.get_text(strip=True)
        if not look_like_news(title):
            continue
        href = news_tag.get("href", "").strip()
        result[section_name].append(
            {
                "title": title,
                "url": href,
            })
    return dict(result)

def main():
    html = load_html("iz_news.html")
    news_by_section = parse_news(html)

    print(json.dumps(news_by_section, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()