# ocr/ocr_reader.py

def extract_digits_from_image(image_path):
    """
    Şimdilik sadece test için, gerçek OCR yok.
    Daha sonra API kodunu buraya yazacağız.
    """
    # TODO: Buraya ChatGPT/Gemini OCR kodu gelecek
    text_output = ""
    return text_output


def image_to_grid(image_path):
    text = extract_digits_from_image(image_path)

    """
    Şimdilik dummy bir 9x9 grid döndürüyoruz.
    Daha sonra extract_digits_from_image çıktısını parse edeceğiz.
    """
    # TODO: text_output'u 9x9 listeye çevir
    grid = [[0 for _ in range(9)] for _ in range(9)]
    return grid
