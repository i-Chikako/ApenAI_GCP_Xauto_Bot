# 🐤 ChatGPT × GCP × X自動ポストBot

**ChatGPTで生成したポスト案をGoogleスプレッドシートに保存し、Cloud FunctionsとSchedulerを使って自動投稿する仕組み**です。  
週1回の自動生成と、月～金の自動投稿をスケジューリングしています。

---

## 🔧 使用技術

- Google Cloud Functions
- Cloud Scheduler
- Google Sheets API
- OpenAI API（ChatGPT）
- X API
- Python 3.10

---

## 🔁 処理の流れ

| 処理内容          | 頻度         | Cloud Function名           　| 説明                                       |
|-------------------|--------------|-----------------------------|-------------------------------------------|
| ポスト文の自動生成 | 毎週月曜 9:00 | `generate_tweet_function`   | ChatGPTで生成 → Googleスプレッドシートに保存 |
| ポストの自動投稿   | 月～金 12：00 | `post_tweet_function`       | スプレッドシートから投稿 → 投稿済みフラグ更新 |

---

## 📂 フォルダ構成

```bash
.
├── generate_post_function/
│   ├── main.py               # ChatGPTでポスト文を生成しスプレッドシートに追加
│   └── requirements.txt      # OpenAI, gspread など
├── post_auto_function/
│   ├── main.py               # スプレッドシートから投稿してXに送信
│   └── requirements.txt      # tweepy, gspread など
└── README.md                 # このドキュメント
