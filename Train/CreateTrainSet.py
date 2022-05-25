import csv
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
import glob
from random import randint,random


class CreateTrainChar:
  def __init__(self) -> None:
    with open("dictionary.txt", "r", encoding="ascii") as charListFp:
      charList = charListFp.readline()
    charList = list(charList)
    fontList = glob.glob("./Fonts/*")
    for char in charList:
      for fontPt in range(len(fontList)):
        for i in range(30):
          outImg = self.getCharImg(fontList[fontPt],char)
          outImg = self.ditherImg(outImg)
          cv2.imwrite(f"data/char_{ord(char)}_{fontPt}_{i}.png",outImg)
          pass
    self.writeCsv()

  def getCharImg(self, fontPath: str, char):
    font = ImageFont.truetype(fontPath, 48) # 定义字体，大小
    img = Image.new('L', (64, 64), 0) # 新建长宽64像素，背景色为黑色的画布对象
    wd,ht = font.getsize(char) # 获取字符宽高用来定位
    draw = ImageDraw.Draw(img) # 新建画布绘画对象
    draw.text(((64-wd)//2, (64-ht)//2), char, 255, font=font) # 在新建的对象中心画出白色文本
    img = np.array(img)
    return img
  
  def ditherImg(self,img:np.ndarray):
    def getRd(base:float,range:float):    #基于0的随机数
      return base + (random() * 2 - 1)*range
    wd = img.shape[1]; ht = img.shape[0]
    #透视变换矩阵
    s = 8
    perspMat = cv2.getPerspectiveTransform(np.asarray([[0,0],[0,wd],[ht,0],[ht,wd]],dtype="float32"),
      np.asarray([[getRd(0,s),getRd(0,s)],[getRd(0,s),getRd(wd,s)],[getRd(ht,s),getRd(0,s)],[getRd(ht,s),getRd(wd,s)]],dtype="float32"))
    img = cv2.warpPerspective(img,perspMat,(wd,ht),borderMode=cv2.BORDER_CONSTANT,borderValue=0)
    # img = cv2.normalize(img,None,randint(0,100),randint(155,255),cv2.NORM_MINMAX)       #随机亮度
    # size = randint(1,3)*2+1
    # img = cv2.GaussianBlur(img,ksize=(size,size),sigmaX=0)               #随机高斯模糊
    # img = (img + np.random.normal(loc=0,scale=random()*32,size=img.shape))    #随机高斯噪声
    img = np.clip(img,0,255).astype("uint8")
    return img

  def writeCsv(self):
    #文件名转csv数据
    fileList = glob.glob("data/*.png")
    csvItems = []
    for item in fileList:
      item = str.split(item,"_")[1:]
      item[2] = item[2][:-4]
      item.append(chr(int(item[0])))
      csvItems.append(item)

    #写入csv
    with open("allData.csv","w",encoding="ascii",newline="") as dataFp:
      writer = csv.writer(dataFp)
      writer.writerow(["code","font","sample","char"])
      writer.writerows(csvItems)

if __name__ == "__main__":
 CreateTrainChar()
