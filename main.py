import whisper

from tkinter import *
from tkinter import filedialog
import json


def info_audio():
    try:
        model = whisper.load_model("small")  # small.en (only en)
        song_path = filedialog.askopenfilename(title = "Select a File", 
                                                filetypes = (("Text files", 
                                                                "*.mp3*"), 
                                                            ("all files", 
                                                                "*.*")))

        result = model.transcribe(song_path)
        lyric = result["text"]

        with open("lyric.json", "w", encoding="utf-8") as f:
            json.dump(result,f, ensure_ascii=False, indent=4)

    except Exception as err:
        print(err)



def format_time(seconds):
    hours = int(seconds / 60 / 60)
    seconds -= hours*60*60
    minutes = int(seconds/60)
    seconds -= minutes*60
    milliseconds = ".000"
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}{milliseconds}"


def create_subtitle():
    with open('lyric.json') as file:
        data = json.load(file)

    with open("subtitle.sbv","w", encoding="utf-8") as f:
        for row in data['segments']:
            start = format_time(int(row['start']))
            end = format_time(int(row['end']))
            text = row['text']

            time = start + "," + end
            lyric = text

            f.writelines(time)
            f.writelines("\n")
            f.writelines(lyric)
            f.writelines("\n\n")


def main():
    print("loading...")
    info_audio()
    create_subtitle()

if __name__ == "__main__":
    main()