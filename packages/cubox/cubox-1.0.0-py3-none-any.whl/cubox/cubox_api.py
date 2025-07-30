import os
import shutil
from typing import List, Dict, Optional, Tuple

import requests

# 常量定义
ALL_FOLDERS_ID = "all_folders"
ALL_ITEMS = "all_items"
ALL_STATUS_ID = "all_status"


class CuboxArticle:
    """Cubox文章对象"""

    def __init__(
            self,
            id: str,
            title: str,
            article_title: str,
            description: str,
            url: str,
            domain: str,
            create_time: str,
            update_time: str,
            word_count: int,
            content: Optional[str],
            cubox_url: str,
            highlights: Optional[List[Dict]] = None,
            tags: Optional[List[str]] = None,
            type: str = ""
    ):
        self.id = id
        self.title = title
        self.article_title = article_title
        self.description = description
        self.url = url
        self.domain = domain
        self.create_time = create_time
        self.update_time = update_time
        self.word_count = word_count
        self.content = content
        self.cubox_url = cubox_url
        self.highlights = highlights or []
        self.tags = tags or []
        self.type = type

    @classmethod
    def from_dict(cls, data: Dict) -> 'CuboxArticle':
        """从字典创建CuboxArticle对象"""
        return cls(
            id=data.get('id', ''),
            title=data.get('title', ''),
            article_title=data.get('article_title', ''),
            description=data.get('description', ''),
            url=data.get('url', ''),
            domain=data.get('domain', ''),
            create_time=data.get('create_time', ''),
            update_time=data.get('update_time', ''),
            word_count=data.get('word_count', 0),
            content=data.get('content'),
            cubox_url=data.get('cubox_url', ''),
            highlights=data.get('highlights', []),
            tags=data.get('tags', []),
            type=data.get('type', '')
        )


class CuboxHighlight:
    """Cubox高亮对象"""

    def __init__(
            self,
            id: str,
            text: str,
            color: str,
            create_time: str,
            cubox_url: str,
            image_url: Optional[str] = None,
            note: Optional[str] = None
    ):
        self.id = id
        self.text = text
        self.color = color
        self.create_time = create_time
        self.cubox_url = cubox_url
        self.image_url = image_url
        self.note = note


class CuboxFolder:
    """Cubox文件夹对象"""

    def __init__(
            self,
            id: str,
            name: str,
            nested_name: str,
            uncategorized: bool
    ):
        self.id = id
        self.name = name
        self.nested_name = nested_name
        self.uncategorized = uncategorized

    @classmethod
    def from_dict(cls, data: Dict) -> 'CuboxFolder':
        """从字典创建CuboxFolder对象"""
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            nested_name=data.get('nested_name', ''),
            uncategorized=data.get('uncategorized', False)
        )


class CuboxTag:
    """Cubox标签对象"""

    def __init__(
            self,
            id: str,
            name: str,
            nested_name: str,
            parent_id: Optional[str]
    ):
        self.id = id
        self.name = name
        self.nested_name = nested_name
        self.parent_id = parent_id

    @classmethod
    def from_dict(cls, data: Dict) -> 'CuboxTag':
        """从字典创建CuboxTag对象"""
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            nested_name=data.get('nested_name', ''),
            parent_id=data.get('parent_id')
        )


class CuboxApi:
    """Cubox API客户端"""

    def __init__(self, domain: str, api_key: str):
        """
        初始化Cubox API客户端
        
        Args:
            domain: Cubox域名
            api_key: API密钥
        """
        self.endpoint = f"https://{domain}"
        if '/' in api_key:
            api_key = api_key.split('/')[-1]
        self.api_key = api_key

    def update_config(self, domain: str, api_key: str) -> None:
        """
        同时更新域名和API Key
        
        Args:
            domain: 新的Cubox域名
            api_key: 新的API密钥
        """
        self.endpoint = f"https://{domain}"
        self.api_key = api_key

    def _request(self, path: str, method: str = "GET", body: Optional[Dict] = None) -> Dict:
        """
        发送API请求
        
        Args:
            path: API路径
            method: HTTP方法
            body: 请求体
            
        Returns:
            响应数据
        """
        url = f"{self.endpoint}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=body)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")

            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API请求失败: {e}")
            raise

    def get_articles(self,
                     last_card_id: Optional[str] = None,
                     last_card_update_time: Optional[str] = None,
                     folder_filter: Optional[List[str]] = None,
                     type_filter: Optional[List[str]] = None,
                     status_filter: Optional[List[str]] = None,
                     tags_filter: Optional[List[str]] = None,
                     is_read: Optional[bool] = None,
                     is_starred: Optional[bool] = None,
                     is_annotated: Optional[bool] = None) -> Tuple[List[CuboxArticle], bool]:
        """
        获取文章列表
        
        Args:
            last_card_id: 上一页最后一篇文章ID
            last_card_update_time: 上一页最后一篇文章更新时间
            folder_filter: 文件夹过滤
            type_filter: 类型过滤
            status_filter: 状态过滤
            tags_filter: 标签过滤
            is_read: 是否已读
            is_starred: 是否标星
            is_annotated: 是否有批注
            
        Returns:
            文章列表和是否有更多数据
        """
        try:
            request_body = {"limit": 50}
            page_size = 50

            if last_card_id and last_card_update_time:
                request_body["last_card_id"] = last_card_id
                request_body["last_card_update_time"] = last_card_update_time

            # 添加文件夹过滤
            if folder_filter and len(folder_filter) > 0:
                if ALL_FOLDERS_ID not in folder_filter:
                    request_body["group_filters"] = folder_filter

            # 添加类型过滤
            if type_filter and len(type_filter) > 0:
                request_body["type_filters"] = type_filter

            # 添加状态过滤
            if status_filter and len(status_filter) > 0:
                if ALL_STATUS_ID not in status_filter:
                    if is_read is True:
                        request_body["read"] = True
                    if is_starred is True:
                        request_body["starred"] = True
                    if is_annotated is True:
                        request_body["annotated"] = True

            # 添加标签过滤
            if tags_filter and len(tags_filter) > 0:
                if ALL_ITEMS not in tags_filter:
                    request_body["tag_filters"] = tags_filter

            path = "/c/api/third-party/card/filter"
            response = self._request(path, method="POST", body=request_body)

            articles_data = response.get('data', [])
            articles = [CuboxArticle.from_dict(article) for article in articles_data]
            has_more = len(articles) >= page_size

            return articles, has_more
        except Exception as e:
            print(f"获取文章列表失败: {e}")
            raise e

    def get_article_detail(self, article_id: str) -> Optional[str]:
        """
        获取文章详情，包括内容
        
        Args:
            article_id: 文章ID
            
        Returns:
            文章内容
        """
        try:
            path = f"/c/api/third-party/card/content?id={article_id}"
            response = self._request(path)

            return response.get('data')
        except Exception as e:
            print(f"获取文章 {article_id} 详情失败: {e}")
            return None

    def get_folders(self) -> List[CuboxFolder]:
        """
        获取用户的文件夹列表
        
        Returns:
            文件夹列表
        """
        try:
            path = "/c/api/third-party/group/list"
            response = self._request(path)

            folders_data = response.get('data', [])
            return [CuboxFolder.from_dict(folder) for folder in folders_data]
        except Exception as e:
            print(f"获取Cubox文件夹列表失败: {e}")
            raise e

    def get_tags(self) -> List[CuboxTag]:
        """
        获取用户的标签列表
        
        Returns:
            标签列表
        """
        try:
            path = "/c/api/third-party/tag/list"
            response = self._request(path)

            tags_data = response.get('data', [])
            return [CuboxTag.from_dict(tag) for tag in tags_data]
        except Exception as e:
            print(f"获取Cubox标签列表失败: {e}")
            raise e


def _get_safe_filename(filename: str) -> str:
    """
    将字符串转换为安全的文件名

    Args:
        filename: 原始文件名

    Returns:
        安全的文件名
    """
    # 移除不安全的字符
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')

    # 限制长度
    if len(filename) > 50:
        filename = filename[:50]

    return filename


class CuboxOutput:
    def __init__(self, api: CuboxApi, articles: List[CuboxArticle]):
        self.api = api
        self.articles = articles
        self.total_articles = len(articles)

    def to_markdown(self, file_path: str = 'cubox') -> None:
        """
        将文章列表转换为markdown格式并保存到指定目录
        
        Args:
            file_path: 保存markdown文件的目录路径
        """
        # 如果目录已存在，先删除
        if os.path.exists(file_path):
            shutil.rmtree(file_path)

        # 创建保存目录
        os.makedirs(file_path, exist_ok=True)

        # 遍历所有文章
        for i, article in enumerate(self.articles):
            print(f"正在处理第 {i + 1}/{self.total_articles} 篇文章: {article.title}")

            # 从API获取文章详细内容
            if not article.content:
                article.content = self.api.get_article_detail(article.id)

            # 创建安全的文件名
            safe_filename = f"{_get_safe_filename(article.title)}.md"
            article_path = os.path.join(file_path, safe_filename)

            # 创建文章文件
            with open(article_path, 'w', encoding='utf-8') as article_file:
                # 写入YAML格式的元数据
                article_file.write('---\n')
                article_file.write(f'title: "{article.title}"\n')
                article_file.write(f'url: "{article.url}"\n')
                article_file.write(f'domain: "{article.domain}"\n')
                article_file.write(f'create_time: "{article.create_time}"\n')
                article_file.write(f'update_time: "{article.update_time}"\n')
                article_file.write(f'word_count: {article.word_count}\n')
                if article.tags and len(article.tags) > 0:
                    article_file.write('tags:\n')
                    for tag in article.tags:
                        article_file.write(f'  - "{tag}"\n')
                article_file.write('---\n\n')

                # 写入标题
                article_file.write(f"# {article.title}\n\n")

                content = self.api.get_article_detail(article.id)
                # 写入内容
                if content:
                    article_file.write(f"{content}\n\n")
                else:
                    article_file.write(f"{article.description}\n\n")

                # 写入高亮内容
                if article.highlights and len(article.highlights) > 0:
                    article_file.write("## 高亮\n\n")
                    for highlight in article.highlights:
                        article_file.write(f"> {highlight.get('text', '')}\n\n")

                        # 如果有批注
                        if highlight.get('note'):
                            article_file.write(f"**批注**: {highlight.get('note')}\n\n")

        # 完成导出的信息
        print(f"已将 {self.total_articles} 篇文章导出到 {os.path.abspath(file_path)} 目录")
