import fitz, pytesseract, io
from PIL import Image

def pdf_scans_to_txt(pdf_path, txt_path, language='rus+eng'): 
    pdf_document = fitz.open(pdf_path)
    text_content = []
    
    print(f"Количество страниц: {len(pdf_document)}")
    for page_num in range(len(pdf_document)):
        print(f"Обработка страницы {page_num + 1}...")
        page = pdf_document[page_num]

        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat)
        
        img_data = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_data))
        
        page_text = pytesseract.image_to_string(image, lang=language)
        
        text_content.append(f"--------------------------- Страница {page_num + 1} ---------------------------\n")
        text_content.append(page_text)
    
    pdf_document.close()
    
    with open(txt_path, 'w', encoding='utf-8') as file:
        file.write(''.join(text_content))
    

if __name__ == "__main__":
    input_pdf = "data/documents/books/Polnoe_rukovodstvo_po_vizivaniyu.pdf"
    output_txt = "data/documents/txt/Polnoe_rukovodstvo_po_vizivaniyu.txt"
    pdf_scans_to_txt(input_pdf, output_txt, language='rus+eng')