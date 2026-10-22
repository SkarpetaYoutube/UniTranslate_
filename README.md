# Whisper Translator

Mój projekt transkrypcji audio z GUI oparty na Whisper, PyQt5 i deep-translator.

## Wymagania

- Python 3.10+
- FFmpeg dostępny w `PATH` albo w lokalnym katalogu `ffmpeg/bin`

> `ffmpeg-python` z `requirements.txt` nie instaluje samego programu FFmpeg. Whisper nadal potrzebuje binarki `ffmpeg` do odczytu plików audio.

## Jak uruchomić

```bash
pip install -r requirements.txt
python main.py
```

Aplikacja obsługuje pliki MP3, WAV i M4A.

## Status

- ✅ Działa w PyCharm
- ❌ `.exe` nie działa jeszcze poprawnie z PyInstallerem

## Rozwiązywanie problemów

- **Brak polecenia `ffmpeg`**: zainstaluj FFmpeg i dodaj jego katalog `bin` do zmiennej `PATH`, ewentualnie umieść go w `ffmpeg/bin` w katalogu projektu. Uruchom ponownie aplikację.
- **Pierwsze uruchomienie trwa długo**: Whisper przy pierwszym użyciu może pobierać model `base`; potrzebne jest połączenie z internetem.
- **Błąd tłumaczenia**: usługa GoogleTranslator wymaga połączenia z internetem; sprawdź sieć i spróbuj ponownie.
- **Brak rozpoznanej mowy**: sprawdź, czy plik zawiera wyraźną mowę w wybranym języku źródłowym.
- **Brak obsługi GPU**: Whisper może działać na CPU, ale przetwarzanie będzie wolniejsze.

## Obsługa przetwarzania

Przed rozpoczęciem aplikacja sprawdza istnienie wybranego pliku oraz dostępność
FFmpeg. Długie transkrypcje są tłumaczone w fragmentach do 4500 znaków; jeśli
to możliwe, podział wypada na spacji. Podział może ograniczyć kontekst tłumaczenia.
Pusta odpowiedź usługi jest zgłaszana jako błąd.

Podczas pracy wybór pliku i języków jest zablokowany. Okno można zamknąć po
zakończeniu pracy wątku; próba wcześniejszego zamknięcia wyświetla komunikat.
Aplikacja nie obsługuje anulowania trwającego zadania.

## Testy regresji

Z katalogu projektu uruchom:

```bash
python -m unittest discover -s tests -v
```

Testy korzystają wyłącznie z biblioteki standardowej Pythona. Sprawdzają
dzielenie tekstu, błędne odpowiedzi usługi i logikę zamykania okna oraz
przywracania kontrolek, bez pobierania modeli i wywoływania sieci.
Nie zastępują testu integracyjnego GUI, FFmpeg i rzeczywistego tłumaczenia.
