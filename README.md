# JPEG-Image-Compression
```
VIDEO: https://youtu.be/LzXKH4CnWhI
```

JPEG yaygın olarak kullanılan kayıplı sıkıştırma algoritmasıdır. Kayıplı sıkıştırma da kalite faktörüne bağlı olarak görüntünün sıkıştırma oranı ve bozulma miktarı istenilen seviyede ayarlanabilmektedir. Resmin kalitesinden bir miktar ödün verilerek sıkıştırma uygulanır. Böylece dosya boyutu küçültülür. JPEG'ler birçok rengin bulunduğu ve birbirine derece derece geçtiği, belirgin sınırlar içermeyen fotoğraflar için idealdir.
JPEG sıkıştırma yöntemi, aşağıdaki adımlardan oluşmaktadır.

1. Öncelikle bir görüntü YCbCr renk uzayına dönüştürülür ve 8x8’lik bloklara ayrılır.
2. Her bloğa Ayrık Kosinüs Dönüşümü(AKD) uygulanır.
3. AKD katsayıları bazı kuantalama kurallarına göre kuantize edilir.
4. Entropi kodlama yöntemi gerçekleştirilir.

![image](https://user-images.githubusercontent.com/72580629/227977819-a4c8c487-d464-4024-b0fe-d8052d18a34c.png)

JPEG Algoritmasının detaylarına bakmadan önce jpeg in yararlandığı **insan gözlerini inceleyelim.**

**Retina** da ışığı algılayan ve ışığa tepki veren çubuk ve koni isimli iki tür hücre bulunur. Çubuk hücreleri renge duyarlı değildir, siyah-beyaz görmeyi sağlar ve düşük ışık koşullarında görmek için kritik öneme sahiptirler. Koni hücreleri ise renk alıcılarına sahiptirler ve kırmızı, yeşil ve mavi renklere duyarlıdırlar. Ayrıca her bir gözde yaklaşık olarak 110 milyon çubuk hücresi varken 6 milyon da koni hücresi vardır. Sonuç olarak gözlerimiz bir görüntünün parlaklığına ve karanlığına daha çok duyarlıdır.

Bir çiçek görüntüsünü inceleyelim. Resme baktığımızda sadece parlaklığı gösteren siyah beyaz versiyon, tam renkli görüntü kadar ayrıntılı görünüyor.

![image](https://user-images.githubusercontent.com/72580629/227978004-52e99ae4-cb59-4246-9047-1042bfc10c26.png)

Sadece renge veya belirginliğe baktığımızda aynı görüntünün önemli ölçüde daha az ayrıntılı göründüğünü görüyoruz.

![image](https://user-images.githubusercontent.com/72580629/228059535-87c72bfe-7d1e-4833-90f5-4a62ea73c30f.png)


## Renk Uzayı Dönüşümü

Orijinal görüntü piksellerden oluşur ve bu piksellerin her birinin 0 ile 255 değer aralığına sahip kırmızı, yeşil ve mavi bir RGB bileşeni vardır. RGB Renk uzayında her bir pikseldeki renk değeri ayrı kanallar olarak saklanır. Örneğin 8 bit bir videoda her bir piksel için 3 byte (8 bit x 3 kanal) renk değeri saklanır. RGB renk uzayında ayrıca bir parlaklık bilgisi yoktur. Bu nedenle renk ve parlaklık bilgisini birbirinden ayrı sıkıştırmak mümkün değildir. Çoğu JPEG algoritması uygulaması, RGB yerine YUV - Y’/Cb/Cr kullanır. Y parlaklığı (siyah-beyaz), U mavi tabanlı renkliliği, V kırmızı tabanlı renkliliği temsil eder. YUV, RGB gibi tam anlamıyla bir renk uzayı değildir, RGB renk uzayını göstermenin farklı bir yoludur. Bu yöntemde renk bilgisi, parlaklık bilgisinden ayrıldığı için bağımsız işlemlerle farklı oranlarda sıkıştırılabilir. Bir sonraki adımda önemli miktarda veriyi kaldırır.

![image](https://user-images.githubusercontent.com/72580629/228059820-ef96fa6e-75a2-4a13-9927-7181c45d8516.png)

Görsele baktığımızda iyi bir tespit için hem mavi hem de kırmızı renkli birleşen görüntülerini alırız ve bu görüntüleri ikiye iki piksel bloğuna böleriz. Ardından her bir blok için ortalama değeri hesaplayarak tekrarlanan bilgileri kaldırır ve görüntüyü küçültürüz. Böylece 4 piksellik bloğunun her bir ortalama değeri tek bir piksel kaplayacaktır.

![image](https://user-images.githubusercontent.com/72580629/228059875-03d108ce-e3f7-45b9-9e66-1bd5e6ee48ce.png)

Sonuç olarak gözlerimizin kırmızı ve mavi belirginlikleri algılamada zayıf olduğu bilgisi ile bileşen görüntüler orijinal boyutun dörtte birine küçültülür. Ancak parlaklık aynı kalır.  

![image](https://user-images.githubusercontent.com/72580629/228060020-fc2985c4-28cb-43a0-973f-84b462022a3b.png)

Görüntümüz sadece yaptığımız bu iki adımlık işlem ile orijinal boyutun yarısıdır. 

![image](https://user-images.githubusercontent.com/72580629/228060107-27a53f78-ce40-4f81-87c7-1afe9467150e.png)

İnsan gözü küçük bir alanda yüksek frekanslı parlaklık değişikliklerini görmekte oldukça kötü olduğundan, bu JPEG'de çok kullanışlıdır, bu nedenle frekans miktarını esasen azaltabiliriz ve insan gözü farkı anlayamaz. Sonuç olarak kalitede neredeyse hiç gözle görülür azalma olmayan yüksek oranda sıkıştırılmış bir görüntü elde ederiz.

## **Ayrık Kosinüs Dönüşümü ve Kuantalama**

Ayrık kosinüs ve kuantalama adımları, görüntünün her bölümünden geçer ve yüksek frekansta değişen belirginlik veya parlaklığa sahip alanları bulur. Örnek olarak parlaklık bileşeni görüntüsünü kullanalım. Aynı işlemin iki belirginlik bileşeniyle de gerçekleştiğini bilmeliyiz. Öncelikle tüm görüntü her biri 0 ile 255 arasında değerlerden oluşan 64 piksellik 8x8 lik bloklara ayrılır. 8 bitlik bir görüntü için, orijinal blokta her öğe [0,255] aralığında yer alır. Orijinal bloktaki her öğeden aralığın orta noktası (128 değeri) çıkarıldıktan sonra sıfır etrafında ortalanan veri aralığı üretilir, böylece değiştirilen aralık [0,255]'ten [-128,127]'ye kaydırılır. Burada -128 siyahı 127 ise beyazı temsil eder. 

**Daha sonra her bloğa Ayrı Kosinüs Dönüşümü uygulayarak elde edilen bloğu sıkıştırmak için kuantalama kullanır.**

Bu ifademizi detaylandıralım.

Ayrık kosinüs dönüşümü, farklı frekanslarda salınan kosinüs fonksiyonlarının toplamı cinsinden sonlu bir veri noktası dizisini ifade eder. Bir kosinüs işlevinin tanım aralığı 1 ile -1 arasındadır. 

![image](https://user-images.githubusercontent.com/72580629/228060362-dd85fcd3-9811-4934-beeb-6a10b84c6a6e.png)

Ayrık Kosinüs Dönüşümü, ayrık veri noktalarını kosinüs dalgalarının bir kombinasyonuna dönüştürme yöntemidir. Bir görüntüyü bir grup kosinüs haline dönüştürmek için zaman harcamak oldukça işe yaramaz gibi görünüyor. Onları çizmeye başlayana kadar bu pek mantıklı değil. Diyelim ki burada standart kosinüs dalgası olan bu kosinüs dalgasını aldık. Sonra daha yüksek bir frekans olan başka bir kosinüs dalgası elde ettik. Şimdi iki dalgamız var. Onları bir araya getirirsek, elde ettiğimiz şey bu iki dalganın birleşiminden oluşan başka bir dalga olacaktır. Görselde de görüldüğü gibi bu iki dalganın yarısını elde ederiz. 

![image](https://user-images.githubusercontent.com/72580629/228060462-5e71c1d5-58ac-438d-8506-cfe43177f5f1.png)

**Yani her ikisi de ağırlıklı ve bu aslında her ikisinin de ortalamasıdır. Bunların ağırlığını da değiştirebiliriz. Böylece çoğunlukla  görselde gördüğümüz gibi  daha yüksek frekanslı olan dalgaya sahip olabiliriz ve sonunda düşük frekanslı dalganın da etkisi ile farklı dalgalar elde ederiz. Böylece her dalga çıktının küçük bir bileşenini temsil eder. Dalganın frekansı yükseldikçe, uğraştığımız sinyalin frekans kısmı da artar. JPEG ile görüntünün genel durumunu bozmadan, bazı yüksek frekans sinyallerinden kurtulabileceği savunulur. Bu sadece iki bileşenli tek boyutlu ayrık bir kosinüs dönüşümüdür.**

İşin matematiğine baktığımız da, eğer elimizde 8 uzunluğunda bir sinyalimiz varsa onu farklı frekanslarda 8 kosinüs dalgası kullanarak temsil ederiz. Aynı durum bir görüntü için de geçerlidir. JPEG de her görüntü 8x8 piksel gruba bölünür ve bu piksel gruplarının her biri ayrı ayrı kosinüs dönüşümü ile ayrı ayrı kodlanır. 

**Kosinüs fonksiyonlarının 8x8 matrisi şöyle görünür:**

![image](https://user-images.githubusercontent.com/72580629/228060534-3f6f298c-964a-4ffc-97fa-2e7d5de29e53.png)

8x8 piksel olarak gruplanan herhangi bir görüntüyü üreten 64 kosinüs dalgalarını gösteriyor. Sol üst köşe en düşük, sağ alt köşe ise en yüksek frekans kosinüs fonksiyonunu temsil eder. Bunun bize söylediği şey, çoğu görüntünün büyük miktarda düşük frekanslı bilgi ve az miktarda yüksek frekanslı bilgi içerdiğidir. Düşük frekanslı olanlar, yüksek frekanslı verilere göre çok daha büyük bir etkiye sahiptir. Her ayrık kosinüs dönüşüm matrisinin sağ alt bileşenlerini 0'a çevirirsek, ortaya çıkan görüntü yine aynı görünür çünkü yüksek frekanslı değişiklikleri gözlemlemede kötüyüz, düşük frekansları daha iyi görüyoruz.

Örneğin beyaz kutunun yanındaki iki kutuyu ele alalım. Bu iki dalganın ayrı ayrı yarısını alırsak, sol tarafının sağ tarafına göre daha parlak olduğu bir kare görüntüsü elde ederiz çünkü bu iki dalgayı topluyoruz. 

![image](https://user-images.githubusercontent.com/72580629/228060854-3061cb13-bbcf-41a2-86c0-ec76c617d307.png)

Herhangi bir tür 8x8 lik görüntü oluşturmak için yapmamız gereken aynı anda bunların hepsinin bir kombinasyonunu oluşturmaktır. Bunların her biri katsayı adı verilen bir şeye dayanarak ağırlıklandırılır. Bu, bireysel blokların her birinin bütüne katkısını temsil eden bir sayıdır. Ayrık kosinüs dönüşümü ile yaptığımız şey, temel olarak bu dalgalar için katsayıları hesaplamaktır.

JPEG'in kayıplı bir sıkıştırma algoritması olduğunu biliyoruz ama şimdiye kadar kayıplı bir şey yapmadık. Sadece 8x8 blok YUV bileşenlerini hiçbir bilgi kaybı olmadan 8x8 blok kosinüs fonksiyonlarına dönüştürdük. Kuantalama adımı ile verideki fazlalıklar atılır kayıplar burada meydana gelir. Kuantalama ile daha az önemli olan yüksek frekanslı ayrık kosinüs dönüşüm katsayılarının çoğunu sıfıra indirme amaçlanır. Sıfırların sayısı ne kadar fazla olursa görüntünün sıkıştırma oranı o kadar yüksek olacaktır. Yüksek frekanslı bilgileri bir kez kaybettiğinizde, ortaya çıkan JPEG görüntüsünden tam orijinal görüntüyü yeniden oluşturamazsınız. Gereken sıkıştırma seviyesine bağlı olarak, bazı genel niceleme matrisleri kullanılır. DCT katsayı matrisini niceleme matrisiyle eleman bazında böleriz, sonucu bir tamsayıya yuvarlarız ve nicelenmiş matrisi elde ederiz. Bir örnek üzerinden gidelim.

* **DCT matrisi:**

![image](https://user-images.githubusercontent.com/72580629/228061117-aec7306c-4abe-4b3c-abbd-48fa4a6c2aa1.png)

* **Niceleme matrisi  (yaygın):**

![image](https://user-images.githubusercontent.com/72580629/228061183-45d9be58-ea8f-403a-a685-16a5c27ac81f.png)

* **Elde edilen nicelenmiş matris:**

![image](https://user-images.githubusercontent.com/72580629/228061261-c6d9f993-0fa4-463c-b4ff-819f196332aa.png)


İnsanlar yüksek frekanslı bilgileri göremese de, 8x8 görüntü parçalarından çok fazla bilgi kaldırırsanız, genel görüntü bloklu görünür. Bu kuantize matriste, ilk değer DC değeri olarak adlandırılır ve değerlerin geri kalanı AC değerleridir. Tüm nicelenmiş matrislerden DC değerlerini alırsak ve yeni bir görüntü oluşturursak, esasen orijinal görüntünün 1/8 çözünürlüğünde bir küçük resim elde ederiz.

## Zig-zag

![image](https://user-images.githubusercontent.com/72580629/228061449-bfbd1be2-c975-40ca-b2ee-8c78df4412ec.png)

Bu nicelenmiş matrise sahip olduğumuzu hayal edelim. Zig-Zag kodlamanın çıktısı [15 14 13 12 11 10 9 8 0 0 ... 0] şeklinde  olacaktır.

![image](https://user-images.githubusercontent.com/72580629/228061393-bcf547d6-0102-4b5f-afd3-2f38224b02c9.png)

Bu kodlama tercih edilir çünkü düşük frekanslı (en önemli) bilgilerin çoğu nicelemeden sonra matrisin başında depolanır ve zig-zag kodlama bunların hepsini 1 boyutlu matrisin başlangıcında depolar. Bu, bir sonraki adımda gerçekleşen sıkıştırma için kullanışlıdır.

## Huffman Algoritması

Veri sıkıştırmak için kullanılan bir yöntemdir. Kayıpsız (lossless) olarak veriyi sıkıştırıp tekrar açmak için kullanılır. Huffman kodlamasının en büyük avantajlarından birisi kullanılan karakterlerin frekanslarına göre bir kodlama yapmasıdır. Bu sayede sık kullanılan karakterler küçük bitler ile nadir kullanılan karakterleri ise daha büyük bitler ile eşleyerek ikili ağaçta düzenler. Böylece verinin daha az yer kaplamasını sağlar.

JPEG'de, Huffman kodlamasını kullanarak DCT (Ayrık Kosinüs Dönüşümü) bilgilerini depoluyoruz. Bir JPEG en fazla 4 Huffman tablosu içerir ve bunlar "Huffman Tablosunu Tanımla" bölümünde saklanır ( `0xffc4` ile başlayan). DCT katsayıları 2 farklı Huffman tablosunda saklanmaktadır. Biri sadece zig-zag tablolarından DC değerlerini içerir diğeri ise zig-zag tablolarından AC değerlerini içerir. Bu, kod çözme işlemimizde iki ayrı matristen DC ve AC değerlerini birleştirmemiz gerekeceği anlamına gelir. Parlaklık ve krominans kanalı için DCT bilgisi ayrı ayrı depolanır, bu nedenle 2 set DC ve 2 set AC bilgimiz var, bu da bize toplam 4 Huffman tablosu verir.







* **Kaynaklar:**

    - [https://www.youtube.com/watch?v=Q2aEzeMDHMA&ab_channel=Computerphile](https://www.youtube.com/watch?v=Q2aEzeMDHMA&ab_channel=Computerphile)
    - [https://www.youtube.com/watch?v=Kv1Hiv3ox8I&ab_channel=BranchEducation](https://www.youtube.com/watch?v=Kv1Hiv3ox8I&ab_channel=BranchEducation)
    - [https://yasoob.me/posts/understanding-and-writing-jpeg-decoder-in-python/](https://yasoob.me/posts/understanding-and-writing-jpeg-decoder-in-python/)
    - [https://www.youtube.com/watch?v=JsTptu56GM8&ab_channel=TomScott](https://www.youtube.com/watch?v=JsTptu56GM8&ab_channel=TomScott)
    - [https://www.youtube.com/watch?v=0me3guauqOU&ab_channel=Reducible](https://www.youtube.com/watch?v=0me3guauqOU&ab_channel=Reducible)
    - [https://github.com/yasoob/Baseline-JPEG-Decoder/blob/master/decoder.py](https://github.com/yasoob/Baseline-JPEG-Decoder/blob/master/decoder.py)
    - [https://github.com/abhinav-TB/JPEG-IMAGE-COMPRESSION](https://github.com/abhinav-TB/JPEG-IMAGE-COMPRESSION)
    - [https://github.com/changhsinlee/software-for-science/tree/master/2019-04-11-jpeg-algorithm](https://github.com/changhsinlee/software-for-science/tree/master/2019-04-11-jpeg-algorithm)
    - [https://www.youtube.com/watch?v=PHrYZUN-pW0&ab_channel=SoftwareforScience](https://www.youtube.com/watch?v=PHrYZUN-pW0&ab_channel=SoftwareforScience)
    - [https://www.geeksforgeeks.org/image-compression-using-huffman-coding/](https://www.geeksforgeeks.org/image-compression-using-huffman-coding/)
    - [https://inst.eecs.berkeley.edu/~ee123/sp16/Sections/JPEG_DCT_Demo.html](https://inst.eecs.berkeley.edu/~ee123/sp16/Sections/JPEG_DCT_Demo.html)
