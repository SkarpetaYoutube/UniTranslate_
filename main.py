from transcribe import transcribe_audio
from translate import translate_text

def main():
    tekst_arabski = transcribe_audio("arabic_audio.mp3")
    polski_tekst = translate_text(tekst_arabski)

    with open("transkrypcja.txt", "w", encoding="utf-8") as f:
        f.write(polski_tekst)

    print("Gotowe! Zapisano do transkrypcja.txt")

if __name__ == "__main__":
    main()


