import functions_framework
import tweepy
import gspread
from google.auth import default
import os
from openai import OpenAI

@functions_framework.http
def Ai_API(request):
    client = OpenAI(
        api_key = os.environ.get("OPEN_AI_KEY")
    )
    creds, _ = default()
    client_gsheets = gspread.authorize(creds)
    spreadsheet_id = os.environ.get("spreadsheet_id")
    sheet_name = "シート1"
    sheet = client_gsheets.open_by_key(spreadsheet_id).worksheet(sheet_name)

    max_generate = 5
    sheet = client_gsheets.open_by_key(spreadsheet_id).worksheet(sheet_name)
    # ChatGPTで生成
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        n=max_generate,
        top_p=1,
        messages=[
            {
                "role": "system",
                "content": "あなたはXの投稿者です。投稿内容を作ってください。",
            },
            {
                "role": "user",
                "content": "楽しい気分になれるようなポジティブな内容の投稿を一文で考えてください。",
            },
        ],
    )

    # 投稿内容列の最終行を取得
    header = sheet.row_values(1)
    post_col = header.index("投稿内容") + 1
    next_row = len(sheet.col_values(post_col)) + 1

    # 順に書き込み
    for i, choice in enumerate(chat_completion.choices):
        text = choice.message.content.strip()
        sheet.update_cell(next_row + i, post_col, text)
        
    return "書き込み完了"


