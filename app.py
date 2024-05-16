from flask import Flask, request, render_template
from google.cloud import vision
from google.oauth2 import service_account
import re
import io

app = Flask(__name__)

# Google Cloud Vision API 설정
credentials = service_account.Credentials.from_service_account_file(
    r"C:/Users/Admin/Desktop/vs-code-421312-cb357167d131.json"  # 서비스 계정 키 파일 경로
)
client = vision.ImageAnnotatorClient(credentials=credentials)

@app.route('/')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file_and_find_dates():
    if request.method == 'POST':
        f = request.files['file']
        if not f:
            return "파일이 선택되지 않았습니다."

        # 이미지 파일에서 텍스트 추출
        content = f.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        full_text = texts[0].description if texts else ""

        # yyyy.MM.dd 형식 날짜 찾기
        date_pattern = r'\d{4}\.\d{2}\.\d{2}'
        dates = re.findall(date_pattern, full_text)

        # 찾은 날짜 출력
        if dates:
            dates_str = "<br>".join(dates)
            return f"<br>{dates_str}"
        else:
            return "yyyy.MM.dd 형식의 날짜가 감지되지 않았습니다."

if __name__ == '__main__':
   app.run(debug = True)