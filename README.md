# JPEG-Image-Compression
JPEG yaygın olarak kullanılan kayıplı sıkıştırma tekniğidir. Kayıplı sıkıştırma da kalite faktörüne bağlı olarak görüntünün sıkıştırma oranı ve bozulma miktarı istenilen seviyede ayarlanabilmektedir. 

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/cc74ea4f-063c-4e95-a1bd-0e27dcf69495/Untitled.png)

JPEG sıkıştırma yöntemi, aşağıdaki adımlardan oluşmaktadır.

1. Öncelikle bir görüntü YCbCr renk uzayına dönüştürülür ve 8x8’lik bloklara ayrılır.
2. Her bloğa Ayrık Kosinüs Dönüşümü(AKD) uygulanır.
3. AKD katsayıları bazı kuantalama kurallarına göre kuantize edilir.
4. Entropi kodlama yöntemi gerçekleştirilir.

JPEG Algoritmasının detaylarına bakmadan önce jpeg in yararlandığı **insan gözlerini inceleyelim.**

**Retina** da ışığı algılayan ve ışığa tepki veren çubuk ve koni isimli iki tür hücre bulunur. Çubuk hücreleri renge duyarlı değildir, siyah-beyaz görmeyi sağlar ve düşük ışık koşullarında görmek için kritik öneme sahiptirler. Koni hücreleri ise renk alıcılarına sahiptirler ve kırmızı, yeşil ve mavi renklere duyarlıdırlar. Ayrıca her bir gözde yaklaşık olarak 110 milyon çubuk hücresi varken 6 milyon da koni hücresi vardır. Sonuç olarak gözlerimiz bir görüntünün parlaklığına ve karanlığına daha çok duyarlıdır.

Bir çiçek görüntüsünü inceleyelim. Resme baktığımızda sadece parlaklığı gösteren siyah beyaz versiyon, tam renkli görüntü kadar ayrıntılı görünüyor.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/032ccbf2-06eb-4ade-9541-09ac7877b5e1/Untitled.png)

Sadece renge veya belirginliğe baktığımızda aynı görüntünün önemli ölçüde daha az ayrıntılı göründüğünü görüyoruz.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/617ea3fe-06fa-474d-aa5a-c21d24cc085d/Untitled.png)

JPEG algoritmasının bu görüntüyü nasıl kullandığını inceleyelim.
