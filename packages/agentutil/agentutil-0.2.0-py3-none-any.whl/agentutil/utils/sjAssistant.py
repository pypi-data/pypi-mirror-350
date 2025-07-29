from agentutil.helper.publisher import publish_article as publish_article_helper
from agentutil.models.news import NewsORM, News as NewsSchema
from agentutil.helper.mongo_client import get_mongo_client
from agentutil.models.blocked_sites import SiteBlockedORM
from agentutil.utils.agentAssistant import AgentAssistant
from agentutil.helper.sql_client import get_db

from typing import List


class SJAssistant(AgentAssistant):
    def __init__(self):
        super().__init__()


    def publish_article(
        self,
        news_id: str,
        news: NewsSchema,
        cms_base_url: str,
        auth_data: tuple,
        republish: bool = False
    ) -> tuple:
        return publish_article_helper(
            news_id=news_id,
            news=news,
            cms_base_url=cms_base_url,
            auth_data=auth_data,
            republish=republish
        )


    def update_news_status(
        self,
        news_id: str,
        news_status: str = None,
        title: str = None,
        cms_news_id: str = None,
        cost: int = None,
        duration = None,
        pipeline = None
    ) -> bool: 
        try:
            with get_db() as db:
                news_obj: NewsORM = db.query(NewsORM).filter(
                    NewsORM.id == news_id
                ).first()

                if not news_obj:
                    return False

                if news_status:
                    news_obj.status = news_status

                if title:
                    news_obj.title = title

                if cms_news_id:
                    news_obj.news_id = cms_news_id

                if cost:
                    news_obj.cost = cost

                if duration:
                    news_obj.duration = duration

                if pipeline:
                    news_obj.pipeline = pipeline

                db.commit()

            return True

        except Exception as e:
            print(f"Unexpected error while updating news {news_id}: {e}")
            return False

    
    def get_blacklisted_urls(self) -> List[str]:
        try:
            with get_db() as db:
                blacklisted = db.query(SiteBlockedORM.url).filter(
                    SiteBlockedORM.is_active == True
                ).all()

                return [url for (url,) in blacklisted]
            
        except Exception as e:
            print(f"Unexpected error while get blacklisted urls: {e}")
            return None


    def save_news_content(self, news_id: str, news: NewsSchema) -> None:
        try:
            mongo_db = get_mongo_client()
            collection = mongo_db["news_publish_logs"]

            news_data = {
                "title": news.title,
                "summary": news.summary,
                "content": news.content,
                "status": news.status,
            }

            collection.update_one(
                {"news_id": news_id},
                {"$set": {"news": news_data}},
                upsert=True
            )
        except Exception as e:
            print(e)


    def save_create_config(self, *args, **kwargs):
        pass
