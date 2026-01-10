import base64
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def encode_image(image_path):
    """이미지 파일을 base64 문자열로 인코딩"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def parse_portfolio_api(image_path):
    """
    포트폴리오 이미지를 분석하여 종목 정보를 JSON으로 반환
    Model: gpt-4o-mini (Cost effective)
    """
    if not os.path.exists(image_path):
        return {"error": "File not found"}

    base64_image = encode_image(image_path)

    prompt = """
    Analyze this stock portfolio screenshot.
    Extract the Ticker Symbol, Quantity (Shares), and Return Rate (%) for each holding.
    Ignore cash or total account value.
    
    If the ticker is Korean (e.g., 삼성전자), try to convert it to a symbol (e.g., 005930.KS) or keep the name if unsure.
    
    Return ONLY a raw JSON string (no markdown formatting like ```json ... ```) with this structure:
    [
        {"symbol": "AAPL", "quantity": 10, "return_pct": 15.4},
        {"symbol": "TSLA", "quantity": 5, "return_pct": -2.1}
    ]
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=500,
        )
        
        content = response.choices[0].message.content.strip()
        
        # Markdown 코드블록이 섞여있을 경우 제거
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
            
        return json.loads(content)

    except Exception as e:
        print(f"Error parsing image: {e}")
        return []

if __name__ == "__main__":
    # parser.py 위치: /app/api/rag/parser.py
    # 이미지 위치: /app/api/test_portfolio.jpg
    # 따라서 상위 폴더(../)로 가서 찾아야 함
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir) # api/
    test_img = os.path.join(parent_dir, "test_portfolio.jpg")
    
    if os.path.exists(test_img):
        print(f"Analyzing {test_img}...")
        result = parse_portfolio_api(test_img)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Test image not found at: {test_img}")
        print("Please place 'test_portfolio.jpg' in the 'api/' directory.")
