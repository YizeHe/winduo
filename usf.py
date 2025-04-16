# usf.py - 用户友好的脚本函数库
import tkinter as tk
from tkinter import messagebox
import os


def get_entry_value(interpreter, index):
    """获取指定索引的单行文本框的值"""
    entry = interpreter.widgets.get(f"entry_{index}")
    return entry.get() if entry else None

def set_entry_value(interpreter, index, value):
    """设置指定索引的单行文本框的值"""
    entry = interpreter.widgets.get(f"entry_{index}")
    if entry:
        entry.delete(0, "end")
        entry.insert(0, value)

def clear_entries(interpreter):
    """清空所有单行文本框"""
    for widget in interpreter.widgets.values():
        if isinstance(widget, tk.Entry):
            widget.delete(0, "end")

def get_text_value(interpreter):
    """获取多行文本框的值"""
    text = interpreter.widgets.get("text")
    return text.get("1.0", "end-1c") if text else None

def set_text_value(interpreter, value):
    """设置多行文本框的值"""
    text = interpreter.widgets.get("text")
    if text:
        text.delete("1.0", "end")
        text.insert("1.0", value)

def show_message(title, message):
    """显示消息框"""
    messagebox.showinfo(title, message)

def test_print(message):
    print(message)