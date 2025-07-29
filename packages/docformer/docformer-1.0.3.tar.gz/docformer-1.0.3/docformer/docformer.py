import os
import sys
import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
import shutil
import webbrowser

class DocFormerEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("DocFormer Editor")
        self.root.geometry("1000x600")
        
        # 配置文件路径
        self.config_file = os.path.join(os.path.expanduser('~'), '.docformer_config.json')
        
        # 创建主框架
        self.main_frame = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.main_frame.pack(expand=True, fill='both')
        
        # 创建左侧目录框架
        self.toc_frame = ttk.Frame(self.main_frame, width=200)
        self.main_frame.add(self.toc_frame, weight=1)
        
        # 创建右侧编辑框架
        self.edit_frame = ttk.Frame(self.main_frame)
        self.main_frame.add(self.edit_frame, weight=3)
        
        # 创建菜单栏
        self.menu_bar = tk.Menu(root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="新建", command=self.new_file)
        self.file_menu.add_command(label="打开", command=self.open_file)
        self.file_menu.add_command(label="保存", command=self.save_file)
        self.file_menu.add_command(label="导出为HTML", command=self.export_to_html)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="退出", command=root.quit)
        self.menu_bar.add_cascade(label="文件", menu=self.file_menu)
        
        # 添加工具菜单
        self.tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.tools_menu.add_command(label="清理安装", command=self.clean_installation)
        self.menu_bar.add_cascade(label="工具", menu=self.tools_menu)
        
        root.config(menu=self.menu_bar)
        
        # 创建目录显示区域
        self.toc_label = ttk.Label(self.toc_frame, text="目录")
        self.toc_label.pack(pady=5)
        
        # 创建目录文本框和滚动条
        self.toc_text = tk.Text(self.toc_frame, wrap=tk.WORD, width=30)
        self.toc_text.pack(expand=True, fill='both', padx=5, pady=5)
        self.toc_text.config(state='disabled')
        
        # 配置编号颜色
        self.toc_text.tag_config("blue_number", foreground="#0077CC")
        
        # 配置目录文本框的标签
        self.toc_text.tag_configure("toc_title", font=("TkDefaultFont", 12, "bold"))
        self.toc_text.tag_configure("toc_separator", foreground="gray")
        self.toc_text.tag_configure("toc_item", foreground="blue")
        
        # 创建目录滚动条
        self.toc_scrollbar = ttk.Scrollbar(self.toc_frame, command=self.toc_text.yview)
        self.toc_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.toc_text.config(yscrollcommand=self.toc_scrollbar.set)
        
        # 创建文本编辑器
        self.text_editor = tk.Text(self.edit_frame, wrap=tk.WORD, undo=True, padx=32, pady=20)
        self.text_editor.pack(expand=True, fill='both')
        
        # 设置编辑器背景色和边框
        self.text_editor.config(
            bg="white", 
            relief=tk.FLAT, 
            borderwidth=0
        )
        
        # 使用tag_configure设置选中样式，确保不被覆盖
        self.text_editor.tag_configure(tk.SEL,
            background="#c3dffa",  # 选中背景色-蓝色
            foreground="#000000",  # 选中文本色-白色
            selectbackground="#c3dffa",  # 选中背景色-蓝色
            selectforeground="#000000",  # 选中文本色-白色
        )
        
        # 配置基本样式标签
        self.text_editor.tag_configure("title", 
            spacing1=30, spacing3=5,  # 减少spacing3让分隔线更靠近下方标题
            font=("TkDefaultFont", 24, "bold"),
            )  # 浅灰色分隔线
        self.text_editor.tag_configure("body_text", 
            spacing1=8, spacing3=8, 
            lmargin1=32, lmargin2=32)
        self.text_editor.tag_configure("block", 
            spacing1=10, spacing3=10)
        
        # 创建编辑器滚动条
        self.scrollbar = ttk.Scrollbar(self.edit_frame, command=self.text_editor.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_editor.config(yscrollcommand=self.scrollbar.set)
        
        # 绑定文本修改事件
        self.text_editor.bind('<<Modified>>', self.on_text_modified)
        
        # 绑定目录点击事件
        self.toc_text.bind('<Button-1>', self.on_toc_click)
        self.toc_text.bind('<Enter>', lambda e: self.toc_text.config(cursor="hand2"))
        self.toc_text.bind('<Leave>', lambda e: self.toc_text.config(cursor=""))
        
        # 绑定快捷键
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-e>', lambda e: self.export_to_html())
        self.root.bind('<Control-i>', lambda e: self.open_file())
        
        self.current_file = None
        self.current_file_type = None  # 'docformer' 或 'html'
        self.toc_data = []  # 存储目录数据
        self.toc_positions = {}  # 存储目录项对应的文本位置
        self.font_sizes = {}  # 存储每行的字号
        self.block_ranges = {}  # 存储每个标题块的范围
        self.current_hover_block = None  # 当前鼠标悬浮的块
        
        # 字号配置
        self.font_config = {
            'body_size': 18,        # 正文字号
            'min_title_size': 20,   # 最低级标题字号
            'size_step': 2          # 每级标题字号差
        }
        
        # 创建工具栏
        self.toolbar = ttk.Frame(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # 添加工具栏按钮
        ttk.Button(self.toolbar, text="导出HTML", command=self.export_to_html).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="保存", command=self.save_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="字号设置", command=self.show_font_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="插入图片", command=self.insert_image).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="插入文件", command=self.insert_file).pack(side=tk.LEFT, padx=2)
        
        # 添加提示标签
        self.hint_label = ttk.Label(self.edit_frame, text="第一行将作为文档总标题", foreground="gray")
        self.hint_label.pack(side=tk.TOP, pady=2)
        
        # 在UI初始化完成后加载配置
        self.load_config()
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

    

    def on_text_modified(self, event=None):
        if self.text_editor.edit_modified():
            content = self.text_editor.get(1.0, tk.END)
            self.generate_toc_from_content(content)
            self.update_font_sizes()
            self.text_editor.edit_modified(False)

    def update_font_sizes(self):
        # 清除所有标签
        for tag in self.text_editor.tag_names():
            if tag.startswith('font_') or tag.startswith('hover_') or tag.startswith('block_') or tag.startswith('separator_'):
                self.text_editor.tag_remove(tag, '1.0', tk.END)
        
        # 获取所有行
        lines = self.text_editor.get('1.0', tk.END).split('\n')
        max_indent = 0
        
        # 计算最大缩进
        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                max_indent = max(max_indent, indent)
        
        # 配置样式标签
        self.text_editor.tag_configure("title", 
            font=("TkDefaultFont", 24, "bold"),
            spacing1=30, spacing3=30,
            lmargin1=0, lmargin2=0)
        
        self.text_editor.tag_configure("body_text",
            font=("TkDefaultFont", 18),
            spacing1=8, spacing3=8,
            lmargin1=32, lmargin2=32)
        
        # 处理每一行
        line_number = 1
        previous_indent = -1
        
        for line in lines:
            if line.strip():
                start = f"{line_number}.0"
                end = f"{line_number}.end"
                indent = len(line) - len(line.lstrip())
                
                # 确定行类型并应用相应样式
                if line_number == 1:
                    # 文档总标题
                    self.text_editor.tag_add('title', start, end)
                elif line.lstrip().startswith('\\'):
                    # 正文内容
                    self.text_editor.tag_add('body_text', start, end)
                    self.text_editor.tag_add('block', start, end)
                else:
                    # 其他标题
                    #self.text_editor.tag_add('body_text', start, end)
                    self.text_editor.tag_add('block', start, end)
                    
                    # 在标题之间添加分隔线
                    #if previous_indent != -1 and indent <= previous_indent:
                    #    sep_pos = f"{line_number}.0"
                    #    self.text_editor.tag_add('separator', sep_pos)
                
                
            line_number += 1
        
        # 分析每个文本块的层级关系
        blocks = []
        current_block = []
        last_indent = -1
        
        for i, line in enumerate(lines, 1):
            if line.strip():
                # 如果以"\"开头，视为正文，不创建新block
                if line.lstrip().startswith('\\'):
                    if current_block:  # 如果有当前block，则附加到其中
                        current_block.append((i, line, current_block[-1][2] if current_block else 0))  # 使用上级缩进级别
                        # 设置正文字号为18
                        self.text_editor.tag_add("body_text", f"{i}.0", f"{i}.end")
                        self.text_editor.tag_configure("body_text", font=("TkDefaultFont", 18))
                        continue
                    
                                    # 计算缩进，确保最多比上一级多一级
                indent = len(line) - len(line.lstrip())
                if last_indent != -1:
                    # 限制缩进增加不超过一级
                    if indent > last_indent + 4:  # 4个空格为一级
                        indent = last_indent + 4
                    
                if last_indent != -1 and last_indent != indent:
                    if current_block:
                        blocks.append(current_block)
                        current_block = []
                current_block.append((i, line, indent))
                last_indent = indent
            elif current_block:
                blocks.append(current_block)
                current_block = []
        
        if current_block:
            blocks.append(current_block)
        
        # 应用字号标签和块范围
        current_block = 0
        block_start = 1
        last_indent = -1
        self.block_ranges = {}
        
        for block in blocks:
            block_indent = block[0][2]  # 获取块的缩进级别
            has_lower_level = False
            
            # 检查是否有更低级别的块
            for other_block in blocks:
                if other_block[0][2] > block_indent:
                    has_lower_level = True
                    break
            
            # 设置字号和缩进
            for i, line, indent in block:
                # 处理以"\"开头的行（正文内容）
                if line.lstrip().startswith('\\'):
                    font_size = self.font_config['body_size']
                elif not has_lower_level:
                    # 如果块之后没有更低级别的文本，则视为最低级标题
                    font_size = self.font_config['min_title_size']
                else:
                    # 根据缩进级别计算字号
                    font_size = self.font_config['min_title_size'] + (max_indent - indent) * self.font_config['size_step']
                
                # 第一行作为总标题，字号加一级
                if i == 1:
                    font_size += self.font_config['size_step']
                    
                # 创建并配置标签，设置字号和缩进
                tag = f"font_{font_size}"
                start = f"{i}.0"
                end = f"{i}.end"
                # 设置第一行和后续行的缩进，确保换行后文本紧贴缩进
                self.text_editor.tag_configure(tag, font=("TkDefaultFont", font_size),
                                            lmargin1=indent*10, lmargin2=indent*10,
                                            wrap="word")
                self.text_editor.tag_add(tag, start, end)
            
            # 处理块范围
            if block:
                start_line = block[0][0]
                end_line = block[-1][0]
                self.block_ranges[current_block] = (start_line, end_line)
                current_block += 1
        
        # 配置悬浮效果标签
        for block_id in self.block_ranges:
            self.text_editor.tag_configure(f"hover_{block_id}", background="#F0F0F0")

    def on_toc_click(self, event):
        # 获取点击位置的行号
        index = self.toc_text.index(f"@{event.x},{event.y}")
        line = int(index.split('.')[0])
        
        # 跳过目录标题和分隔线
        if line <= 2:
            return
            
        # 获取对应的文本位置
        toc_line = line - 2  # 减去标题和分隔线的行数
        if toc_line in self.toc_positions:
            target_pos = self.toc_positions[toc_line]
            self.text_editor.see(target_pos)
            self.text_editor.mark_set(tk.INSERT, target_pos)
            # 高亮显示目标行
            self.text_editor.tag_remove("highlight", "1.0", tk.END)
            self.text_editor.tag_add("highlight", target_pos, f"{int(target_pos.split('.')[0])}.end")
            self.text_editor.tag_configure("highlight", background="#FFFF00")
            # 1秒后移除高亮
            self.root.after(2000, lambda: self.text_editor.tag_remove("highlight", "1.0", tk.END))

    def new_file(self):
        self.text_editor.delete(1.0, tk.END)
        self.toc_text.config(state='normal')
        self.toc_text.delete(1.0, tk.END)
        self.toc_text.config(state='disabled')
        self.current_file = None
        self.current_file_type = None
        self.toc_data = []
        self.toc_positions = {}
        self.font_sizes = {}
        self.block_ranges = {}
        self.current_hover_block = None
        self.root.title("DocFormer Editor - 新文件")

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("DocFormer files", "*.docformer"),
                ("HTML files", "*.html"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            try:
                file_ext = os.path.splitext(file_path)[1].lower()
                if file_ext == '.html':
                    self.open_html(file_path)
                else:
                    self.open_docformer(file_path)
                self.save_config()
            except Exception as e:
                messagebox.showerror("错误", f"无法打开文件: {str(e)}")

    def open_docformer(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(1.0, content)
        
        # 生成目录和更新字号
        self.generate_toc_from_content(content)
        self.update_font_sizes()
        
        self.current_file = file_path
        self.current_file_type = 'docformer'
        self.root.title(f"DocFormer Editor - {os.path.basename(file_path)}")

    def open_html(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 提取目录
            toc_match = re.search(r'<div class="toc">(.*?)</div>', content, re.DOTALL)
            if toc_match:
                toc_content = toc_match.group(1)
                self.toc_text.config(state='normal')
                self.toc_text.delete(1.0, tk.END)
                self.toc_text.insert(tk.END, toc_content)
                self.toc_text.config(state='disabled')
            
            # 提取正文内容
            content_match = re.search(r'<div class="content">(.*?)</div>', content, re.DOTALL)
            if content_match:
                text_content = content_match.group(1)
                # 移除HTML标签，保留文本
                text_content = re.sub(r'<[^>]+>', '', text_content)
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(1.0, text_content)
            
            self.current_file = file_path
            self.current_file_type = 'html'
            self.root.title(f"DocFormer Editor - {os.path.basename(file_path)}")
            
            # 更新字号
            self.update_font_sizes()
            
        except Exception as e:
            messagebox.showerror("错误", f"打开文件时出错: {str(e)}")

    def generate_toc_from_content(self, content):
        lines = content.split('\n')
        toc = []
        self.toc_positions = {}
        line_number = 1
        
        # 分析每个文本块的层级关系
        blocks = []
        current_block = []
        last_indent = -1
        
        for i, line in enumerate(lines, 1):
            if line.strip():
                # 处理图片标记（跳过，将在导出HTML时处理）
                if line.strip().startswith('[img:'):
                    continue

                # 处理文件标记（跳过，将在导出HTML时处理）
                if line.strip().startswith('[file:'):
                    continue
                    
                indent = len(line) - len(line.lstrip())
                if last_indent != -1 and last_indent != indent:
                    if current_block:
                        blocks.append(current_block)
                        current_block = []
                current_block.append((i, line, indent))
                last_indent = indent
            elif current_block:
                blocks.append(current_block)
                current_block = []
        
        if current_block:
            blocks.append(current_block)
        
        # 创建编号系统
        numbering = {}  # 存储每个缩进级别的当前编号
        last_level = -1  # 上一个处理的缩进级别
        
            # 判断每个块是否应该显示在目录中
        for block in blocks:
            # 将块添加到目录中
            for i, line, indent in block:
                # 完全跳过以"\"开头的行（不显示在目录中）
                if line.lstrip().startswith('\\'):
                    continue
                    
                # 跳过第一行（标题）
                if i == 1:
                    self.toc_positions[len(toc)] = f"{i}.0"
                    continue
                    
                    # 计算当前行的缩进级别（每个空格代表一级）
                level = indent
                    
                # 更新编号系统
                if level > last_level:  # 进入更深层级
                    # 初始化新层级的编号
                    for l in range(last_level + 1, level + 1):
                        if l == level:
                            numbering[l] = 1
                elif level < last_level:  # 返回较浅层级
                    # 重置更深层级的编号
                    for l in range(level + 1, last_level + 1):
                        if l in numbering:
                            del numbering[l]
                    # 增加当前层级的编号
                    numbering[level] = numbering.get(level, 0) + 1
                else:  # 同级
                    numbering[level] = numbering.get(level, 0) + 1
                    
                # 生成编号字符串
                number_str = ""
                for l in range(level + 1):
                    if l in numbering:
                        number_str += str(numbering[l]) + ("." if l < level else "")
                    
                stripped_line = line.strip()
                if len(stripped_line) > 16:
                    stripped_line = stripped_line[:16] + "..."
                    
                # 添加带编号的目录项，分开存储编号和文本
                actual_indent = indent if indent >= 0 else 0
                toc.append((number_str, stripped_line, actual_indent))
                self.toc_positions[len(toc)] = f"{i}.0"
                last_level = level
        
        self.toc_text.config(state='normal')
        self.toc_text.delete(1.0, tk.END)
        
        # 使用文档第一行作为总标题
        doc_title = lines[0].strip() if lines else "无标题"
        self.toc_text.insert(tk.END, doc_title + "\n\n", "toc_title")
        
        # 配置目录文本样式
        self.toc_text.tag_config("toc_item", font=("TkDefaultFont", 10))
        self.toc_text.tag_config("blue_number", foreground="#0077CC")
        self.toc_text.tag_config("black_text", foreground="black")
        self.toc_text.tag_config("toc_title", font=("TkDefaultFont", 14, "bold"))
        
        # 添加目录内容
        for number_str, text, indent in toc:
            # 插入带有不同颜色的编号和文本
            if indent > 0:
                self.toc_text.insert(tk.END, ' ' * indent)
            self.toc_text.insert(tk.END, number_str, "blue_number")
            self.toc_text.insert(tk.END, ' ' + text + '\n', "black_text")
        
        self.toc_text.config(state='disabled')
        self.toc_data = toc

    def save_config(self):
        """保存配置到文件"""
        config = {
            'last_file': self.current_file,
            'file_type': self.current_file_type
        }
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"保存配置失败: {str(e)}")

    def on_exit(self):
        """处理程序退出"""
        try:
            self.save_config()
        except Exception as e:
            print(f"退出时保存配置失败: {str(e)}")
        finally:
            self.root.destroy()

    def load_config(self):
        """从配置文件加载设置"""
        try:
            if not os.path.exists(self.config_file):
                return
                
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            if not config.get('last_file'):
                return
                
            if not os.path.exists(config['last_file']):
                print(f"警告: 配置文件记录的文件不存在: {config['last_file']}")
                return
                
            self.current_file = config['last_file']
            self.current_file_type = config.get('file_type', 'docformer')
            
            try:
                if self.current_file_type == 'docformer':
                    self.open_docformer(self.current_file)
                else:
                    self.open_html(self.current_file)
            except Exception as e:
                print(f"打开记录的文件失败: {str(e)}")
                self.current_file = None
                self.current_file_type = None
                
        except json.JSONDecodeError:
            print("错误: 配置文件格式无效")
        except Exception as e:
            print(f"加载配置失败: {str(e)}")

    def save_file(self):
        if not self.current_file:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".docformer",
                filetypes=[("DocFormer files", "*.docformer"), ("All files", "*.*")]
            )
            if not file_path:
                return
            self.current_file = file_path
            self.current_file_type = 'docformer'
        
        try:
            content = self.text_editor.get(1.0, tk.END)
            with open(self.current_file, 'w', encoding='utf-8') as file:
                file.write(content)
            self.root.title(f"DocFormer Editor - {os.path.basename(self.current_file)}")
            self.save_config()
        except Exception as e:
            messagebox.showerror("错误", f"保存文件时出错: {str(e)}")

    def show_font_dialog(self):
        """显示字号设置对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("字号设置")
        dialog.geometry("300x200")
        
        # 正文字号设置
        ttk.Label(dialog, text="正文字号:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        body_size = tk.IntVar(value=self.font_config['body_size'])
        ttk.Spinbox(dialog, from_=8, to=36, textvariable=body_size, width=5).grid(row=0, column=1, padx=5, pady=5)
        
        # 最小标题字号设置
        ttk.Label(dialog, text="最小标题字号:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        min_title_size = tk.IntVar(value=self.font_config['min_title_size'])
        ttk.Spinbox(dialog, from_=8, to=36, textvariable=min_title_size, width=5).grid(row=1, column=1, padx=5, pady=5)
        
        # 字号步长设置
        ttk.Label(dialog, text="字号步长:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        size_step = tk.IntVar(value=self.font_config['size_step'])
        ttk.Spinbox(dialog, from_=1, to=6, textvariable=size_step, width=5).grid(row=2, column=1, padx=5, pady=5)
        
        # 应用按钮
        def apply_changes():
            self.font_config['body_size'] = body_size.get()
            self.font_config['min_title_size'] = min_title_size.get()
            self.font_config['size_step'] = size_step.get()
            self.update_font_sizes()
            dialog.destroy()
            
        ttk.Button(dialog, text="应用", command=apply_changes).grid(row=3, column=0, columnspan=2, pady=10)

    def insert_image(self):
        """在当前光标位置插入图片"""
        file_path = filedialog.askopenfilename(
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.gif")]
        )
        if file_path:
            # 插入图片标记格式：[img:path/to/image.png]
            self.text_editor.insert(tk.INSERT, f"[img:{file_path}]")
            
            # 如果是新行插入图片，需要更新字体大小
            line_num = int(self.text_editor.index(tk.INSERT).split('.')[0])
            self.update_font_sizes()
            
    def insert_file(self):
        """在当前光标位置插入文件"""
        file_path = filedialog.askopenfilename(
            filetypes=[("所有文件", "*.*")]
        )
        if file_path:
            # 插入文件标记格式：[file:path/to/file.ext]
            self.text_editor.insert(tk.INSERT, f"[file:{file_path}]")
            
            # 更新字体大小
            line_num = int(self.text_editor.index(tk.INSERT).split('.')[0])
            self.update_font_sizes()

    def set_font_config(self, body_size=None, min_title_size=None, size_step=None):
        """设置字号配置"""
        if body_size is not None:
            self.font_config['body_size'] = body_size
        if min_title_size is not None:
            self.font_config['min_title_size'] = min_title_size
        if size_step is not None:
            self.font_config['size_step'] = size_step
        self.update_font_sizes()  # 更新字体大小

    def export_to_html(self):
        export_path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        if not export_path:
            return
            
        try:
            content = self.text_editor.get(1.0, tk.END)
            lines = content.split('\n')
            
            # 生成HTML内容
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{os.path.basename(export_path)}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .container {{ display: flex; height: 100vh; }}
        .toc {{ 
            width: 300px; 
            padding: 10px; 
            border-right: 1px solid #ccc;
            overflow-y: auto;
            height: 100%;
        }}
        .toc-title {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            padding-bottom: 5px;
            border-bottom: 1px solid #ccc;
        }}
        .content {{ 
            flex: 1; 
            padding: 10px;
            overflow-y: auto;
            height: 100%;
        }}
        .sidebar {{ 
            width: 250px; 
            padding: 10px; 
            border-left: 1px solid #ccc;
            overflow-y: auto;
            height: 100%;
            background-color: #f8f8f8;
        }}
        .toc a {{ 
            text-decoration: none; 
            color: #333; 
            display: block; 
            margin: 5px 0; 
        }}
        .toc a:hover {{ color: #666; }}
        .block {{
            padding: 5px;
            margin: 5px 0;
            word-wrap: break-word;
            transition: background-color 0.5s;
        }}
        .block p {{
            margin: 0;
            padding: 0;
            white-space: pre-wrap;       /* 保留空格和换行 */
            word-wrap: break-word;       /* 允许长单词换行 */
            text-indent: inherit;        /* 继承缩进 */
        }}
        .highlight {{
            transition: background-color 0.5s;
            background-color: yellow;
        }}
        .unhighlight {{
            transition: background-color 0.5s;
            background-color: transparent;
        }}
        .block:hover {{
            background-color: yellow;
        }}
        .separator {{
            border-top: 1px solid #E0E0E0;
            margin: 10px 0;
        }}
        .file-item {{
            display: flex;
            align-items: center;
            padding: 10px;
            margin-bottom: 10px;
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.2s;
        }}
        .file-item:hover {{
            background-color: #f0f0f0;
        }}
        .file-icon {{
            margin-right: 10px;
            font-size: 24px;
            color: #0077CC;
        }}
        .file-name {{
            flex-grow: 1;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        img.sidebar-img {{
            max-width: 100%;
            margin-bottom: 10px;
            cursor: pointer;
            border: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="toc">
            <div class="toc-title">目录</div>
"""
            
            # 添加目录
            numbering = {}  # 存储每个缩进级别的当前编号
            last_level = -1  # 上一个处理的缩进级别
            
            for i, line in enumerate(lines, 1):
                if line.strip():
                    # 跳过正文
                    if line.lstrip().startswith('\\'):
                        continue
                
                    # 跳过图片
                    if line.lstrip().startswith('[img:'):
                        continue
                
                    # 跳过文件
                    if line.lstrip().startswith('[file:'):
                        continue
                        
                    stripped_line = line.strip()
                    if len(stripped_line) > 16:
                        stripped_line = stripped_line[:16] + "..."
                    indent = len(line) - len(line.lstrip())
                    
                    # 跳过第一行（标题）
                    if i == 1:
                        html_content += f'            <a href="#h{i}" onclick="highlightBlock(\'h{i}\')">{stripped_line}</a>\n'
                        continue
                    
                    # 计算当前行的缩进级别（每个空格代表一级）
                    level = indent
                    
                    # 更新编号系统
                    if level > last_level:  # 进入更深层级
                        # 初始化新层级的编号
                        for l in range(last_level + 1, level + 1):
                            if l == level:
                                numbering[l] = 1
                    elif level < last_level:  # 返回较浅层级
                        # 重置更深层级的编号
                        for l in range(level + 1, last_level + 1):
                            if l in numbering:
                                del numbering[l]
                        # 增加当前层级的编号
                        numbering[level] = numbering.get(level, 0) + 1
                    else:  # 同级
                        numbering[level] = numbering.get(level, 0) + 1
                    
                    # 生成编号字符串
                    number_str = ""
                    for l in range(level + 1):
                        if l in numbering:
                            number_str += str(numbering[l]) + ("." if l < level else "")
                    
                    # 添加带编号的目录项（编号为蓝色）
                    if i == 1:  # 第一行标题
                        stripped_line = line.strip()
                        if len(stripped_line) > 16:
                            stripped_line = stripped_line[:16] + "..."
                        html_content += f'            <a href="#h{i}" onclick="highlightBlock(\'h{i}\')">{stripped_line}</a>\n'
                    else:
                        # 计算编号和文本
                        level = indent
                        number_str = ""
                        for l in range(level + 1):
                            if l in numbering:
                                number_str += str(numbering[l]) + ("." if l < level else "")
                        
                        stripped_line = line.strip()
                        if len(stripped_line) > 16:
                            stripped_line = stripped_line[:16] + "..."
                        
                        if indent == 0:
                            html_content += f'            <a href="#h{i}" onclick="highlightBlock(\'h{i}\')"><span style="color: #0077CC;">{number_str}</span> <span style="color: black;">{stripped_line}</span></a>\n'
                        else:
                            html_content += f'            <a href="#h{i}" onclick="highlightBlock(\'h{i}\')" style="margin-left: {16*indent}px"><span style="color: #0077CC;">{number_str}</span> <span style="color: black;">{stripped_line}</span></a>\n'
                    
                    last_level = level
            
            html_content += """        </div>
        <div class="content">
"""
            
            # 创建导出目录（如果不存在）
            export_dir = os.path.dirname(export_path)
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)
                
            # 创建images子目录存放图片
            images_dir = os.path.join(export_dir, 'images')
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)
                
            # 创建assets子目录存放文件
            assets_dir = os.path.join(export_dir, 'assets')
            if not os.path.exists(assets_dir):
                os.makedirs(assets_dir)
                
            # 添加正文内容
            last_indent = -1
            current_block = []
            numbering = {}  # 存储每个缩进级别的当前编号
            last_level = -1  # 上一个处理的缩进级别
            
            for i, line in enumerate(lines, 1):
                if line.strip():
                    # 处理图片标记
                    if line.strip().startswith('[img:'):
                        img_path = line.strip()[5:-1]  # 提取图片路径
                        if os.path.exists(img_path):
                            try:
                                img_name = os.path.basename(img_path)
                                dest_path = os.path.join(images_dir, img_name)
                                shutil.copy2(img_path, dest_path)
                                current_block.append(f'''
                                    <div style="padding-left: {indent * 32}px; margin: 10px 0;">
                                        <img src="images/{img_name}" style="max-width: 100%; display: block; border: 1px solid #ddd; border-radius: 4px;">
                                    </div>
                                ''')
                            except Exception as e:
                                print(f"无法复制图片 {img_path}: {str(e)}")
                        continue
                    
                    # 处理文件标记
                    if line.strip().startswith('[file:'):
                        file_path = line.strip()[6:-1]  # 提取文件路径
                        if os.path.exists(file_path):
                            try:
                                file_name = os.path.basename(file_path)
                                dest_path = os.path.join(assets_dir, file_name)
                                shutil.copy2(file_path, dest_path)
                                current_block.append(f'''
                                    <div class="file-item" style="padding-left: {indent * 32}px; margin: 10px 0;" onclick="downloadFile('assets/{file_name}', '{file_name}')">
                                        <div class="file-icon">📄</div>
                                        <div class="file-name">{file_name}</div>
                                    </div>
                                ''')
                            except Exception as e:
                                print(f"无法复制文件 {file_path}: {str(e)}")
                        continue
                    
                    # 处理以"\"开头的行（正文内容）
                    if line.lstrip().startswith('\\'):
                        if current_block:  # 附加到当前block
                            stripped_line = line.strip()[1:]  # 去掉开头的"\\"
                            if len(stripped_line) > 16:
                                stripped_line = stripped_line[:16] + "..."
                            
                            # 获取父级缩进（使用当前block中最后一个标题的缩进）
                            parent_indent = 0
                            for item in reversed(current_block):
                                if isinstance(item, tuple):  # 找到最近的标题
                                    parent_indent = item[2]
                                    break
                            
                            current_block.append(f'<p style="font-size: {self.font_config["body_size"]}px; padding-left: {parent_indent * 10}px; white-space: pre-wrap; text-indent: 0;"><span style="color: black;">{stripped_line}</span></p>')
                        continue
                    
                    indent = len(line) - len(line.lstrip())
                    # 使用配置的字号参数
                    if line.lstrip().startswith('\\'):
                        font_size = self.font_config['body_size']
                    else:
                        # 根据缩进级别计算标题字号
                        font_size = self.font_config['min_title_size'] + \
                                   (max(len(l) - len(l.lstrip()) for l in lines if l.strip()) - indent) * \
                                   self.font_config['size_step']
                    
                    # 第一行作为总标题，字号加一级
                    if i == 1:
                        font_size += self.font_config['size_step']
                        # 处理块和分隔线
                        if current_block:
                            html_content += '            <div class="block">\n'
                            for block_line in current_block:
                                html_content += f'                {block_line}\n'
                            html_content += '            </div>\n'
                            current_block = []
                        # 添加分隔线
                        html_content += '            <div class="separator"></div>\n'
                        # 添加当前行到块（标题不需要编号）
                        current_block.append(f'<p id="h{i}" style="font-size: {font_size}px; text-indent: {indent * 32}px;">{line.strip()}</p>')
                        continue
                    
                    # 计算当前行的缩进级别（每个空格代表一级）
                    level = indent
                    
                    # 更新编号系统
                    if level > last_level:  # 进入更深层级
                        # 初始化新层级的编号
                        for l in range(last_level + 1, level + 1):
                            if l == level:
                                numbering[l] = 1
                    elif level < last_level:  # 返回较浅层级
                        # 重置更深层级的编号
                        for l in range(level + 1, last_level + 1):
                            if l in numbering:
                                del numbering[l]
                        # 增加当前层级的编号
                        numbering[level] = numbering.get(level, 0) + 1
                    else:  # 同级
                        numbering[level] = numbering.get(level, 0) + 1
                    
                    # 生成编号字符串
                    number_str = ""
                    for l in range(level + 1):
                        if l in numbering:
                            number_str += str(numbering[l]) + ("." if l < level else "")
                    
                    # 处理块和分隔线
                    # 跳过以"\"开头的行（正文内容）
                    if line.lstrip().startswith('\\'):
                        if current_block:  # 附加到当前block
                            stripped_line = line.strip()[1:]  # 去掉开头的"\\"
                            if len(stripped_line) > 16:
                                stripped_line = stripped_line[:16] + "..."
                            
                            # 获取父级缩进（使用当前block中最后一个标题的缩进）
                            parent_indent = 0
                            for item in reversed(current_block):
                                if isinstance(item, tuple):  # 找到最近的标题
                                    parent_indent = item[2]
                                    break
                            
                            # 确保缩进不小于父级缩进
                            effective_indent = max(indent, parent_indent) if indent >=0 else parent_indent
                            current_block.append(f'<p style="font-size: {font_size}px; padding-left: {effective_indent * 32}px; white-space: pre-wrap; text-indent: 0;"><span style="color: black;">{stripped_line}</span></p>')
                        continue
                    
                    # 每个标题都作为一个新块
                    if current_block and (i > 1):  # 跳过第一行（总标题）
                        # 输出上一个块
                        html_content += '            <div class="block">\n'
                        for block_line in current_block:
                            html_content += f'                {block_line}\n'
                        html_content += '            </div>\n'
                        # 添加分隔线
                        html_content += '            <div class="separator"></div>\n'
                        current_block = []
                    
                    # 确保文本块中的每一行都保持相同的缩进
                    if line.strip():
                        # 对于正文内容区域，不截断标题
                        line = ' ' * indent*4 + line.strip()
                        # 如果是标题行且不是目录，则不截断
                        if not line.lstrip().startswith('\\') and i != 1:  # 跳过第一行总标题
                            if len(line.strip()) > 16:
                                line = ' ' * indent*4 + line.strip()  # 保持完整内容
                    
                    # 添加当前行到块（带编号，编号部分为深蓝色）
                    stripped_line = line.strip()
                    if len(stripped_line) > 16:
                        stripped_line = stripped_line[:16] + "..."
                    # 对于正文内容区域，标题完整显示
                    full_line = line.strip()
                    current_block.append(f'<p id="h{i}" style="font-size: {font_size}px; padding-left: {indent * 32}px; white-space: pre-wrap; text-indent: 0;"><span style="color: #0077CC;">{number_str}</span> <span style="color: black;">{full_line}</span></p>')
                    last_indent = indent
                    last_level = level
            
            # 输出最后一个块
            if current_block:
                html_content += '            <div class="block">\n'
                for block_line in current_block:
                    html_content += f'                {block_line}\n'
                html_content += '            </div>\n'
            
            html_content += """        </div>
    </div>
    <script>
        function highlightBlock(blockId) {
            // 移除现有高亮
            //var currentlyHighlighted = document.querySelector('.highlight');
            //if (currentlyHighlighted) {
            //    currentlyHighlighted.classList.remove('highlight');
            //}
            // 添加新高亮
            var blockToHighlight = document.getElementById(blockId);
            if (blockToHighlight) {
                blockToHighlight.classList.add('highlight');
                blockToHighlight.scrollIntoView({behavior: 'smooth'});
            }
            setTimeout(function() {
                blockToHighlight.classList.add('unhighlight');
            }, 500);
            setTimeout(function() {
                blockToHighlight.classList.remove('unhighlight');
                blockToHighlight.classList.remove('highlight');
            }, 1000);
        }
        
        function downloadFile(filePath, fileName) {
            const link = document.createElement('a');
            link.href = filePath;
            link.download = fileName;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    </script>
</body>
</html>"""
            
            with open(export_path, 'w', encoding='utf-8') as file:
                file.write(html_content)
                
            #messagebox.showinfo("成功", "文件已导出为HTML格式")
            
            # 询问是否在浏览器中打开
            webbrowser.open(export_path)
                
        except Exception as e:
            messagebox.showerror("错误", f"导出文件时出错: {str(e)}")

    def clean_installation(self):
        if messagebox.askyesno("确认", "确定要清理DocFormer安装吗？这将删除所有相关文件。"):
            try:
                # 获取Python安装路径
                python_path = Path(sys.executable).parent
                
                # 删除可执行文件
                if os.name == 'nt':  # Windows
                    exe_path = python_path / 'Scripts' / 'docformer.exe'
                else:  # Linux/Mac
                    exe_path = python_path / 'bin' / 'docformer'
                
                if exe_path.exists():
                    os.remove(exe_path)
                
                # 删除包文件
                package_path = python_path / 'Lib' / 'site-packages' / 'docformer'
                if package_path.exists():
                    shutil.rmtree(package_path)
                
                messagebox.showinfo("成功", "DocFormer已成功清理")
                self.root.quit()
            except Exception as e:
                messagebox.showerror("错误", f"清理安装时出错: {str(e)}")

def main():
    root = tk.Tk()
    app = DocFormerEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main() 