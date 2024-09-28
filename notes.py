import os
from notion_client import Client

# 初始化 Notion 客户端
notion = Client(auth=os.environ["NOTION_API_KEY"])

# PodcastSummary 数据库 ID
PODCAST_SUMMARY_DATABASE_ID = "10f8a86cad6380f4ad74e1eab2708e77"
def check_notion_connection():
    try:
        # 檢查 NOTION_API_KEY 環境變量是否存在
        if "NOTION_API_KEY" not in os.environ:
            return "錯誤: NOTION_API_KEY 環境變量未設置"
        # 檢查 NOTION_API_KEY 是否為空
        if not os.environ["NOTION_API_KEY"]:
            return "錯誤: NOTION_API_KEY 環境變量為空"
        # 嘗試獲取數據庫信息
        notion.databases.retrieve(database_id=PODCAST_SUMMARY_DATABASE_ID)
        return "Notion 連接成功!"
    except Exception as e:
        return f"Notion 連接失敗: {str(e)}"

# 測試 Notion 連接
if check_notion_connection():
    print("Notion API 可以正常使用。")
else:
    print("請檢查你的 Notion API 密鑰和數據庫 ID 是否正確。")

def get_latest_podcast_summary():
    try:
        response = notion.databases.query(
            database_id=PODCAST_SUMMARY_DATABASE_ID,
            sorts=[{
                "property": "Created time",
                "direction": "descending"
            }],
            page_size=1
        )
        
        if response["results"]:
            latest_page = response["results"][0]
            latest_summary = {
                "title": latest_page["properties"]["Title"]["title"][0]["plain_text"],
                "link": latest_page["properties"]["Link"]["url"],
                "summary": latest_page["properties"]["Summary"]["rich_text"][0]["plain_text"] if latest_page["properties"]["Summary"]["rich_text"] else ""
            }
            return latest_summary
        else:
            return None
    except Exception as e:
        print(f"Error occurred while fetching the latest podcast summary: {str(e)}")
        return None

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
        print(f"Error occurred while fetching podcast summaries: {str(e)}")
        return []

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

