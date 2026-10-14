import os
from PyPDF2 import PdfReader, PdfWriter

def extract_pdf_pages():
    # 1. Запит шляху до файлу
    # Метод strip() автоматично прибере пробіли та лапки, які з'являються при перетягуванні файлу в термінал
    pdf_path = input("Введіть шлях до великого PDF-файлу (можна перетягнути у вікно): ").strip(' \'"')
    
    if not os.path.exists(pdf_path):
        print(f"Помилка: Файл не знайдено за шляхом {pdf_path}")
        return

    # 2. Запит діапазону сторінок
    pages_input = input("Введіть номери сторінок для відділення (наприклад, 5 або 12-15): ").strip()
    
    # 3. Запит місця збереження
    output_folder = input("Введіть шлях до папки для збереження (натисніть Enter, щоб зберегти поруч із оригіналом): ").strip(' \'"')
    
    # Якщо користувач нічого не ввів, зберігаємо в ту саму папку, де лежить оригінал
    if not output_folder:
        output_folder = os.path.dirname(pdf_path)
        
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Аналіз введених сторінок
    start_page, end_page = 0, 0
    try:
        if '-' in pages_input:
            start_page, end_page = map(int, pages_input.split('-'))
        else:
            start_page = int(pages_input)
            end_page = start_page
    except ValueError:
        print("Помилка: Неправильний формат сторінок. Використовуйте числа, наприклад '5' або '12-15'.")
        return

    # Розрізання PDF
    try:
        print("\nОпрацювання файлу...")
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        total_pages = len(reader.pages)
        if start_page < 1 or end_page > total_pages or start_page > end_page:
            print(f"Помилка: Некоректний діапазон сторінок. У файлі всього {total_pages} сторінок.")
            return

        # PyPDF2 індексує сторінки з 0
        for i in range(start_page - 1, end_page):
            writer.add_page(reader.pages[i])
        
        # Формування назви нового файлу
        original_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_filename = os.path.join(output_folder, f"{original_name}_pages_{start_page}-{end_page}.pdf")
        
        with open(output_filename, "wb") as output_pdf:
            writer.write(output_pdf)
            
        print(f"Успіх! Відокремлені сторінки збережено за шляхом:\n{output_filename}")
        
    except Exception as e:
        print(f"Виникла помилка під час обробки PDF: {e}")

if __name__ == "__main__":
    extract_pdf_pages()