import io
import tkinter as tk
from tkinter import filedialog
from google.cloud import vision
from google.oauth2 import service_account
import re

# Google Cloud Vision API 설정
credentials = service_account.Credentials.from_service_account_file(
    r"C:/Users/Admin/Desktop/vs-code-421312-cb357167d131.json"  # 서비스 계정 키 파일 경로
)
client = vision.ImageAnnotatorClient(credentials=credentials)

def select_image_and_find_dates():
    # 파일 선택 대화상자 열기
    root = tk.Tk()
    root.withdraw()  # tkinter 창 숨기기
    filepath = filedialog.askopenfilename()
    if not filepath:
        return

    # 이미지 파일에서 텍스트 추출
    with io.open(filepath, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    full_text = texts[0].description if texts else ""

    # yyyy.MM.dd 형식 날짜 찾기
    date_pattern = r'\d{4}\.\d{2}\.\d{2}'
    dates = re.findall(date_pattern, full_text)

    # 찾은 날짜 출력
    if dates:
        print("Detected dates:")
        for date in dates:
            print(date)
    else:
        print("No dates in the format yyyy.MM.dd were detected.")

if __name__ == "__main__":
    select_image_and_find_dates()