import os
from notion_client import Client

# 初始化 Notion 客户端
notion = Client(auth=os.environ["NOTION_API_KEY"])

# PodcastSummary 数据库 ID
PODCAST_SUMMARY_DATABASE_ID = "10f8a86cad6380f4ad74e1eab2708e77"

def get_podcast_summaries():
    try:
        response = notion.databases.query(
            database_id=PODCAST_SUMMARY_DATABASE_ID,
            sorts=[{
                "property": "Title",
                "direction": "ascending"
            }]
        )
        
        summaries = []
        for page in response["results"]:
            summary = {
                "title": page["properties"]["Title"]["title"][0]["plain_text"],
                "link": page["properties"]["Link"]["url"],
                "summary": page["properties"]["Summary"]["rich_text"][0]["plain_text"] if page["properties"]["Summary"]["rich_text"] else ""
            }
            summaries.append(summary)
        
        return summaries
    except Exception as e:
        error_message = f"Error occurred while fetching podcast summaries: {str(e)}"
        print(error_message)
        return [], [error_message]

def add_podcast_summary(title, link, summary):
    try:
        notion.pages.create(
            parent={"database_id": PODCAST_SUMMARY_DATABASE_ID},
            properties={
                "Title": {"title": [{"text": {"content": title}}]},
                "Link": {"url": link},
                "Summary": {"rich_text": [{"text": {"content": summary}}]}
            }
        )
        return True
    except Exception as e:
        print(f"Error occurred while adding podcast summary: {str(e)}")
        return False

