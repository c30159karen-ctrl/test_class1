# 匯入 Google Gen AI SDK
from google import genai
# 匯入 dotenv，用來讀取 .env 檔案中的環境變數（例如 API 金鑰）
from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()

# 建立 Gen AI 用戶端（會自動從環境變數讀取 API 金鑰）
client = genai.Client()

# 呼叫模型，傳入提示文字並取得回應
interaction = client.interactions.create(
    model="gemini-3.5-flash",  # 指定要使用的模型
    input="天空為什麼是藍的"      # 傳給模型的提問內容
)

# 印出模型回傳的文字結果
print(interaction.output_text)