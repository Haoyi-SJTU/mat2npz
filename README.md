# MAT-NPZ 批量转换工具

##  概述

这是一个基于 Python Tkinter，用于批量转换 MATLAB 的 `.mat` 文件为 NumPy 的 `.npz` 文件的图形界面工具。该工具允许您从多个 MAT 文件中提取指定的变量，并保存为同名的 NPZ 文件，过滤掉不必要的元数据。

##  功能特点

-  **选择性提取**：只提取指定的变量，过滤 `__header__`、`__version__` 等元数据
-  **批量处理**：一键转换整个文件夹中的所有 MAT 文件
-  **图形界面**：直观的用户界面，无需编写代码
-  **递归处理**：支持处理子文件夹中的文件
-  **实时日志**：显示详细的转换进度和结果
-  **变量配置**：动态添加/删除要提取的变量
-  **自动目录**：自动创建输出文件夹结构

##  系统要求

### 必需环境
- Python 3.6 或更高版本（已在python 3.8环境下测试可用）
- 以下 Python 库：
  - NumPy
  - SciPy
  - Tkinter

### 可选依赖
- tqdm（用于进度条显示）

## 使用步骤

### 1. 安装 Python
确保已安装 Python 3.6 或更高版本。

### 2. 安装必需库并下载代码
打开命令行工具，运行以下命令：

```bash
pip install numpy scipy
pip install tqdm

git clone https://github.com/Haoyi-SJTU/mat2npz
```

### 3. 启动程序
在终端中运行以下命令启动图形界面：

```bash
python mat2npz_batch.py
```

### 界面说明

界面如图（有点儿丑请忽略）

![](https://github.com/Haoyi-SJTU/mat2npz/blob/main/Screenshot.png)

#### 1. 输入设置
- **MAT文件文件夹**：选择包含要转换的 `.mat` 文件的文件夹
- **输出文件夹**：选择或输入保存 `.npz` 文件的文件夹（默认为输入文件夹下的 `npz_output` 子文件夹）

#### 2. 变量配置
- **变量列表**：指定要从 MAT 文件中提取的变量名
  - 默认包含 `angle_ideal` 和 `angle_residual`
  - 点击 "+ 添加变量" 添加新变量
  - 点击 "- 删除变量" 删除选中的变量

#### 3. 转换控制
- **开始转换**：开始批量转换过程
- **清除日志**：清空日志窗口
- **退出**：关闭程序

### 转换步骤

1. **选择输入文件夹**
   - 点击 "浏览..." 按钮
   - 选择包含 `.mat` 文件的文件夹

2. **设置输出文件夹**（可选）
   - 指定输出 NPZ 文件的文件夹
   - 如果留空，将在输入文件夹下创建 `npz_output` 子文件夹

3. **配置目标变量**
   - 在变量列表中输入要提取的变量名
   - 每行一个变量
   - 支持添加/删除变量

4. **开始转换**
   - 点击 "开始转换" 按钮
   - 程序将遍历指定文件夹中的所有 `.mat` 文件
   - 提取指定的变量
   - 保存为同名的 `.npz` 文件

5. **查看结果**
   - 在日志窗口中查看转换进度
   - 转换完成后显示统计信息

## 📁 文件结构示例

### 转换前
```
项目文件夹/
├── data/
│   ├── experiment1.mat
│   ├── experiment2.mat
│   └── experiment3.mat
└── mat_converter_gui.py
```

### 转换后
```
项目文件夹/
├── data/
│   ├── experiment1.mat
│   ├── experiment2.mat
│   └── experiment3.mat
├── npz_output/           # 自动创建
│   ├── experiment1.npz
│   ├── experiment2.npz
│   └── experiment3.npz
└── mat_converter_gui.py
```

##  输出文件格式

### 输入文件
```
example.mat
├── __header__: b'MATLAB 5.0 MAT-file...'
├── __version__: '1.0'
├── __globals__: []
├── angle_ideal: (150, 6)     # ← 需要提取
├── angle_residual: (150, 6)  # ← 需要提取
└── other_variable: (100, 4)   # ← 不需要提取
```

### 输出文件
```
example.npz
├── angle_ideal: (150, 6)    # 只包含指定变量
└── angle_residual: (150, 6)
```

##  常见问题

#### 1. "未找到任何 .mat 文件"
- 确认输入文件夹路径正确
- 确保文件夹中包含 `.mat` 文件
- 检查文件扩展名是否正确（应为 `.mat`）

#### 2. "未找到目标变量"
- 确认变量名拼写正确
- MAT 文件中可能使用不同的变量名
- 使用 MATLAB 或其他工具检查 MAT 文件中的变量名

#### 3. 内存不足错误
- 对于大型 MAT 文件，确保有足够的内存
- 可以分批处理文件
- 考虑增加系统虚拟内存

#### 4. 权限错误
- 确保有写入输出文件夹的权限
- 以管理员身份运行程序（如果需要）

### 错误消息

| 错误消息 | 可能原因 | 解决方案 |
|---------|---------|---------|
| "文件夹不存在" | 输入的文件夹路径错误 | 检查路径并重新选择 |
| "未找到目标变量" | 变量名错误或不存在 | 检查 MAT 文件中的变量名 |
| "访问被拒绝" | 没有写入权限 | 以管理员运行或更改输出文件夹 |
| "内存不足" | 文件太大或内存不足 | 分批处理或增加内存 |

## 许可证

本工具基于 MIT 许可证开源。

# MAT to NPZ Batch Converter Tool

## 📋 Overview

This is a Python Tkinter-based graphical interface tool for batch converting MATLAB `.mat` files to NumPy `.npz` files. The tool allows you to extract specified variables from multiple MAT files and save them as NPZ files with the same name, filtering out unnecessary metadata.

## ✨ Features

- 🎯 **Selective Extraction**: Extract only the variables you specify, filtering out metadata like `__header__`, `__version__`
- 📁 **Batch Processing**: Convert all MAT files in a folder with one click
- 🎨 **Graphical Interface**: Intuitive user interface, no coding required
- 🔄 **Recursive Processing**: Support for processing files in subfolders
- 📊 **Real-time Logging**: Display detailed conversion progress and results
- 🎚️ **Variable Configuration**: Dynamically add/remove variables to extract
- 📁 **Automatic Directory**: Automatically create output folder structure

## 📦 System Requirements

### Required Environment
- Python 3.6 or higher
- The following Python libraries:
  - NumPy
  - SciPy
  - Tkinter

### Optional Dependencies
- tqdm (for progress bar display)

##  Usage Steps

### 1. Install Python
Python 3.6 or higher.

### 2. Install Required Libraries and Download the Tool
Open a Terminal and run:

```bash
pip install numpy scipy
pip install tqdm

git clone https://github.com/Haoyi-SJTU/mat2npz
```

###  3. Usage

### Launch the Program
Run the following command to start the graphical interface:

```bash
python mat2npz_batch.py
```

### Interface Description

Interface is as following

![](https://github.com/Haoyi-SJTU/mat2npz/blob/main/Screenshot.png)

#### 1. Input Settings
- **MAT Files Folder**: Select folder containing `.mat` files to convert
- **Output Folder**: Select or enter folder to save `.npz` files (default is `npz_output` subfolder in input folder)

#### 2. Variable Configuration
- **Variable List**: Specify variable names to extract from MAT files
  - Default includes `angle_ideal` and `angle_residual`
  - Click "+ Add Variable" to add new variable
  - Click "- Remove Variable" to delete selected variable

#### 3. Conversion Controls
- **Start Conversion**: Begin batch conversion process
- **Clear Log**: Clear log window
- **Exit**: Close the program

### Conversion Steps

1. **Select Input Folder**
   - Click "Browse..." button
   - Select folder containing `.mat` files

2. **Set Output Folder** (Optional)
   - Specify folder for output NPZ files
   - If left blank, will create `npz_output` subfolder in input folder

3. **Configure Target Variables**
   - Enter variable names to extract in the variable list
   - One variable per line
   - Supports adding/removing variables

4. **Start Conversion**
   - Click "Start Conversion" button
   - Program will traverse all `.mat` files in the specified folder
   - Extract specified variables
   - Save as `.npz` files with the same name

5. **View Results**
   - View conversion progress in the log window
   - Display statistics after conversion is complete

## File Structure Example

### Before Conversion
```
Project Folder/
├── data/
│   ├── experiment1.mat
│   ├── experiment2.mat
│   └── experiment3.mat
└── mat_converter_gui.py
```

### After Conversion
```
Project Folder/
├── data/
│   ├── experiment1.mat
│   ├── experiment2.mat
│   └── experiment3.mat
├── npz_output/           # Automatically created
│   ├── experiment1.npz
│   ├── experiment2.npz
│   └── experiment3.npz
└── mat_converter_gui.py
```

## Output File Format

### Input File
```
example.mat
├── __header__: b'MATLAB 5.0 MAT-file...'
├── __version__: '1.0'
├── __globals__: []
├── angle_ideal: (150, 6)     # ← To extract
├── angle_residual: (150, 6)  # ← To extract
└── other_variable: (100, 4)   # ← Not to extract
```

### Output File
```
example.npz
├── angle_ideal: (150, 6)    # Contains only specified variables
└── angle_residual: (150, 6)
```

##  Troubleshooting

### Common Issues

#### 1. "No .mat files found"
- Confirm input folder path is correct
- Ensure folder contains `.mat` files
- Check file extensions are correct (should be `.mat`)

#### 2. "Target variables not found"
- Confirm variable names are spelled correctly
- MAT files may use different variable names
- Use MATLAB or other tools to check variable names in MAT files

#### 3. Insufficient Memory Error
- For large MAT files, ensure sufficient memory
- Process files in batches
- Consider increasing system virtual memory

#### 4. Permission Error
- Ensure write permission to output folder
- Run program as administrator (if needed)

### Error Messages

| Error Message | Possible Cause | Solution |
|--------------|---------------|----------|
| "Folder does not exist" | Input folder path is incorrect | Check path and reselect |
| "Target variables not found" | Variable names are wrong or don't exist | Check variable names in MAT file |
| "Access denied" | No write permission | Run as administrator or change output folder |
| "Insufficient memory" | File too large or insufficient memory | Process in batches or increase memory |


## License

This tool is open source under the MIT License.


