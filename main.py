import time
from PIL import Image     #pip install pillow
from pytesseract import * #pip install pytesseract
import configparser
import os


#이미지 -> 문자열 추출
def ocrToStr(fullPath, outTxtPath, fileName, lang='eng'): #디폴트는 영어로 추출
    img = Image.open(fullPath)
    txtName = os.path.join(outTxtPath,fileName.split('.')[0])

    #추출(이미지파일, 추출언어, 옵션)
    #preserve_interword_spaces : 단어 간격 옵션을 조절하면서 추출 정확도를 확인한다.
    #psm(페이지 세그먼트 모드 : 이미지 영역안에서 텍스트 추출 범위 모드)
    #psm 모드 : https://github.com/tesseract-ocr/tesseract/wiki/Command-Line-Usage
    outText = image_to_string(img, lang=lang, config='--psm 4 -c preserve_interword_spaces=1')
    print('Extract FileName ->>> : ', fileName, ' : <<<-')
    strToTxt(txtName, outText)      #추출 문자 텍스트 파일 쓰기

def strToTxt(txtName, outText):
    with open(txtName + '.txt', 'w', encoding='utf-8') as f:
        f.write(outText)

if __name__ == "__main__":
    print("initialization Strat")
    config = configparser.ConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'property.ini')
    inImgPath = os.path.dirname(os.path.realpath(__file__))+ config['Path']['imgPath']
    outTxtPath = os.path.dirname(os.path.realpath(__file__))+ config['Path']['txtPath']
    print("이미지 입력 경로 : %s" % (inImgPath))
    print("텍스트 출력 경로 : %s" % (outTxtPath))
    print("initialization End")
    time.sleep(3)

    #OCR 추출 작업 메인
    for root, dirs, files in os.walk(inImgPath):
        for fname in files:
            fullPath = os.path.join(root, fname)
            ocrToStr(fullPath, outTxtPath, fname,'kor') #한글+영어 추출(kor, eng , kor+eng)

    #OCR 추출 텍스트 파일 크기 확인
    for root, dirs, files in os.walk(outTxtPath):
        for fname in files:
            print("fileName : %s, %d" %(fname, float(os.path.getsize(os.path.join(root, fname)))))  #바이트 단위
            #fullPath = os.path.join(root, fname)
            #txtName = os.path.join(outTxtPath, fname.split('.')[0])