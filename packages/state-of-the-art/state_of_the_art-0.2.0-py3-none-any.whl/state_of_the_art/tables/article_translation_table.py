import os
from typing import Optional
from state_of_the_art.tables.base_table import BaseTable

class ArticleTranslationTable(BaseTable):
    table_name = "article_translation"
    schema = {"url": {"type": str}, "content": {"type": str}, "translation": {"type": str}}

    def add_article(self, url: str, original_content: str, merged_content: str) -> str:
        if not url:
            raise ValueError("url is required to add an article to article translation table")
        return self.add(url=url, content=original_content, translation=merged_content)

    def get_translation_by_id(self, url: str) -> Optional['ArticleTranslation']:
        df = self.read(recent_first=True)
        # filter by url and get first row
        filter = df[df['url'] == url]
        if len(filter) == 0:
            return None
        data = filter.iloc[0]
        return ArticleTranslation(url=data['url'], original_content=data['content'], merged_content=data['translation'])

class ArticleTranslation:
    def __init__(self, url: str, original_content: str, merged_content: str):
        self.url = url
        self.original_content = original_content
        self.merged_content = merged_content
