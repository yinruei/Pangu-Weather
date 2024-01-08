# import subprocess
# import os

# BASEPATH = os.getcwd()

# # 定义要执行的脚本列表
# script_list = [
#     "plot_200wind_slp.py",
#     "plot_850t_500gh.py",
#     "plot_t2m_10mwind.py",
#     "plot_850wind_slp.py"
# ]

# # 循环执行每个脚本
# for script in script_list:
#     try:
#         # 激活虚拟环境（假设虚拟环境在项目根目录下的 venv 文件夹中）
#         subprocess.run([f'{BASEPATH}/venv/Scripts/activate'], check=True, shell=True)

#         # 执行脚本
#         subprocess.run(["python", script], check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"Error executing {script}: {e}")
        
        
# !!!!!!!!!!!!!!!!!!!
import subprocess

# 请确保虚拟环境已经激活

# 定义要执行的四个 Python 脚本的路径
scripts = [
    "plot_200wind_slp.py",
    "plot_850t_500gh.py",
    "plot_t2m_10mwind.py",
    "plot_850wind_slp.py"
]

# 依次执行每个脚本
for script in scripts:
    command = f"python {script}"
    subprocess.run(command, shell=True)

# 如果希望在执行脚本之后等待用户输入，可以添加以下代码
input("Press Enter to exit...")
