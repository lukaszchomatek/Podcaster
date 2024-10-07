import os
from openai import OpenAI
from pydub import AudioSegment

def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def save_response_to_file(response, file_path='middle_phase.txt'):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(response)

def text_to_speech(input_text, output_file='output.mp3', voice_mode='alloy', api_key_from_file=''):
    client = OpenAI(api_key=api_key_from_file)
    print(f'Generating audio content for text: "{input_text}"')
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice_mode,
        input=input_text
    )
    print(f'Audio content generated for text: "{input_text}"')
    with open(output_file, 'wb') as out:
        out.write(response.read())
    print(f'Audio content written to file "{output_file}"')


def process_lines_from_middle_phase(output_folder='output_audio', api_key_from_file=''):
    os.makedirs(output_folder, exist_ok=True)
    lines = read_txt_file('middle_phase.txt').splitlines()
    print("Loaded Lines:\n", lines)
    for index, line in enumerate(lines):
        if line.strip():
            if line.startswith("**MIKE:**") or line.startswith("**MIKE**:"):
                voice_mode = 'onyx'
                content = line.replace("**MIKE:**", "").replace("**MIKE**:", "").strip()
            elif line.startswith("**JOHN:**") or line.startswith("**JOHN**:"):
                voice_mode = 'alloy'
                content = line.replace("**JOHN:**", "").replace("**JOHN**:", "").strip()
            elif line.startswith("**KATE:**") or line.startswith("**KATE**:"):
                voice_mode = 'nova'
                content = line.replace("**KATE:**", "").replace("**KATE**:", "").strip()
            else:
                continue

            output_file = os.path.join(output_folder, f"{index + 1}.mp3")
            text_to_speech(content, output_file=output_file, voice_mode=voice_mode, api_key_from_file=api_key_from_file) 

def combine_audio_files(input_folder='output_audio', output_file='final_podcast.mp3'):
    audio_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.mp3')], key=lambda x: int(x.split('.')[0]))
    combined = AudioSegment.empty()
    for audio_file in audio_files:
        audio_path = os.path.join(input_folder, audio_file)
        audio_segment = AudioSegment.from_mp3(audio_path)
        combined += audio_segment
    combined.export(output_file, format='mp3')
    print(f'Combined audio content written to file "{output_file}"')

if __name__ == "__main__":
     api_key = read_txt_file('key.txt')

     process_lines_from_middle_phase('output_audio', api_key)

     combine_audio_files()