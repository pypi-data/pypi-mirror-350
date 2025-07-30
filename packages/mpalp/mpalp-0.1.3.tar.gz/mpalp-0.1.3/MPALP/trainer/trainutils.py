import os
import time
import json
import psutil
import torch
import torch.nn as nn
import torch.optim as optim
import subprocess
# from transformers import AdamW, get_linear_schedule_with_warmup



def see_device():
    '''
    선택 가능한 gpu device 표시
    '''
    return_string = ''
    if torch.cuda.is_available():
        print('\n------------- GPU list -------------')
        n_devices = torch.cuda.device_count()
        for i in range(n_devices):
            print(f'{i} - {torch.cuda.get_device_name(i)}')
        print('------------------------------------')
        
        return_string += f'{i} - {torch.cuda.get_device_name(i)}\n'
    else:
        return_string = 'No GPU available'
    return return_string
        

# gpu or cpu 선택
def get_device(gpu_idx):
    '''
    학습에 활용할 gpu 선택 (없을 시 cpu)

    parameters
    ----------
    gpu_idx: int
        학습에 활용할 gpu 번호(순서)

    returns
    -------
    device: gpu or cpu
        학습에 활용할 gpu or cpu
    '''
    # Arrange GPU devices starting from 0
    # os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID" 
    # os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_idx)
    try:
        if torch.cuda.is_available():
            device = torch.device(f"cuda:{gpu_idx}")
            print('------------------------------------')
            print(f'GPU used: {gpu_idx} - {torch.cuda.get_device_name(gpu_idx)}')
            print('------------------------------------')
        else:
            print('------------------------------------')
            print('No GPU available, using the CPU instead.')
            print('wait 5 second...')
            print('------------------------------------')
            time.sleep(5)
            device = torch.device("cpu")
    except AssertionError:
        print('------------------------------------')
        print('No GPU available, using the CPU instead.')
        print('wait 5 second...')
        print('------------------------------------')
        time.sleep(5)
        device = torch.device("cpu")
    return device


def get_optimizer(base, method, model, learning_rate):
    '''
    학습용 optimizer 를 얻어내는 코드
    
    paramaters
    ----------
    base: str
        기반이 되는 모듈 이름 설정. transformers or torch.

    method: str
        optimizer 의 종류 설정.

    model: torch.model
        optimizer 를 적용할 model
    
    learning_rate: float
        learning rate

    returns
    -------
    optimizer: optimizer
        학습용 optimizer
    '''
    if base == 'torch':
        if method == 'SGD':
            optimizer = optim.SGD(model.parameters(), lr=learning_rate)
        elif method == 'Adam':
            optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=1e-5)
        elif method == 'AdamW':
            optimizer = optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=1e-5)
        else:
            raise ValueError('Not a valid optimizer')
    # optimizer = optimizer(params=model.parameters(), lr=learning_rate)
    return optimizer


def get_scheduler(base, method, optimizer, 
                  gamma=0.97, 
                  t_max=100, eta_min=0.001,
                  total_iter=None, warmup_iter=None):
    '''
    학습용 scheduler 를 얻어내는 함수

    parameters
    ----------
    base: str
        기반이 되는 모듈 이름 설정. transformers or torch.

    method: str
        scheduler 의 종류 설정.

    optimizer: optimizer
        학습용 optimizer

    t_total: float

    warmup_ratio: float

    gamma:float
        learning rate 를 줄이는 비율
    '''
    if base == 'torch':
        if method == 'StepLR':
            scheduler = optim.lr_scheduler.StepLR(
                optimizer,
                5.0,
                gamma=gamma
            )
        if method == 'ExponentialLR':
            scheduler = optim.lr_scheduler.ExponentialLR(
                optimizer, 
                gamma=gamma
            )
        if method == 'ReduceLROnPlateau':
            scheduler = optim.lr_scheduler.ReduceLROnPlateau(
                optimizer, 
                mode='min', 
                factor=0.5, 
                patience=20, 
                verbose=1
            )
        if method == 'LambdaLR':
            scheduler = optim.lr_scheduler.LambdaLR(
                optimizer=optimizer,
                lr_lambda=lambda epoch:gamma ** epoch,
                last_epoch=-1,
                verbose=False
            )
        if method == 'CosineAnnealingLR':
            scheduler = optim.lr_scheduler.CosineAnnealingLR(
                optimizer, 
                T_max=t_max,
                eta_min=eta_min
            )
    return scheduler


def see_parameters(model):
    total_params = sum(p.numel() for p in model.parameters())
    print(f'총 파라미터 수: {total_params}')
    
    
def get_condition_order(args_setting, save_path, except_arg_list=None):
    os.makedirs(save_path, exist_ok=True)
    condition_list = os.listdir(save_path)
    condition_list.sort()
    if len(condition_list) == 0:
        condition_order = 0
    else:
        args_key_list = list(args_setting.keys())
        args_key_list.sort()

        for condition in condition_list:
            with open(f'{save_path}/{condition}/args_setting.json', 'r', encoding='utf-8-sig') as f:
                exist_args_setting = json.load(f)

            exist_args_key_list = list(exist_args_setting.keys())
            exist_args_key_list.sort()

            for key, e_key in zip(args_key_list, exist_args_key_list):
                if except_arg_list is not None:
                    if key in except_arg_list:
                        continue
                if key == e_key:
                    if args_setting[key] != exist_args_setting[e_key]:
                        condition_order = int(condition) + 1
                        break
                    else:
                        condition_order = int(condition)
                        continue
                if key != e_key:
                    condition_order = int(condition) + 1
                    break
            if condition_order > int(condition):
                continue
            else:
                break

    condition_order = str(condition_order).zfill(4)

    return condition_order


# 메모리 사용 확인 함수
def print_memory_usage():
    '''
    메모리 사용 확인 함수
    '''
    memory_info = psutil.virtual_memory()
    cpu_use = memory_info.percent
    memory_avail = memory_info.available / (1024 ** 3)
    print(f'CPU Memory Usage: {cpu_use}% Used, {memory_avail:.2f} GB available')
    allocated_memory = torch.cuda.memory_allocated()
    reserved_memory = torch.cuda.memory_reserved()
    print(f'GPU allocated {allocated_memory / 1024**2:.2f} MB')
    print(f'gpu reserved {reserved_memory / 1024**2:.2f} MB')
    
    
def get_gpu_temperature():
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"],
        stdout=subprocess.PIPE, text=True
    )
    gpu_t = int(result.stdout.strip())
    return gpu_t


def gpu_temp_control(limit=65, proper=51):
    gpu_temp = get_gpu_temperature()
    # print(f'GPU temperature : {gpu_temp}')
    if gpu_temp > limit:
        print(f'GPU 온도가 {limit}도를 초과하여 {proper}도 아래로 내려갈때까지 학습을 중단합니다...')
        while True:
            time.sleep(5)
            gpu_temp = get_gpu_temperature()
            if gpu_temp < proper:
                break
    