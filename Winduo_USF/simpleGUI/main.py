import tkinter as tk
from tkinter import messagebox
import sys

class SimpleGUIInterpreter:
    def __init__(self):
        self.window = None
        self.widgets = {}
        self.script_globals = {}

    def parse_script(self, script_path):
        """解析脚本文件，提取函数定义并存储到全局变量中"""
        try:
            with open(script_path, "r", encoding="utf-8") as f:  # 显式指定 UTF-8 编码
                script = f.read()
            print(f"解析脚本文件: {script_path}")
            
            # 将解释器实例、tkinter 和 messagebox 注入到脚本的全局变量中
            self.script_globals["interpreter"] = self
            self.script_globals["tk"] = tk  # 注入 tkinter 模块
            self.script_globals["messagebox"] = messagebox  # 注入 messagebox 模块
            exec(script, self.script_globals)
        except FileNotFoundError:
            print(f"警告: 脚本文件 '{script_path}' 未找到，界面将仅支持静态显示。")
        except Exception as e:
            print(f"错误: 解析脚本文件时发生错误 - {e}")

    def interpret_gui(self, gui_file):
        """解析 GUI 文件并生成界面"""
        print(f"解析 GUI 文件: {gui_file}")
        try:
            with open(gui_file, "r", encoding="utf-8") as f:  # 显式指定 UTF-8 编码
                lines = f.readlines()

            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue  # 跳过空行和注释

                tokens = line.split()
                command = tokens[0]

                try:
                    if command == "script":
                        script_path = tokens[2]
                        self.parse_script(script_path)

                    elif command == "main":
                        # 创建主窗口
                        title = tokens[1].strip('"')
                        size = tokens[2].split("*")
                        width, height = int(size[0]), int(size[1])
                        self.create_main_window(title, width, height)

                    elif command == "button":
                        # 创建按钮
                        label = tokens[1].strip('"')
                        position = tokens[2].split("*")
                        x, y = int(position[0]), int(position[1])
                        action = tokens[3].split("=")[1] if len(tokens) > 3 else None
                        self.add_button(label, x, y, action)

                    elif command == "label":
                        # 创建标签
                        text = tokens[1].strip('"')
                        position = tokens[2].split("*")
                        x, y = int(position[0]), int(position[1])
                        self.add_label(text, x, y)

                    elif command == "entry":
                        # 创建单行文本框
                        position = tokens[1].split("*")
                        x, y = int(position[0]), int(position[1])
                        self.add_entry(x, y)

                    elif command == "text":
                        # 创建多行文本框
                        position = tokens[1].split("*")
                        x, y = int(position[0]), int(position[1])
                        width, height = int(tokens[2]), int(tokens[3])
                        self.add_text(x, y, width, height)

                    elif command == "checkbox":
                        # 创建复选框
                        text = tokens[1].strip('"')
                        position = tokens[2].split("*")
                        x, y = int(position[0]), int(position[1])
                        self.add_checkbox(text, x, y)

                    elif command == "radiobutton":
                        # 创建单选按钮
                        text = tokens[1].strip('"')
                        position = tokens[2].split("*")
                        x, y = int(position[0]), int(position[1])
                        group = tokens[3]
                        value = tokens[4]
                        self.add_radiobutton(text, x, y, group, value)

                    elif command == "dropdown":
                        # 创建下拉菜单
                        position = tokens[1].split("*")
                        x, y = int(position[0]), int(position[1])
                        options = tokens[2:]
                        self.add_dropdown(x, y, options)

                except (ValueError, IndexError) as e:
                    print(f"警告: 解析命令时发生错误 - 行='{line}', 错误={e}")
                    continue  # 跳过当前命令，继续解析下一行

        except Exception as e:
            print(f"错误: 解析 GUI 文件时发生错误 - {e}")
        
        # 确保主窗口被创建
        if self.window is None:
            print("警告: GUI 文件解析失败，创建默认主窗口...")
            self.create_main_window("默认窗口", 800, 600)

    def create_main_window(self, title, width, height):
        """创建主窗口"""
        print(f"创建主窗口: 标题={title}, 宽度={width}, 高度={height}")
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(f"{width}x{height}")

    def add_button(self, label, x, y, action):
        """添加按钮"""
        print(f"添加按钮: 文本={label}, 位置=({x}, {y}), 动作={action}")
        button = tk.Button(self.window, text=label, command=lambda: self.execute_action(action))
        button.place(x=x, y=y)

    def add_label(self, text, x, y):
        """添加标签"""
        print(f"添加标签: 文本={text}, 位置=({x}, {y})")
        label = tk.Label(self.window, text=text)
        label.place(x=x, y=y)

    def add_entry(self, x, y):
        """添加单行文本框"""
        print(f"添加单行文本框: 位置=({x}, {y})")
        entry = tk.Entry(self.window)
        entry.place(x=x, y=y)
        self.widgets[f"entry_{len(self.widgets)}"] = entry  # 使用唯一键存储

    def add_text(self, x, y, width, height):
        """添加多行文本框"""
        print(f"添加多行文本框: 位置=({x}, {y}), 宽度={width}, 高度={height}")
        text = tk.Text(self.window, width=width, height=height)
        text.place(x=x, y=y)
        self.widgets["text"] = text

    def add_checkbox(self, text, x, y):
        """添加复选框"""
        print(f"添加复选框: 文本={text}, 位置=({x}, {y})")
        checkbox_var = tk.BooleanVar()
        checkbox = tk.Checkbutton(self.window, text=text, variable=checkbox_var)
        checkbox.place(x=x, y=y)
        self.widgets[text] = checkbox_var

    def add_radiobutton(self, text, x, y, group, value):
        """添加单选按钮"""
        print(f"添加单选按钮: 文本={text}, 位置=({x}, {y}), 组={group}, 值={value}")
        if group not in self.widgets:
            self.widgets[group] = tk.StringVar()
        radiobutton = tk.Radiobutton(self.window, text=text, variable=self.widgets[group], value=value)
        radiobutton.place(x=x, y=y)

    def add_dropdown(self, x, y, options):
        """添加下拉菜单"""
        print(f"添加下拉菜单: 位置=({x}, {y}), 选项={options}")
        dropdown_var = tk.StringVar()
        dropdown = tk.OptionMenu(self.window, dropdown_var, *options)
        dropdown.place(x=x, y=y)
        self.widgets["dropdown"] = dropdown_var

    def execute_action(self, action):
        """执行按钮绑定的动作"""
        if action is None:
            print("警告: 按钮未绑定任何动作。")
            return

        if action in self.script_globals:
            func = self.script_globals[action]
            print(f"执行动作: {action}")
            func()
        else:
            print(f"警告: 动作 '{action}' 未定义，无法执行。")

    def run(self):
        """运行 GUI 主循环"""
        print("启动 GUI 主循环...")
        if self.window is None:
            print("错误: 主窗口未创建，无法启动主循环。")
            return
        self.window.mainloop()

def main():
    if len(sys.argv) != 2:
        print("用法: python simple_gui_interpreter.py <winduo_file>")
        sys.exit(1)
			
    winduo_file = sys.argv[1]
    interpreter = SimpleGUIInterpreter()
    interpreter.interpret_gui(winduo_file)
    interpreter.run()
	
# 示例使用
if __name__ == "__main__":
    main()