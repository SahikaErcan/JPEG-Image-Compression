from collections import Counter
import numpy as np

"""
Amacı matris elemanlarını düşük frekanstan yüksek frekansa dogru artacak biçimde dizmektir.
Böylece ilk sıradaki eleman DC katsayı olacaktır. Kuantalama blogunda sıfırlanan elemanlar ise 
burada yan yana gelecektir.Bu durum kodlama kısmında kolaylık saglayacaktır.
"""
def zigzag(matrix: np.ndarray) -> np.ndarray:
    # nicelenmiş bir bloğun zigzagını hesaplar.
    # yatay ve dikey durumlar için değişkenleri tanımlıyoruz
    h = 0
    v = 0
    v_min = 0
    h_min = 0
    v_max = matrix.shape[0]
    h_max = matrix.shape[1]
    i = 0
    output = np.zeros((v_max * h_max))

    while (v < v_max) and (h < h_max):
        if ((h + v) % 2) == 0:  # yukarı çık
            if v == v_min:
                output[i] = matrix[v, h]  # İlk satır
                if h == h_max:
                    v = v + 1
                else:
                    h = h + 1
                i = i + 1
            elif (h == h_max - 1) and (v < v_max):  # son sütun
                output[i] = matrix[v, h]
                v = v + 1
                i = i + 1
            elif (v > v_min) and (h < h_max - 1):  # diğer tüm durumlar
                output[i] = matrix[v, h]
                v = v - 1
                h = h + 1
                i = i + 1
        else:  # aşağı git
            if (v == v_max - 1) and (h <= h_max - 1):  # son satır
                output[i] = matrix[v, h]
                h = h + 1
                i = i + 1
            elif h == h_min:  # ilk sütun
                output[i] = matrix[v, h]
                if v == v_max - 1:
                    h = h + 1
                else:
                    v = v + 1
                i = i + 1
            elif (v < v_max - 1) and (h > h_min):  # diğer tüm durumlar
                output[i] = matrix[v, h]
                v = v + 1
                h = h - 1
                i = i + 1
        if (v == v_max - 1) and (h == h_max - 1):  # sağ alt eleman
            output[i] = matrix[v, h]
            break

    return output


def trim(array: np.ndarray) -> np.ndarray:
    """
    trim_zeros(): diziden baştaki ve/veya sondaki sıfırları kırpın.
    trim_zeros işlevinin boş bir dizi döndürmesi durumunda, DC bileşeni olarak kullanmak için diziye bir sıfır ekleyin
    """
    trimmed = np.trim_zeros(array, 'b') # arkadaki sıfırları siler
    if len(trimmed) == 0:
        trimmed = np.zeros(1)
    return trimmed

"""
 ***** AC Dizi Uzunlugu (Run Length) Kodlama *****
Kuantalama ve zig-zag bloklarından sonra içinde birçok sıfır içeren dizi elde edilmişti.
Bu aşamada her 8x8’lik blokta yer alan 63 adet AC katsayı kodlanır. 
Örnek olarak 57, 45, 0, 0, 0, 0, 23, 0, -30, -16, 0, 0, 1, 0 .... 0 şeklinde bir dizi varsa 
AC dizi uzunlugu kodlaması şu şekilde olacaktır: (0,57); (0,45); (4,23); (1,-30); (0,-16); (2,1); EOB.
EOB (End of Block) kodu özel olarak belirlenmiştir. Eger zig-zag blogundan gelen vektörün kalan 
elemanlarının hepsi 0 ise EOB blogu konularak bütün sıfırların gönderilmesi engellenebilir. 
Eger zig-zag blogundan gelen vektör 0 ile bitmiyorsa, yani son eleman 0 degil ise, EOB koyulmaz.
"""
def run_length_encoding(array: np.ndarray) -> list:    # çalışma uzunluğu kodlaması
    """
    zikzakları temsil eden ara akışı bulur
    DC bileşenlerinin formatı <size><amplitude (genişlik)> şeklindedir.
    AC bileşenleri için biçim <run_length, size> <Amplitude of non-zero> şeklindedir.
    :param numpy.ndarray array: dizideki zikzak vektörleri
    """
    encoded = list()
    run_length = 0
    eob = ("EOB",)

    for i in range(len(array)):
        for j in range(len(array[i])):
            trimmed = trim(array[i]) # arkadaki sıfırlar silindi.
            if j == len(trimmed):
                encoded.append(eob)  # Arkadaki sıfırların olduğu konuma geldiğinde EOB  .
                break
            if i == 0 and j == 0:  # ilk DC bileşeni için
                encoded.append((int(trimmed[j]).bit_length(), trimmed[j]))
# int.bit_length(): İşaret ve baştaki sıfırlar hariç, bir tamsayıyı ikili sistemde temsil etmek için gereken bit sayısını döndürür.
            elif j == 0:  # DC bileşenleri arasındaki farkı hesaplamak için
                diff = int(array[i][j] - array[i - 1][j])
                if diff != 0:
                    encoded.append((diff.bit_length(), diff))
                else:
                    encoded.append((1, diff))
                run_length = 0
            elif trimmed[j] == 0:  # sıfır olması durumunda çalışma_uzunluğunu bir artırın
                run_length += 1
            else:  # AC bileşenlerinin ara akış gösterimi
                encoded.append((run_length, int(trimmed[j]).bit_length(), trimmed[j]))
                run_length = 0
            # EOB gönder
        if not (encoded[len(encoded) - 1] == eob):
            encoded.append(eob)
    return encoded


def get_freq_dict(array: list) -> dict:
    """
    tuşların dizinin değerleri olduğu ve değerlerin frekansları olduğu bir sözlük döndürür.
    :param numpy.ndarray array: dizi olarak ara akış
    :return: frekans tablosu
    """
    data = Counter(array) # Nesneleri anahtar ve değer olarak sayan bir sözlüktür.
    result = {k: d / len(array) for k, d in data.items()}
    return result

def find_huffman(p: dict) -> dict:

    # Yalnızca iki simgenin temel durumu, keyfi olarak 0 veya 1 atayın; frekans önemli değil
    if len(p) == 2:
        return dict(zip(p.keys(), ['0', '1']))

    # Olası en düşük çifti birleştirerek yeni bir dağıtım oluşturun
    p_prime = p.copy()
    a1, a2 = lowest_prob_pair(p)
    p1, p2 = p_prime.pop(a1), p_prime.pop(a2)
    p_prime[a1 + a2] = p1 + p2

    # Yeni dağıtımda kodu yineleyin ve oluşturun
    c = find_huffman(p_prime)
    ca1a2 = c.pop(a1 + a2)
    c[a1], c[a2] = ca1a2 + '0', ca1a2 + '1'

    return c


def lowest_prob_pair(p):
    # En düşük olasılıkla p dağılımından sembol çiftini döndür
    sorted_p = sorted(p.items(), key=lambda x: x[1])
    return sorted_p[0][0], sorted_p[1][0]
