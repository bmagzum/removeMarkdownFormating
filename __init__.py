import os
import re

from anki.hooks import addHook
from aqt import mw
from aqt.editor import Editor
from aqt.qt import *


def get_key():
    conf = mw.addonManager.getConfig(__name__)
    return conf.get("hotkey", "Ctrl+Alt+R") if conf else "Ctrl+Alt+R"


def format_key(k):
    return QKeySequence(k).toString(QKeySequence.SequenceFormat.NativeText)


def removeMarkdownFormating(editor: Editor):
    js = """
    var sel = window.getSelection().toString();
    var cleaned = sel.replace(/\\$\\$|\\$|\\*\\*|\\*|&nbsp;/g, "");
    document.execCommand('insertText', false, cleaned);
    """
    editor.web.eval(js)


def setupEditorButtons(buttons, editor: Editor):
    key = get_key()
    b = editor.addButton(
        os.path.join(os.path.dirname(__file__), "dollar-alt.png"),
        "removeMarkdownFormating",
        removeMarkdownFormating,
        tip=f"Remove Markdown Formatting ({format_key(key)})",
        keys=key,
    )
    buttons.append(b)
    return buttons


addHook("setupEditorButtons", setupEditorButtons)
