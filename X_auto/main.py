import functions_framework
import tweepy
import gspread
from google.auth import default
from datetime import datetime, timezone, timedelta
import os

@functions_framework.http
def post_from_sheets(request):
    API_Key = os.environ.get("API_KEY")
    API_Key_Secret = os.environ.get("API_SECRET_KEY")
    Access_Token = os.environ.get("ACCESS_TOKEN")
    Access_Token_Secret = os.environ.get("ACCESS_TOKEN_SECRET")
    Bearer_Token = os.environ.get("BEARER_TOKEN")

    client = tweepy.Client(
        bearer_token=Bearer_Token,
        consumer_key=API_Key,
        consumer_secret=API_Key_Secret,
        access_token=Access_Token,
        access_token_secret=Access_Token_Secret
    )

    creds, _ = default()
    client_gsheets = gspread.authorize(creds)

    spreadsheet_id = os.environ.get("spreadsheet_id")
    sheet_name = "シート1"
    sheet = client_gsheets.open_by_key(spreadsheet_id).worksheet(sheet_name)

    data = sheet.get_all_records()

    for i, row in enumerate(data):
        tweet_content = row['投稿内容']
        status = row['完了']

        if status == "":
            client.create_tweet(text=tweet_content)
            sheet.update_cell(i + 2, 2, "済み")
            current_time = (datetime.utcnow() + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")
            sheet.update_cell(i + 2, 3, current_time)
            break

    return "post is done"  
