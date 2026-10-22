"""Offline regression tests; no Qt, model downloads or translation API needed."""
import ast
import pathlib
import types
import unittest
from unittest.mock import Mock

SOURCE = pathlib.Path(__file__).resolve().parents[1] / "main.py"
tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
selected = []
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "translate_text":
        selected.append(node)
    if isinstance(node, ast.ClassDef) and node.name == "WhisperApp":
        selected.extend(n for n in node.body if isinstance(n, ast.FunctionDef)
                        and n.name in {"closeEvent", "transcription_stopped"})
namespace = {}
exec(compile(ast.Module(body=selected, type_ignores=[]), str(SOURCE), "exec"), namespace)
translate_text = namespace["translate_text"]


class TranslationTests(unittest.TestCase):
    def test_chunk_limits_and_preservation(self):
        for text in ("abc def ghi jkl", "abcdefghijklmn", "مرحبا بالعالم " * 4):
            with self.subTest(text=text):
                translator = Mock()
                translator.translate.side_effect = lambda value: value
                translate_text(text, translator, max_chars=5)
                chunks = [call.args[0] for call in translator.translate.call_args_list]
                self.assertEqual("".join(chunks), text)
                self.assertTrue(all(len(chunk) <= 5 for chunk in chunks))

    def test_empty_input(self):
        translator = Mock()
        self.assertEqual(translate_text("", translator), "")
        translator.translate.assert_not_called()

    def test_invalid_limit(self):
        with self.assertRaises(ValueError):
            translate_text("abc", Mock(), max_chars=0)

    def test_empty_service_response(self):
        for response in (None, "", "   "):
            with self.subTest(response=response):
                with self.assertRaises(ValueError):
                    translate_text("abc", Mock(translate=Mock(return_value=response)))

    def test_service_error_propagates(self):
        with self.assertRaises(RuntimeError):
            translate_text("abc", Mock(translate=Mock(side_effect=RuntimeError("offline"))))


class LifecycleTests(unittest.TestCase):
    def test_close_waits_for_worker(self):
        for running in (False, True):
            app = types.SimpleNamespace(
                thread=Mock(isRunning=Mock(return_value=running)), label_status=Mock())
            event = Mock()
            namespace["closeEvent"](app, event)
            self.assertEqual(event.ignore.called, running)
            self.assertEqual(event.accept.called, not running)

    def test_close_before_first_job(self):
        event = Mock()
        namespace["closeEvent"](types.SimpleNamespace(thread=None), event)
        event.accept.assert_called_once()

    def test_controls_restored_after_thread_exit(self):
        app = types.SimpleNamespace(**{name: Mock() for name in
            ("btn_transcribe", "btn_select", "combo_source", "combo_target")})
        namespace["transcription_stopped"](app)
        for widget in vars(app).values():
            widget.setEnabled.assert_called_once_with(True)


if __name__ == "__main__":
    unittest.main()
