import os
import sys
import whisper
from deep_translator import GoogleTranslator
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QLabel, QTextEdit, QFileDialog, QComboBox,
                             QVBoxLayout, QHBoxLayout, QWidget, QProgressBar)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QFont

# Dodaj ffmpeg do PATH
ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg", "bin")
os.environ["PATH"] += os.pathsep + ffmpeg_path


class TranscriptionThread(QThread):
    """Osobny wątek żeby GUI się nie zawieszało"""
    finished = pyqtSignal(str, str)
    progress = pyqtSignal(str)

    def __init__(self, audio_path, source_lang, target_lang):
        super().__init__()
        self.audio_path = audio_path
        self.source_lang = source_lang
        self.target_lang = target_lang

    def run(self):
        try:
            self.progress.emit("Ładuję model Whisper...")
            model = whisper.load_model("base")  # base = szybszy dla GUI

            self.progress.emit("Transkrybuję audio...")
            result = model.transcribe(self.audio_path, language=self.source_lang)
            source_text = result["text"]

            self.progress.emit("Tłumaczę tekst...")
            translator = GoogleTranslator(source=self.source_lang, target=self.target_lang)
            translated_text = translator.translate(source_text)

            self.progress.emit("Gotowe!")
            self.finished.emit(source_text, translated_text)
        except Exception as e:
            self.progress.emit(f"BŁĄD: {str(e)}")


class WhisperApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.audio_file = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Whisper Translator')
        self.setGeometry(100, 100, 800, 600)

        # Widget główny
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Tytuł
        title = QLabel('🎙️ WHISPER TRANSLATOR')
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; padding: 20px;")
        layout.addWidget(title)

        # Przycisk wyboru pliku
        self.btn_select = QPushButton('📁 Wybierz plik audio (MP3)')
        self.btn_select.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 15px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.btn_select.clicked.connect(self.select_file)
        layout.addWidget(self.btn_select)

        # Label wybranego pliku
        self.label_file = QLabel('Nie wybrano pliku')
        self.label_file.setStyleSheet("padding: 10px; color: #7f8c8d;")
        layout.addWidget(self.label_file)

        # Wybór języków
        lang_layout = QHBoxLayout()

        self.label_source = QLabel('Język źródłowy:')
        lang_layout.addWidget(self.label_source)

        self.combo_source = QComboBox()
        self.combo_source.addItems(['ar - Arabski', 'en - Angielski', 'pl - Polski',
                                    'es - Hiszpański', 'fr - Francuski', 'de - Niemiecki'])
        lang_layout.addWidget(self.combo_source)

        self.label_target = QLabel('Język docelowy:')
        lang_layout.addWidget(self.label_target)

        self.combo_target = QComboBox()
        self.combo_target.addItems(['pl - Polski', 'en - Angielski', 'ar - Arabski',
                                    'es - Hiszpański', 'fr - Francuski', 'de - Niemiecki'])
        lang_layout.addWidget(self.combo_target)

        layout.addLayout(lang_layout)

        # Przycisk transkrypcji
        self.btn_transcribe = QPushButton('▶️ TRANSKRYBUJ I TŁUMACZ')
        self.btn_transcribe.setEnabled(False)
        self.btn_transcribe.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.btn_transcribe.clicked.connect(self.start_transcription)
        layout.addWidget(self.btn_transcribe)

        # Status
        self.label_status = QLabel('Gotowy do pracy')
        self.label_status.setStyleSheet("padding: 10px; color: #27ae60; font-weight: bold;")
        layout.addWidget(self.label_status)

        # Tekst oryginalny
        self.label_original = QLabel('TEKST ORYGINALNY:')
        self.label_original.setFont(QFont('Arial', 12, QFont.Bold))
        layout.addWidget(self.label_original)

        self.text_original = QTextEdit()
        self.text_original.setReadOnly(True)
        self.text_original.setStyleSheet("background-color: #ecf0f1; padding: 10px;")
        layout.addWidget(self.text_original)

        # Tłumaczenie
        self.label_translated = QLabel('TŁUMACZENIE:')
        self.label_translated.setFont(QFont('Arial', 12, QFont.Bold))
        layout.addWidget(self.label_translated)

        self.text_translated = QTextEdit()
        self.text_translated.setReadOnly(True)
        self.text_translated.setStyleSheet("background-color: #e8f8f5; padding: 10px;")
        layout.addWidget(self.text_translated)

        # Przycisk zapisu
        self.btn_save = QPushButton('💾 Zapisz do pliku')
        self.btn_save.setEnabled(False)
        self.btn_save.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.btn_save.clicked.connect(self.save_to_file)
        layout.addWidget(self.btn_save)

        central_widget.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik audio", "", "Audio Files (*.mp3 *.wav *.m4a)")
        if file_path:
            self.audio_file = file_path
            self.label_file.setText(f'✅ {os.path.basename(file_path)}')
            self.btn_transcribe.setEnabled(True)

    def start_transcription(self):
        if not self.audio_file:
            return

        # Wyciągnij kod języka (np. "ar" z "ar - Arabski")
        source_lang = self.combo_source.currentText().split(' - ')[0]
        target_lang = self.combo_target.currentText().split(' - ')[0]

        # Wyłącz przyciski
        self.btn_transcribe.setEnabled(False)
        self.btn_select.setEnabled(False)

        # Uruchom transkrypcję w osobnym wątku
        self.thread = TranscriptionThread(self.audio_file, source_lang, target_lang)
        self.thread.progress.connect(self.update_status)
        self.thread.finished.connect(self.transcription_finished)
        self.thread.start()

    def update_status(self, message):
        self.label_status.setText(message)

    def transcription_finished(self, original, translated):
        self.text_original.setText(original)
        self.text_translated.setText(translated)
        self.btn_save.setEnabled(True)

        # Włącz przyciski z powrotem
        self.btn_transcribe.setEnabled(True)
        self.btn_select.setEnabled(True)

    def save_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Zapisz jako", "tlumaczenie.txt", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("TEKST ORYGINALNY:\n")
                f.write(self.text_original.toPlainText() + "\n\n")
                f.write("---\n\n")
                f.write("TŁUMACZENIE:\n")
                f.write(self.text_translated.toPlainText())
            self.label_status.setText(f'✅ Zapisano: {os.path.basename(file_path)}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WhisperApp()
    window.show()
    sys.exit(app.exec_())


# Użycie
audio_file = "ElevenLabs_2025-11-09T12_15_28_Alex - expressive narrator_gen_sp100_s50_sb75_se0_m2.mp3"
polish = transcribe_and_translate(audio_file, "en", "pl")