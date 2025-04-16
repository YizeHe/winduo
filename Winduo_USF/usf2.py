# usf.py - 用户友好的脚本函数库
import tkinter as tk
from tkinter import messagebox


class USF:
    def __init__(self, interpreter=None):
        """
        初始化 USF 类。
        :param interpreter: 包含 widgets 的解释器对象（字典结构）。
        """
        self.interpreter = interpreter

    def get_entry_value(self, index):
        """获取指定索引的单行文本框的值"""
        entry = self.interpreter.widgets.get(f"entry_{index}")
        return entry.get() if entry else None

    def set_entry_value(self, index, value):
        """设置指定索引的单行文本框的值"""
        entry = self.interpreter.widgets.get(f"entry_{index}")
        if entry:
            entry.delete(0, "end")
            entry.insert(0, value)

    def clear_entries(self):
        """清空所有单行文本框"""
        for widget in self.interpreter.widgets.values():
            if isinstance(widget, tk.Entry):
                widget.delete(0, "end")

    def get_text_value(self):
        """获取多行文本框的值"""
        text = self.interpreter.widgets.get("text")
        return text.get("1.0", "end-1c") if text else None

    def set_text_value(self, value):
        """设置多行文本框的值"""
        text = self.interpreter.widgets.get("text")
        if text:
            text.delete("1.0", "end")
            text.insert("1.0", value)

    @staticmethod
    def show_message(title, message):
        """显示消息框"""
        messagebox.showinfo(title, message)

    @staticmethod
    def test_print(message):
        print(message)


# 示例代码
if __name__ == "__main__":
    # 创建一个简单的 Tkinter 窗口和解释器模拟
    class Interpreter:
        def __init__(self):
            self.widgets = {}
            self.root = tk.Tk()
            self.root.title("USF 示例")

            # 添加两个单行文本框
            self.widgets["entry_1"] = tk.Entry(self.root)
            self.widgets["entry_1"].pack()

            self.widgets["entry_2"] = tk.Entry(self.root)
            self.widgets["entry_2"].pack()

            # 添加一个多行文本框
            self.widgets["text"] = tk.Text(self.root, height=5, width=30)
            self.widgets["text"].pack()

            # 添加一个按钮用于测试功能
            tk.Button(self.root, text="测试 USF 功能", command=self.test_usf).pack()

        def test_usf(self):
            # 创建 USF 实例
            usf = USF(self)

            # 设置单行文本框的值
            usf.set_entry_value(1, "这是第一个输入框")
            usf.set_entry_value(2, "这是第二个输入框")

            # 获取并打印单行文本框的值
            print("Entry 1:", usf.get_entry_value(1))
            print("Entry 2:", usf.get_entry_value(2))

            # 设置多行文本框的值
            usf.set_text_value("这是一个多行文本框的内容")

            # 获取并打印多行文本框的值
            print("Text:", usf.get_text_value())

            # 显示消息框
            usf.show_message("测试完成", "USF 功能测试成功！")

            # 清空所有单行文本框
            usf.clear_entries()

        def run(self):
            self.root.mainloop()


    # 运行示例
    interpreter = Interpreter()
    interpreter.run()