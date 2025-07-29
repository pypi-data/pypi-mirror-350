from abc import ABC, abstractmethod
from agentutil.models.news import News as NewsSchema
from typing import List


class AgentAssistant(ABC):
    SUCCESS_FINAL_STATE = "موفق ✅"
    FAILURE_FINAL_STATE = "ناموفق ❌"

    @abstractmethod
    def publish_article(
        self,
        news_id: str,
        news: NewsSchema,
        cms_base_url: str,
        auth_data: tuple,
        
    ):
        pass

    @abstractmethod
    def update_news_status(
        self,
        news_id: str,
        new_status: str = None,
        title: str = None,
        cms_news_id: str = None,
        cost: int = None,
        duration = None,
        pipeline = None
    ):
        pass
    
    @abstractmethod
    def get_blacklisted_urls() -> List[str]:
        pass

    @abstractmethod
    def save_news_content(
        self,
        news_id: str,
        news: NewsSchema
    ):
        pass
