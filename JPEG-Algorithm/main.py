# python 3.9.5
from math import ceil

import cv2
import numpy as np

from functions import *

# Niceleme tablolarını tanımlayalım.
QTY = np.array([[16, 11, 10, 16, 24, 40, 51, 61],  # luminance quantization table - Parlaklık
                [12, 12, 14, 19, 26, 48, 60, 55],
                [14, 13, 16, 24, 40, 57, 69, 56],
                [14, 17, 22, 29, 51, 87, 80, 62],
                [18, 22, 37, 56, 68, 109, 103, 77],
                [24, 35, 55, 64, 81, 104, 113, 92],
                [49, 64, 78, 87, 103, 121, 120, 101],
                [72, 92, 95, 98, 112, 100, 103, 99]])

QTC = np.array([[17, 18, 24, 47, 99, 99, 99, 99],  # chrominance quantization table - Renklilik
                [18, 21, 26, 66, 99, 99, 99, 99],
                [24, 26, 56, 99, 99, 99, 99, 99],
                [47, 66, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99]])
# boyut tanımlama
windowSize = len(QTY)  # 8

# Resim okuma
imgOriginal = cv2.imread('marbles.bmp', cv2.IMREAD_COLOR)

# BGR'yi YCrCb'ye dönüştürme
# cv2.cvtColor() Görüntüyü bir renk uzayından diğerine dönüştürmek için kullanılan bir yöntemdir.
img = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2YCR_CB)
width = len(img[0]) # 1419 sütun
height = len(img)   # 1001 satır
# print(img.shape)    # (1001, 1419, 3)

y = np.zeros((height, width), np.float32) + img[:, :, 0]
cr = np.zeros((height, width), np.float32) + img[:, :, 1]
cb = np.zeros((height, width), np.float32) + img[:, :, 2]

# görüntünün sıkıştırılmadan önceki bit cinsinden boyutu  -> satır * sütun * 8
totalNumberOfBitsWithoutCompression = len(y) * len(y[0]) * 8 + len(cb) * len(cb[0]) * 8 + len(cr) * len(cr[0]) * 8
# print(totalNumberOfBitsWithoutCompression)   # 34090056


# kanal değerleri normalleştirilmelidir, bu nedenle 128 çıkarıyoruz.
y = y - 128
cr = cr - 128
cb = cb - 128

# 4: 2: 2 alt örnekleme kullanılır. (başka bir alt örnekleme şeması da kullanılabilir)
# bu nedenle krominans (renk) kanalları alt örneklenmelidir
# alt örnekleme faktörlerini hem yatay hem de dikey yönlerde tanımlıyoruz.
SSH, SSV = 2, 2

# 2x2 ortalama filtre kullanarak krominans kanallarını filtreleyelim. (başka bir filtre türü kullanılabilir)
# boxFilter() - ortalama alma bulanıklaştırma işlemine benzer; bir filtreye ikili bir görüntü uygular.
# ddepth - Çıktı görüntüsünün derinliğini temsil eden tamsayı türünde bir değişken.
# ksize - Bulanıklaştıran çekirdeğin boyutunu temsil eden bir Size nesnesi.
crf = cv2.boxFilter(cr, ddepth=-1, ksize=(2, 2))
cbf = cv2.boxFilter(cb, ddepth=-1, ksize=(2, 2))
crSub = crf[::SSV, ::SSH]
cbSub = cbf[::SSV, ::SSH]
# print(len(crf)) # 1001
# print(len(crSub)) # 501


# dolgu gerekip gerekmediğini kontrol ediyoruz,
# Eğer dolgu gerekli ise her kanalın DCT'sini sıfırlarla doldurmak için boş diziler tanımlayalım.
yWidth, yLength = ceil(len(y[0]) / windowSize) * windowSize, ceil(len(y) / windowSize) * windowSize
# print("y_width: ", ceil(len(y[0]) / windowSize) * windowSize)  # 1419 / 8 = 117.375 = 178 * 8 = 1424
# print("y_length", ceil(len(y) / windowSize) * windowSize)       # 1001 / 8 = 125.125 = 126 * 8 = 1008
if (len(y[0]) % windowSize == 0) and (len(y) % windowSize == 0):  # 1419 % 8 = 3 and 1001 % 8 = 1  (sıfırlarla doldurmamız gerek)
    yPadded = y.copy()
else:
    yPadded = np.zeros((yLength, yWidth))  # (1008, 1424) boyutlu sıfırlardan oluşan dizinin
    for i in range(len(y)):  # 1001
        for j in range(len(y[0])):  # 1419
            yPadded[i, j] += y[i, j]       # ilgili konumlarına eski verileri ekliyoruz. y[0,0]=(-128.0)=yPadded[0,0] gibi

# renklilik (chrominance) kanalları aynı boyutlara sahiptir, yani her ikisi de bir döngüde doldurulabilir
cWidth, cLength = ceil(len(cbSub[0]) / windowSize) * windowSize, ceil(len(cbSub) / windowSize) * windowSize # 712, 504
if (len(cbSub[0]) % windowSize == 0) and (len(cbSub) % windowSize == 0): # 710 % 8 = 6 and 501 % 8 = 5 (sıfırlarla doldurmamız gerek)
    crPadded = crSub.copy()
    cbPadded = cbSub.copy()
else:
    crPadded = np.zeros((cLength, cWidth)) # (504, 712)
    cbPadded = np.zeros((cLength, cWidth))
    for i in range(len(crSub)): # 501
        for j in range(len(crSub[0])): # 710
            crPadded[i, j] += crSub[i, j]
            cbPadded[i, j] += cbSub[i, j]

# her kanalın DCT'sini al
# üç boş matris tanımla
yDct, crDct, cbDct = np.zeros((yLength, yWidth)), np.zeros((cLength, cWidth)), np.zeros((cLength, cWidth))

# parlaklık kosinüs dönüşüm değerlerini hesaplamak için x ekseni ve y ekseni üzerindeki yineleme sayısı
hBlocksForY = int(len(yDct[0]) / windowSize)  # parlaklık için yatay yönde blok sayısı 178
vBlocksForY = int(len(yDct) / windowSize)  # parlaklık için dikey yönde blok sayısı 126
# krominans kanallarını hesaplamak için x ekseni ve y eksenindeki yineleme sayısı kosinüs dönüşümleri değerleri
hBlocksForC = int(len(crDct[0]) / windowSize)  # renklilik için yatay yönde blok sayısı 89
vBlocksForC = int(len(crDct) / windowSize)  # renklilik için dikey yönde blok sayısı 63

# nicelenmiş değerleri depolamak için 3 boş matris tanımlayın
yq, crq, cbq = np.zeros((yLength, yWidth)), np.zeros((cLength, cWidth)), np.zeros((cLength, cWidth))
# ve zikzaklar için 3 tane daha
yZigzag = np.zeros(((vBlocksForY * hBlocksForY), windowSize * windowSize))
crZigzag = np.zeros(((vBlocksForC * hBlocksForC), windowSize * windowSize))
cbZigzag = np.zeros(((vBlocksForC * hBlocksForC), windowSize * windowSize))

yCounter = 0
for i in range(vBlocksForY): # 126
    for j in range(hBlocksForY): # 178
        # Ayrık Kosinüs Dönüşümü
        yDct[i * windowSize: i * windowSize + windowSize, j * windowSize: j * windowSize + windowSize] = cv2.dct(
            yPadded[i * windowSize: i * windowSize + windowSize, j * windowSize: j * windowSize + windowSize])
        # Niceleme
        yq[i * windowSize: i * windowSize + windowSize, j * windowSize: j * windowSize + windowSize] = np.ceil(
            yDct[i * windowSize: i * windowSize + windowSize, j * windowSize: j * windowSize + windowSize] / QTY)
        # Zigzag
        yZigzag[yCounter] += zigzag(
            yq[i * windowSize: i * windowSize + windowSize, j * windowSize: j * windowSize + windowSize])
        yCounter += 1
yZigzag = yZigzag.astype(np.int16)

# blok sayısını hesaplamak için crq veya cbq kullanılabilir.
cCounter = 0
for i in range(vBlocksForC):
    for j in range(hBlocksForC):
        # cr
        crDct[i * windowSize: i * windowSize + windowSize, j * windowSize: j * windowSize + windowSize] = cv2.dct(
            crPadded[i * windowSize: i * windowSize + windowSize, j * windowSize: j * windowSize + windowSize])
        crq[i * windowSize: i * windowSize + windowSize, j * windowSize: j * windowSize + windowSize] = np.ceil(
            crDct[i * windowSize: i * windowSize + windowSize, j * windowSize: j * windowSize + windowSize] / QTC)
        crZigzag[cCounter] += zigzag(
            crq[i * windowSize: i * windowSize + windowSize, j * windowSize: j * windowSize + windowSize])
        #cb
        cbDct[i * windowSize: i * windowSize + windowSize, j * windowSize: j * windowSize + windowSize] = cv2.dct(
            cbPadded[i * windowSize: i * windowSize + windowSize, j * windowSize: j * windowSize + windowSize])
        cbq[i * windowSize: i * windowSize + windowSize, j * windowSize: j * windowSize + windowSize] = np.ceil(
            cbDct[i * windowSize: i * windowSize + windowSize, j * windowSize: j * windowSize + windowSize] / QTC)
        cbZigzag[cCounter] += zigzag(
            cbq[i * windowSize: i * windowSize + windowSize, j * windowSize: j * windowSize + windowSize])
        cCounter += 1
crZigzag = crZigzag.astype(np.int16)
cbZigzag = cbZigzag.astype(np.int16)

# her kanal için çalışma uzunluğu kodlamasını bulun
# daha sonra bir Huffman sözlüğü oluşturmak için her bileşenin frekansını alın
yEncoded = run_length_encoding(yZigzag)
yFrequencyTable = get_freq_dict(yEncoded)
yHuffman = find_huffman(yFrequencyTable)

crEncoded = run_length_encoding(crZigzag)
crFrequencyTable = get_freq_dict(crEncoded)
crHuffman = find_huffman(crFrequencyTable)

cbEncoded = run_length_encoding(cbZigzag)
cbFrequencyTable = get_freq_dict(cbEncoded)
cbHuffman = find_huffman(cbFrequencyTable)

# Her kanal için iletilecek bit sayısını hesaplayın
# ve bunları bir çıktı dosyasına yazın
file = open("CompressedImage.asfh", "w")
yBitsToTransmit = str()
for value in yEncoded:
    yBitsToTransmit += yHuffman[value]

crBitsToTransmit = str()
for value in crEncoded:
    crBitsToTransmit += crHuffman[value]

cbBitsToTransmit = str()
for value in cbEncoded:
    cbBitsToTransmit += cbHuffman[value]

if file.writable():
    file.write(yBitsToTransmit + "\n" + crBitsToTransmit + "\n" + cbBitsToTransmit)
file.close()

# Sıkıştırmadan Sonra Toplam Bit Sayısı
totalNumberOfBitsAfterCompression = len(yBitsToTransmit) + len(crBitsToTransmit) + len(cbBitsToTransmit)
# 2198128 + 457967 + 465325 = 3121420

print(
    "Compression Ratio is " + str(
        np.round(totalNumberOfBitsWithoutCompression / totalNumberOfBitsAfterCompression, 1)))

# Sıkıştırma Olmadan Toplam Bit Sayısı / Sıkıştırmadan Sonra Toplam Bit Sayısı = 34090056 / 3121420 = 10.9