
import netCDF4 as nc
import numpy as np
def getPoint(pre, df, lat0, lon0, resolution, decimal=1):
    latIdx = ((lat0 - df["Lat"]) / resolution + 0.5).astype(np.int64)
    lonIdx = ((df["Lon"] - lon0) / resolution + 0.5).astype(np.int64)
    return pre[...,latIdx, lonIdx].round(decimals=decimal)
def Get_Lat_Lon_QPF(path,Lon_data,Lat_data):
    with nc.Dataset(path) as dataNC:
        latArr = dataNC["lat"][:]
        lonArr = dataNC["lon"][:]
        if "AIW_QPF" in  path:
            pre = dataNC[list(dataNC.variables.keys())[3]][:]    
        elif "AIW_REF" in path:
            pre = dataNC[list(dataNC.variables.keys())[4]][:]   
    data = getPoint(pre , {"Lon":Lon_data,"Lat":Lat_data} , latArr[0], lonArr[0], 0.01)
    data = getPoint(pre , {"Lon":Lon_data,"Lat":Lat_data} , latArr[0], lonArr[0], 0.01)
    return data

"""   pip index  设置
mkdir .pip 进入文件夹  vim pip.conf  粘贴保存
[global]
index_url=https://pypi.tuna.tsinghua.edu.cn/simple
"""
"""
zoom插值
from scipy.ndimage import zoom
d = zoom(d_clip, [4201/169,6201/249], order=1)[:-1, :-1]
"""
"""  区域切割
import xarray as xr
ds = xr.open_dataset(a)
# # 定义经纬度范围
# lon_min, lon_max = 72.0, 136.96
# lat_min, lat_max = 6.04, 54.0
# 定义经纬度范围
ds = ds.sortby('latitude') 
lon_min, lon_max = 73, 134.99
lat_min, lat_max = 12.21, 54.2  #[73,134.99,12.21,54.2] 
# 现在可以进行数据截取
subset = ds.sel(longitude=slice(lon_min, lon_max), latitude=slice(lat_min, lat_max))   # 
H9 = subset["data"][::-1,:]

longitude_values = subset['longitude'].values
latitude_values = subset['latitude'].values

print("裁剪后的经度范围：", longitude_values.min(), longitude_values.max())
print("裁剪后的纬度范围：", latitude_values.min(), latitude_values.max())

# 裁剪后的数据信息
data_values = subset['data'].values
data_attrs = subset['data'].attrs

print("裁剪后的数据形状：", subset['data'].shape)
print("裁剪后的数据值：", data_values)
print("数据的属性信息：", data_attrs)

"""
###用于回算
"""
from main import makeAll,options
from multiprocessing import Pool
import datetime
from config import logger,output
import time
import pandas as pd
import os
from itertools import product
import threading
from shancx import Mul_sub
def excuteCommand(conf):
    cmd = conf[0]
    print(cmd)
    os.system(cmd)

if __name__ == '__main__':
    cfg = options()
    isPhase = cfg.isPhase
    isDebug = cfg.isDebug
    sepSec = cfg.sepSec
    gpu = cfg.gpu
    pool = cfg.pool
    isOverwrite = cfg.isOverwrite
    timeList = pd.date_range(cfg.times[0], cfg.times[-1], freq=f"{sepSec}s")
    logger.info(f"时间段check {timeList}")
    gpuNum = 2
    eachGPU = 4
    makeListUTC = []
    for UTC in timeList:
        UTCStr = UTC.strftime("%Y%m%d%H%M")
        outpath = f"{output}/{UTCStr[:4]}/{UTCStr[:8]}/MSP2_WTX_AIW_QPF_L88_CHN_{UTCStr}_00000-00300-00006.nc"
        if not os.path.exists(outpath) or not os.path.exists(outpath.replace("_QPF_","_REF_"))  or isOverwrite:
            makeListUTC.append(UTC)
    [print(element) for element in makeListUTC]
    phaseCMD = "--isPhase" if isPhase else ""
    debugCMD = "--isDebug" if isDebug else ""
    OverwriteCMD = "--isOverwrite"
    gpuCMD = f"--gpu={gpu}"
    # cmdList = list(map(lambda x:f"python main.py --times={x.strftime('%Y%m%d%H%M')} {phaseCMD} {debugCMD} {OverwriteCMD} {gpuCMD}",makeListUTC))
    cmdList = list(map(lambda x:f"python main.py --times={x.strftime('%Y%m%d%H%M')} {phaseCMD} {debugCMD} {gpuCMD}",makeListUTC))
    if cmdList:
        Mul_sub(excuteCommand, [cmdList], pool)
    else: 
        print("cmdList is empty, skipping the call.")
        raise ValueError("cmdList is empty, cannot execute command.")
CUDA_LAUNCH_BLOCKING=1 python makeHis.py --times 202410010048,202410110048 --gpu=0 --isDebug --sepSec 3600 --pool 5
CUDA_LAUNCH_BLOCKING=1 python makeHis1.py --times 202410010048,202410110048 --gpu=0 --isDebug --sepSec 3600 --pool 5
"""
###用于循环出日报
"""
#!/bin/bash
start_date="20241001"
end_date="20241101"
tag="scx/MQPF_Gan5_default_1112N"
current_date=$(date -d "$start_date" +%Y%m%d)
end_date=$(date -d "$end_date" +%Y%m%d)
while [ "$current_date" != "$end_date" ]; do
    start_time="$current_date"0000
    end_time="$current_date"2359
    python makeDOC_newv2.py --times $start_time,$end_time --tag $tag
    current_date=$(date -d "$current_date + 1 day" +%Y%m%d)
done
python makeDOC_newv2.py --times $end_date"0000",$end_date"2359" --tag $tag
"""
"""
frile name :launch.json
args:
{
    "version": "0.2.0",
    "configurations": [   
        {
            "name": "Python: Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "cwd": "${fileDirname}",
            "purpose": ["debug-in-terminal"],
            "justMyCode": false,
            "args": [  
                "--times", "202409160000,202409180000" 
            ]
        }
    ]
}

{
    "version": "0.2.0",
    "configurations": [   

        {
            "name": "Python: Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "cwd": "${fileDirname}",
            "purpose": ["debug-in-terminal"],
            "justMyCode": false,
            "args": [
            "--times", "202410010042,202410020042",
            "--isDebug" ,
            "--isOverwrite", 
            "--sepSec", "3600",
            "--gpu", "0"
            ]
        }
    ]
}

"""

"""
import importlib
def get_obj_from_str(class_path: str):
    module_name, class_name = class_path.rsplit('.', 1)    
    module = importlib.import_module(module_name)    
    return getattr(module, class_name)
config = {
    "target": "torch.nn.Linear",  # 类路径
    "params": {                  # 参数字典
        "in_features": 128,
        "out_features": 64
    }
}

# 使用配置字典动态实例化对象
target_class = get_obj_from_str(config["target"])  # 获取类（torch.nn.Linear）
model = target_class(**config.get("params", dict()))  # 使用解包的参数实例化

# 打印结果
print(model)

import torch
import torch.nn as nn
linear = nn.Linear(in_features=128, out_features=64, bias=True)配置字典动态传参
"""

"""
ImportError: /lib64/libc.so.6: version `GLIBC_2.28' not found (required by /home/scx1/miniconda3/envs/mqpf/lib/python3.10/site-packages/lxml/etree.cpython-310-x86_64-linux-gnu.so)
pip uninstall lxml
pip install lxml
"""
"""
001  key: "ee90f313-17b2-4e3d-84b8-3f9c290fa596"
002  far_po "f490767c-27bc-4424-9c75-2b33644171e2"
003  数据监控 "4c43f4bd-d984-416d-ac82-500df5e3ed86"
sendMESplus("测试数据",base=user_info)
"""

'''
from multiprocessing import Pool
'''
'''
 ##定義一個streamHandler
# print_handler = logging.StreamHandler()  
# print_handler.setFormatter(formatter) 
# loggers.addHandler(print_handler)
'''
'''
# @Time : 2023/09/27 下午8:52
# @Author : shanchangxi
# @File : util_log.py
import time
import logging  
from logging import handlers
 
logger = logging.getLogger()
logger.setLevel(logging.INFO) 
log_name =  'project_tim_tor.log'
logfile = log_name
time_rotating_file_handler = handlers.TimedRotatingFileHandler(filename=logfile, when='D', encoding='utf-8')
time_rotating_file_handler.setLevel(logging.INFO)   
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
time_rotating_file_handler.setFormatter(formatter)
logger.addHandler(time_rotating_file_handler)
print_handler = logging.StreamHandler()   
print_handler.setFormatter(formatter)   
logger.addHandler(print_handler)
'''
'''
###解决方法  pip install torch==2.4.0  torchvision    torchaudio三个同时安装  python 3.12  解决cuda启动不了的问题
Res网络
'''
'''
import concurrent.futures
from itertools import product
def task(args):
    args1,args2  = args
    print( f"Task ({args1}, {args2}) , result")
    return (args1,args2,5)

def Mul_sub(task, pro):
    product_list = product(*pro)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(task, item) for item in product_list]
    results = [future.result() for future in concurrent.futures.as_completed(futures)]   
    return results
res = Mul_sub(task, [[1, 23, 4, 5], ["n"]])
print("res")
print(res)
'''

"""
find /mnt/wtx_weather_forecast/scx/SpiderGLOBPNGSource -type f -name "*.png" -mtime +3 -exec rm {} \;
-mtime 选项后面的数值代表天数。
+n 表示“超过 n 天”，即查找最后修改时间在 n 天之前的文件。
"""
"""
from shancx.SN import UserManager,sendMESplus
from shancx._info import users 
M = UserManager(info=users)
user_info = M.get_user("003") 
sendMESplus("测试数据",base=user_info)
"""
"""
https://api.map.baidu.com/lbsapi/getpoint/index.html  坐标
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple   pip.conf
python setup.py sdist bdist_wheel
twine upload dist/*
"""
"""   与循环搭配使用   
    for key,value in dictflag.items():
        try:
            pac = all_df1[all_df1['PAC'].str.startswith(f'{key}')]
            acctoal,acctoalEC,matEC,mat,rate_Lift_ratiotsEC,outpath= metriacfunall(pac)
            if not len(matEC.shape) == (2,2):
               continue             
            docdataset =  mkdataset2TS(acctoal,acctoalEC,matEC,mat, rate_Lift_ratiotsEC,outpath)
    
        except Exception as e:
            print(traceback.format_exc())  
            continue
"""

"""

cuda-version              11.8                 hcce14f8_3
cudatoolkit               11.8.0               h6a678d5_0
cudnn                     8.9.2.26               cuda11_0
nvidia-cuda-cupti-cu12    12.1.105                 pypi_0    pypi
nvidia-cuda-nvrtc-cu12    12.1.105                 pypi_0    pypi
nvidia-cuda-runtime-cu12  12.1.105                 pypi_0    pypi
nvidia-cudnn-cu12         8.9.2.26                 pypi_0    pypi
mqpf conda install pytorch  torchvision torchaudio  cudatoolkit=11.8 -c pytorch  
conda install cudnn=8.9.2.26 cudatoolkit=11.8 
resunet pip install torch==2.4.0  torchvision    torchaudio
conda install cudnn==8.9.2.26 cudatoolkit==11.8.0
conda install pytorch=2.2.2 torchvision torchaudio cudatoolkit=11.8 -c pytorch
resunet pip install torch==2.4.0  torchvision    torchaudio
pip install protobuf==3.20

my-envmf1
torch                     2.3.0                    pypi_0    pypi
torchvision               0.18.0                   pypi_0    pypi

RES:
torch                     2.4.0                    pypi_0    pypi
torchaudio                2.2.2                 py311_cpu    pytorch
torchsummary              1.5.1                    pypi_0    pypi
torchvision               0.19.0                   pypi_0    pypi

mqpf:
torch                     2.3.1                    pypi_0    pypi
torchaudio                2.3.1                    pypi_0    pypi
torchvision               0.18.1                   pypi_0    pypi
onnxruntime-gpu           1.16.0
onnx                      1.15.0 
numpy                     1.26.4

vllm:
torch                     2.1.2                    pypi_0    pypi
torchvision               0.15.1+cu118             pypi_0    pypi
vllm                      0.2.7                    pypi_0    pypi

import torch
print("CUDA available:", torch.cuda.is_available())
print("CUDA version:", torch.version.cuda)
print("GPU device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU")
nvidia-smi 
nvcc --version
系统已经检测到物理 GPU（NVIDIA GeForce RTX 4090）和 NVIDIA 驱动，同时安装了 CUDA 12.1。然而，PyTorch 没有正确检测到 GPU，可能是因为 PyTorch 版本与 CUDA 驱动不兼容，或者环境变量未正确配置。

pip install torch==2.3.1    torchvision==0.18.1  

conda install -c conda-forge cudatoolkit=11.8 --force-reinstall   解决报错
ls $CONDA_PREFIX/lib/libcublasLt.so.11
:ProviderLibrary::Get() [ONNXRuntimeError] : 1 : FAIL : Failed to load library libonnxruntime_providers_cuda.so with error: libcublasLt.so.11: cannot open shared object file: No such file or directory
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
"""
"""
conda env export > environment.yml
conda env create -f /path/to/destination/environment.yml
conda activate your_env_name

conda install -c conda-forge conda-pack
conda pack -n aiw -o my_env.tar.gz
mkdir -p my_env
tar -xzf my_env.tar.gz -C my_env
source my_env/bin/activate
"""
"""
定时任务

MAILTO="shanhe12@163.com"

""" 
"""
vgg_loss = VGGLoss(weights_path="/mnt/wtx_weather_forecast/scx/stat/sat/sat2radar/vgg19-dcbb9e9d.pth").to(device)
SAMloss = SAMLoss(model_type='vit_b', checkpoint_path='/mnt/wtx_weather_forecast/scx/stat/sat/sat2radar/sam_vit_b_01ec64.pth.1').to(device)
"""

"""
sdata = xr.open_dataset(sat_paths)
sdata["time"] = sUTC
edata = xr.open_dataset(sat_pathe)
edata["time"] = UTC
sdata = sdata.assign_coords(time=sUTC)
edata = edata.assign_coords(time=UTC)
添加维度和更新已有维度数据
sdata = xr.open_dataset(sat_paths).rename({"time": "old_time"})
edata = xr.open_dataset(sat_pathe).rename({"time": "old_time"})
# 现在可以安全添加新时间坐标
sdata = sdata.assign_coords(time=sUTC)
edata = edata.assign_coords(time=UTC)
UTC = datetime.datetime.strptime(self.nowDate, "%Y%m%d%H%M")  注意时间格式
"""
"""
#sudo mkdir -p /mnt/wtx_weather_forecast/GeoEnvData/rawData/MeteoL/Himawari/H9
#sudo mount -t nfs nfs.300s.ostor:/mnt/ifactory_public/AWS_data/AWS_data/Himawari /mnt/wtx_weather_forecast/GeoEnvData/rawData/MeteoL/Himawari/H9  
"""

"""
groups
sudo gpasswd -d user sudo  # 从 sudo 组移除用户 "user"
id
sudo usermod -u 1001 user
sudo usermod -g 1001 user
sudo chown -R 新用户名:新组名 目录名/

sudo find / -user 1015 -exec chown 1001 {} \;

more  /etc/passwd
vim 修改 /etc/passwd

"""
"""
    latArr = np.linspace(env.n, env.s, int(round((env.n - env.s) / 0.02)) + 1)
    lonArr = np.linspace(env.w, env.e, int(round((env.e - env.w) / 0.02)) + 1)
"""