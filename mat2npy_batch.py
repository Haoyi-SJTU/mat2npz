import os
import glob
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import scipy.io
import numpy as np



import os
import glob
import scipy.io
import numpy as np
import traceback
from pathlib import Path

def batch_mat_to_npz(mat_folder, target_vars, output_folder=None, overwrite=False):
    """
    批量将文件夹中的MAT文件转换为只包含目标变量的NPZ文件
    
    参数:
    mat_folder: 包含MAT文件的文件夹路径
    target_vars: 要提取的变量名列表，如 ['angle_ideal', 'angle_residual']
    output_folder: 输出文件夹路径，默认与输入文件夹相同
    overwrite: 是否覆盖已存在的文件
    
    返回:
    success_list: 成功处理的文件列表
    error_list: 处理失败的文件及错误信息
    """
    
    # 设置输出文件夹
    if output_folder is None:
        output_folder = os.path.join(mat_folder, 'npz_output')
    
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)
    
    # 获取所有MAT文件
    mat_files = glob.glob(os.path.join(mat_folder, '*.mat'))
    
    if not mat_files:
        print(f"在文件夹 {mat_folder} 中未找到任何 .mat 文件")
        return [], []
    
    print(f"找到 {len(mat_files)} 个 .mat 文件")
    
    success_list = []
    error_list = []
    
    for mat_file in mat_files:
        try:
            # 提取文件名（不带扩展名）
            filename = os.path.basename(mat_file)
            file_stem = os.path.splitext(filename)[0]
            npz_file = os.path.join(output_folder, f"{file_stem}.npz")
            
            # 检查是否已存在
            if os.path.exists(npz_file) and not overwrite:
                print(f"跳过 {filename} (文件已存在)")
                continue
            
            # 加载.mat文件
            mat_data = scipy.io.loadmat(mat_file)
            
            # 提取目标变量
            target_data = {}
            missing_vars = []
            
            for var_name in target_vars:
                if var_name in mat_data:
                    target_data[var_name] = mat_data[var_name]
                else:
                    missing_vars.append(var_name)
            
            if missing_vars:
                print(f"警告: 文件 {filename} 缺少变量: {missing_vars}")
            
            if not target_data:
                error_msg = f"文件中没有找到任何目标变量"
                print(f"错误: {filename} - {error_msg}")
                error_list.append((filename, error_msg))
                continue
            
            # 保存为.npz文件
            np.savez(npz_file, **target_data)
            
            # 验证保存结果
            verify_data = np.load(npz_file)
            saved_vars = verify_data.files
            verify_data.close()
            
            # 记录成功
            print(f"✓ 成功: {filename} -> 保存变量: {saved_vars}")
            success_list.append({
                'mat_file': filename,
                'npz_file': f"{file_stem}.npz",
                'saved_vars': list(saved_vars),
                'path': npz_file
            })
            
        except Exception as e:
            error_msg = f"处理失败: {str(e)}"
            print(f"✗ 错误: {filename} - {error_msg}")
            error_list.append((filename, error_msg))
    
    # 打印统计信息
    print(f"\n{'='*50}")
    print(f"处理完成!")
    print(f"成功: {len(success_list)} 个文件")
    print(f"失败: {len(error_list)} 个文件")
    
    if success_list:
        print("\n成功处理的文件:")
        for item in success_list:
            print(f"  {item['mat_file']} -> {item['npz_file']} ({', '.join(item['saved_vars'])})")
    
    if error_list:
        print("\n失败的文件:")
        for filename, error in error_list:
            print(f"  {filename}: {error}")
    
    return success_list, error_list


def convert_with_progress(mat_folder, target_vars, output_folder=None):
    """
    带进度显示的批量转换函数
    """
    from tqdm import tqdm
    import glob
    import os
    
    if output_folder is None:
        output_folder = os.path.join(mat_folder, 'converted_npz')
    
    os.makedirs(output_folder, exist_ok=True)
    
    mat_files = glob.glob(os.path.join(mat_folder, '*.mat'))
    
    if not mat_files:
        print("未找到.mat文件")
        return []
    
    print(f"开始处理 {len(mat_files)} 个文件...")
    
    results = []
    for mat_file in tqdm(mat_files, desc="转换进度"):
        filename = os.path.basename(mat_file)
        file_stem = os.path.splitext(filename)[0]
        npz_file = os.path.join(output_folder, f"{file_stem}.npz")
        
        try:
            # 加载并提取变量
            mat_data = scipy.io.loadmat(mat_file)
            
            # 提取目标变量
            target_data = {}
            for var_name in target_vars:
                if var_name in mat_data:
                    target_data[var_name] = mat_data[var_name]
            
            if target_data:
                np.savez(npz_file, **target_data)
                results.append((filename, True, f"保存变量: {list(target_data.keys())}"))
            else:
                results.append((filename, False, "未找到目标变量"))
                
        except Exception as e:
            results.append((filename, False, str(e)))
    
    # 显示结果摘要
    success_count = sum(1 for r in results if r[1])
    print(f"\n转换完成: {success_count}/{len(results)} 成功")
    
    return results


def convert_mat_to_npz_single(mat_file, target_vars, output_path=None):
    """
    转换单个MAT文件
    
    参数:
    mat_file: MAT文件路径
    target_vars: 目标变量列表
    output_path: 输出NPZ文件路径，默认与输入文件同目录同名
    
    返回:
    bool: 是否成功
    str: 消息
    """
    try:
        # 加载MAT文件
        mat_data = scipy.io.loadmat(mat_file)
        
        # 提取目标变量
        target_data = {}
        for var_name in target_vars:
            if var_name in mat_data:
                target_data[var_name] = mat_data[var_name]
        
        if not target_data:
            return False, "未找到任何目标变量"
        
        # 设置输出路径
        if output_path is None:
            dir_name = os.path.dirname(mat_file)
            file_stem = os.path.splitext(os.path.basename(mat_file))[0]
            output_path = os.path.join(dir_name, f"{file_stem}.npz")
        
        # 保存
        np.savez(output_path, **target_data)
        
        # 验证
        loaded_data = np.load(output_path)
        saved_vars = loaded_data.files
        loaded_data.close()
        
        return True, f"成功保存变量: {list(saved_vars)}"
        
    except Exception as e:
        return False, f"错误: {str(e)}"


def process_folder_recursive(input_folder, target_vars, output_base_folder=None, 
                            file_pattern='*.mat'):
    """
    递归处理文件夹及其子文件夹中的所有MAT文件
    
    参数:
    input_folder: 输入文件夹
    target_vars: 目标变量列表
    output_base_folder: 输出基础文件夹
    file_pattern: 文件匹配模式
    """
    from pathlib import Path
    
    input_path = Path(input_folder)
    
    if output_base_folder is None:
        output_base_folder = input_path.parent / f"{input_path.name}_npz"
    
    # 递归查找所有MAT文件
    mat_files = list(input_path.rglob(file_pattern))
    
    if not mat_files:
        print(f"在 {input_folder} 及其子文件夹中未找到 {file_pattern} 文件")
        return []
    
    print(f"找到 {len(mat_files)} 个 MAT 文件")
    
    results = []
    for mat_file in mat_files:
        # 计算相对路径
        rel_path = mat_file.relative_to(input_path)
        
        # 构建输出路径
        output_file = output_base_folder / rel_path.with_suffix('.npz')
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 转换文件
        success, message = convert_mat_to_npz_single(
            str(mat_file), target_vars, str(output_file)
        )
        
        status = "✓" if success else "✗"
        print(f"{status} {rel_path}: {message}")
        
        results.append({
            'input': str(mat_file),
            'output': str(output_file),
            'success': success,
            'message': message
        })
    
    return results


def create_conversion_summary(results, summary_file='conversion_summary.txt'):
    """
    创建转换结果摘要文件
    """
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("MAT文件转换摘要\n")
        f.write("=" * 50 + "\n\n")
        
        success_count = sum(1 for r in results if r['success'])
        f.write(f"总文件数: {len(results)}\n")
        f.write(f"成功: {success_count}\n")
        f.write(f"失败: {len(results) - success_count}\n\n")
        
        f.write("成功文件:\n")
        f.write("-" * 30 + "\n")
        for item in results:
            if item['success']:
                f.write(f"{os.path.basename(item['input'])} -> {os.path.basename(item['output'])}\n")
        
        f.write("\n失败文件:\n")
        f.write("-" * 30 + "\n")
        for item in results:
            if not item['success']:
                f.write(f"{os.path.basename(item['input'])}: {item['message']}\n")
    
    print(f"摘要已保存到 {summary_file}")



class MatToNpzConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MAT-NPZ 批量转换工具")
        self.root.geometry("600x400")
        
        # 变量列表
        self.target_vars = ['angle_ideal', 'angle_residual']
        
        self.setup_ui()
    
    def setup_ui(self):
        # 输入文件夹
        tk.Label(self.root, text="MAT文件夹:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.input_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.input_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.root, text="浏览...", command=self.browse_input).grid(row=0, column=2, padx=5, pady=5)
        
        # 输出文件夹
        tk.Label(self.root, text="输出文件夹:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.output_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.output_var, width=50).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.root, text="浏览", command=self.browse_output).grid(row=1, column=2, padx=5, pady=5)
        
        # 变量设置
        tk.Label(self.root, text="要提取的变量:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.var_frame = tk.Frame(self.root)
        self.var_frame.grid(row=2, column=1, columnspan=2, sticky='w', padx=5, pady=5)
        
        self.var_entries = []
        for i, var in enumerate(self.target_vars):
            tk.Label(self.var_frame, text=f"变量 {i+1}:").grid(row=i, column=0, sticky='w')
            entry = tk.Entry(self.var_frame, width=20)
            entry.insert(0, var)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.var_entries.append(entry)
        
        # 添加变量按钮
        tk.Button(self.var_frame, text="+ 添加变量", command=self.add_var_entry).grid(row=len(self.target_vars), column=0, pady=5)
        tk.Button(self.var_frame, text="- 删除变量", command=self.remove_var_entry).grid(row=len(self.target_vars), column=1, pady=5)
        
        # 进度条
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=3, sticky='ew', padx=10, pady=10)
        
        # 状态文本
        self.status_var = tk.StringVar(value="就绪")
        tk.Label(self.root, textvariable=self.status_var).grid(row=4, column=0, columnspan=3, pady=5)
        
        # 日志文本框
        tk.Label(self.root, text="日志:").grid(row=5, column=0, sticky='w', padx=10, pady=5)
        self.log_text = tk.Text(self.root, height=8, width=70)
        self.log_text.grid(row=6, column=0, columnspan=3, padx=10, pady=5)
        
        # 按钮
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=7, column=0, columnspan=3, pady=10)
        
        tk.Button(button_frame, text="开始转换", command=self.start_conversion, 
                 bg='green', fg='white').pack(side='left', padx=5)
        tk.Button(button_frame, text="清除日志", command=self.clear_log).pack(side='left', padx=5)
        tk.Button(button_frame, text="退出", command=self.root.quit).pack(side='left', padx=5)
    
    def browse_input(self):
        folder = filedialog.askdirectory(title="选择包含MAT文件的文件夹")
        if folder:
            self.input_var.set(folder)
            # 自动设置输出文件夹
            if not self.output_var.get():
                self.output_var.set(os.path.join(folder, 'npz_output'))
    
    def browse_output(self):
        folder = filedialog.askdirectory(title="选择输出文件夹")
        if folder:
            self.output_var.set(folder)
    
    def add_var_entry(self):
        row = len(self.var_entries)
        tk.Label(self.var_frame, text=f"变量 {row+1}:").grid(row=row, column=0, sticky='w')
        entry = tk.Entry(self.var_frame, width=20)
        entry.grid(row=row, column=1, padx=5, pady=2)
        self.var_entries.append(entry)
    
    def remove_var_entry(self):
        if self.var_entries:
            entry = self.var_entries.pop()
            entry.destroy()
    
    def log(self, message):
        self.log_text.insert('end', message + '\n')
        self.log_text.see('end')
        self.root.update()
    
    def clear_log(self):
        self.log_text.delete(1.0, 'end')
    
    def start_conversion(self):
        # 获取输入输出路径
        input_folder = self.input_var.get()
        output_folder = self.output_var.get()
        
        if not input_folder or not os.path.exists(input_folder):
            messagebox.showerror("错误", "请输入有效的输入文件夹")
            return
        
        if not output_folder:
            messagebox.showerror("错误", "请输入输出文件夹")
            return
        
        # 获取目标变量
        target_vars = [entry.get().strip() for entry in self.var_entries if entry.get().strip()]
        if not target_vars:
            messagebox.showerror("错误", "请至少指定一个变量")
            return
        
        # 开始转换
        self.status_var.set("转换中...")
        self.progress.start()
        
        try:
            # 调用批量转换函数
            success, errors = batch_mat_to_npz(
                mat_folder=input_folder,
                target_vars=target_vars,
                output_folder=output_folder,
                overwrite=True
            )
            
            # 显示结果
            self.status_var.set(f"完成! 成功: {len(success)}, 失败: {len(errors)}")
            self.log(f"\n转换完成!")
            self.log(f"成功: {len(success)} 个文件")
            self.log(f"失败: {len(errors)} 个文件")
            
            if errors:
                self.log("\n失败详情:")
                for filename, error in errors:
                    self.log(f"  {filename}: {error}")
            
        except Exception as e:
            messagebox.showerror("错误", f"转换过程中发生错误:\n{str(e)}")
        finally:
            self.progress.stop()

# 运行GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = MatToNpzConverterGUI(root)
    root.mainloop()