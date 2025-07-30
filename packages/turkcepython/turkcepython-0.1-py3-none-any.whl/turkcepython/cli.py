import sys
import os
import re

KOMUTLAR = {
   
    "eğer": "if",
    "değilse": "else",
    "eğerdeğil": "elif",
    "döngü": "while",
    "sınırlıdöngü": "for",
    "aralık": "range",
    "döndür": "return",
    "devam": "continue",
    "dur": "break",
    "içinde": "in",

    "doğru": "True",
    "yanlış": "False",
    "hiçbir": "None",

    "tanımla": "def",
    "sınıf": "class",
    "kendi": "self",
    "geç": "pass",

    "yazdır": "print",
    "girdi": "input",
    "tamsayi": "int",
    "ondalik": "float",
    "metin": "str",
    "liste": "list",
    "sozluk": "dict",
    "uzunluk": "len",
    "toplam": "sum",

    "dene": "try",
    "hata": "except",
    "sonunda": "finally",
    "hataver": "raise",

    "içeaktar": "import",
    "dan": "from",
    "olarak": "as",
}

def cevir(kod):
    for tr, en in KOMUTLAR.items():
        kod = re.sub(rf'\b{re.escape(tr)}\b', en, kod)
    return kod

def main():
    if len(sys.argv) != 2:
        print("Kullanım: turkcepython dosya.py")
        return

    dosya_adi = sys.argv[1]
    if not os.path.isfile(dosya_adi):
        print("Dosya bulunamadı.")
        return

    with open(dosya_adi, "r", encoding="utf-8") as f:
        kod = f.read()

    kod_python = cevir(kod)
    try:
        exec(kod_python, {})
    except Exception as e:
        print("Hata:", e)

if __name__ == "__main__":
    main()
