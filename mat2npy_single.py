import scipy.io
import numpy as np


# 从.mat文件中只提取目标变量并保存
# 参数:
#     mat_path: .mat文件路径
#     target_vars: 目标变量名列表
#     output_path: 输出文件路径
def save_only_target_variables(mat_path, target_vars, output_path='target_vars.npz'):

    # 加载.mat文件
    mat_data = scipy.io.loadmat(mat_path)
    
    # 提取目标变量
    target_data = {}
    for var_name in target_vars:
        if var_name in mat_data:
            target_data[var_name] = mat_data[var_name]
        else:
            print(f"警告: 变量 '{var_name}' 不存在于MAT文件中")
    
    # 保存为.npz文件
    if target_data:
        np.savez(output_path, **target_data)
        print(f"已保存 {len(target_data)} 个变量到 {output_path}")
    
    return target_data

# 使用示例
target_data = save_only_target_variables(
    'simdata_1/simdata_1.mat',
    ['angle_ideal', 'angle_residual'], #mat里的变量名
    'simdata_1.npz'
)







