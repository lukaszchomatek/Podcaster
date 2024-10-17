import os
import fitz
import docx
from openai import OpenAI

def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def read_pdf_file(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf.load_page(page_num)
            text += page.get_text()
    return text


def read_docx_file(file_path):
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


def read_file(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == ".txt":
        return read_txt_file(file_path)
    elif file_extension == ".pdf":
        return read_pdf_file(file_path)
    elif file_extension == ".docx":
        return read_docx_file(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")


def read_all_files_from_sources():
    folder_path = 'sources'
    all_text = ""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                file_text = read_file(file_path)
                all_text += filename + "\n\n" + file_text + "\n###\n\n"
            except ValueError as e:
                print(e)
    return all_text

def read_prompt():
    return read_txt_file('prompt.txt')

def get_script(text_content_for_script, prompt, api_key_from_file):
    client = OpenAI(api_key=api_key_from_file)
    response = client.chat.completions.create(
        #feel free to use gtp-4o-mini for English podcasts
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "text": prompt,
                        "type": "text"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text_content_for_script
                    }
                ]
            }
        ],
        temperature=1,
        max_tokens=16383,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
    )
    return response.choices[0].message.model_dump()['content']


def save_response_to_file(response, file_path='middle_phase.txt'):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(response)

if __name__ == "__main__":
     api_key = read_txt_file('key.txt')
     text_content = read_all_files_from_sources()
     print("Loaded Text:\n", text_content)

     prompt = read_prompt()
     print("Loaded Prompt:\n", prompt)

     response = get_script(text_content, prompt, api_key)
     print("Generated Response:\n", response)

     save_response_to_file(response)