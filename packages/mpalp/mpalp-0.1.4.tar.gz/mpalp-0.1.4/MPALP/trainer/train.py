import sys
import os
sys.path.append(os.getcwd())
import numpy as np
import shutil
import copy
import time
from tqdm import tqdm
import json
import warnings
warnings.filterwarnings('ignore')

import torch

# share modules
from MPALP.trainer import trainutils as tru
from MPALP.lossfunction import lossfunction as lft
from MPALP.accuracy import classificationutils as cfu
from MPALP.utils import timeutils as tu


def trainer(
        model, iterator, train_dataloader=None, val_dataloader=None, 
        epochs=100, batch_size=16, purpose=None, lf='C', lr=0.0005,
        root_path=None, save_name=None, device_num=0, 
        model_info=None,
        max_grad_norm=1, dropout_p=0.2, 
        opt='Adam', sche='CosineAnnealingLR', t_max=100, eta_min=0.00001,
        seed=42, debug=False, weight=None, param=False
    ):

    if root_path is None:
        root_path = os.getcwd()

    arss = {
        'epochs':epochs, 'batch_size':batch_size, 'learning_rate':lr,
        'root_path':root_path, 'save_name':save_name, 'purpose':purpose,
        'device_num':device_num, 'max_grad_norm':max_grad_norm, 'dropout_p':dropout_p,
        'model_info':model_info,
        'loss_function':lf, 'optimizer':opt, 
        'scheduler':sche, 't_max':t_max, 'eta_min':eta_min,
        'random_seed':seed, 'weight':weight,
    }
    # =========================================================================
    # 데이터 셋 경로
    # dataset_path = f"{ars['root_dataset_path']}/{ars['dataset_name']}"
    
    # =========================================================================
    # dataloader 생성
    print('train dataloader 생성 중...')
    if train_dataloader is None:
        pass
        # Train_Dataloader = dl.get_dataloader(
        #     mode='train',
        #     batch_size=arss['batch_size'],
        #     dataset_path=,
        #     x_name_list=,
        #     y_name_list=,
        #     shuffle=arss['shuffle'], 
        #     drop_last=arss['drop_last'],
        #     num_workers=arss['num_workers'], 
        #     pin_memory=arss['pin_memory']
        # )
    else:
        Train_Dataloader = train_dataloader

    if val_dataloader is None:
        pass
        # print('validation dataloader 생성 중...')
        # Val_Dataloader = dl.get_dataloader(
        #     mode='train',
        #     batch_size=arss['batch_size'], 
        #     dataset_path=, 
        #     x_name_list=, 
        #     y_name_list=, 
        #     shuffle=arss['shuffle'], 
        #     drop_last=arss['drop_last'], 
        #     num_workers=arss['num_workers'], 
        #     pin_memory=arss['pin_memory'], 
        # )
    else:
        Val_Dataloader = val_dataloader
    
    # =========================================================================
    # device 
    # tru.see_device()
    device = tru.get_device(arss['device_num'])
    
    # =========================================================================
    # model        
    model.to(device)

    # pre-trained
    if debug is not None:
        '''
        역전파 중 문제가 발생했을 때, 
        어떤 연산에서 발생했는지 추적 가능하게 해주는 디버깅 도구
        추적 정보를 저장하기 때문에 실행속도가 느려질 수 있어
        디버깅에서만 활용하는 것을 추천
        '''
        torch.autograd.set_detect_anomaly(True)
    if weight is not None:
        model.load_state_dict(weight)
        print('\n>>> use pre-trained model')
        
    # 파라미터 갯수 출력
    if param:
        tru.see_parameters(model)
    
    # =========================================================================
    # optimizer
    optimizer = tru.get_optimizer(
        base='torch',
        method=arss['optimizer'],
        model=model,
        learning_rate=arss['learning_rate']
    )

    # loss function
    criterion = lft.LossFunction(
        base='torch',
        method=arss['loss_function']
    )
    # scheduler
    scheduler = tru.get_scheduler(
        base='torch',
        method=arss['scheduler'],
        optimizer=optimizer,
        t_max=t_max,
        eta_min=eta_min
    )
    
    # =========================================================================
    # save setting
    # root_save_path = f"{ars['root_path']}/trained_model/{ars['phase']}/{ars['dataset_name']}"
    root_save_path = f"{root_path}/trained_model/{save_name}"
    condition_order = tru.get_condition_order(
        args_setting=arss,
        save_path=root_save_path,
        except_arg_list=['epochs', 'batch_size']
    )
    model_save_path = f'{root_save_path}/{condition_order}'
    os.makedirs(f'{root_save_path}/{condition_order}', exist_ok=True)
    with open(f'{root_save_path}/{condition_order}/args_setting.json', 'w', encoding='utf-8') as f:
        json.dump(arss, f, indent='\t', ensure_ascii=False)
    
    # ============================================================
    # train
    print('train...')    
    print(f'condition order: {condition_order}')
    _ = train(
        model=model, 
        iterator=iterator, 
        purpose=purpose, 
        epochs=epochs, 
        train_dataloader=Train_Dataloader, 
        validation_dataloader=Val_Dataloader, 
        device=device, 
        criterion=criterion, 
        optimizer=optimizer, 
        scheduler=scheduler, 
        max_grad_norm=max_grad_norm, 
        model_save_path=model_save_path,
        argmax_axis=1,
        label2id_dict=None, 
        id2label_dict=None,
        ignore_idx=None
    )
    
    print(condition_order)



def train(model, iterator, purpose, 
          epochs, train_dataloader, validation_dataloader, 
          device, criterion, optimizer, scheduler, max_grad_norm, model_save_path,
          argmax_axis=1, label2id_dict=None, id2label_dict=None, ignore_idx=None):


    # 변수 초기화
    best_loss = float('inf')
    history = {'best':{'epoch':0, 'loss':0}}

    # 학습 진행
    whole_start = time.time()
    for epoch in range(epochs):
        epoch_start = time.time()
        history[f'epoch {epoch+1}'] = {'train_loss':0, 'val_loss':0}
        print(f'======== {epoch+1:2d}/{epochs} ========')
        print(f'model path : {model_save_path}')
        print("lr: ", optimizer.param_groups[0]['lr'])

        # train -------------------
        model.train()
        
        # get output        
        _, _, train_loss, _ = iterator(
            mode='train',
            purpose=purpose,
            dataloader=train_dataloader,
            model=model,
            device=device, 
            criterion=criterion,
            optimizer=optimizer,
            max_grad_norm=max_grad_norm
        )
        print(f"epoch {epoch+1} train loss {train_loss}")

        # validation -------------
        model.eval()
        with torch.no_grad():
            val_pred_label_ary, val_true_label_ary, val_loss, _ = iterator(
                mode='val',
                model=model, 
                purpose=purpose,
                dataloader=validation_dataloader,
                device=device,
                criterion=criterion,
            )
            
            if purpose == 'c':
                # true
                val_true_label_ary = np.reshape(val_true_label_ary, (-1))
                
                # pred
                val_pred_label_ary = np.argmax(val_pred_label_ary, axis=argmax_axis)
                val_pred_label_ary = np.reshape(val_pred_label_ary, (-1))
                
                # confusion matrix
                if id2label_dict is not None:
                    val_confusion_matrix = cfu.make_confusion_matrix(
                        mode='id2label',
                        true_list=val_true_label_ary,
                        pred_list=val_pred_label_ary,
                        ignore_idx=ignore_idx,
                        round_num=4,
                        id2label_dict=id2label_dict
                    )
                if label2id_dict is not None:
                    val_confusion_matrix = cfu.make_confusion_matrix(
                        mode='label2id',
                        true_list=val_true_label_ary,
                        pred_list=val_pred_label_ary,
                        round_num=4,
                        label2id_dict=label2id_dict
                    )
                # accuracy
                val_acc = val_confusion_matrix['accuracy'].values[0]
        try:
            scheduler.step() 
        except TypeError:
            scheduler.step(epoch)

        # 학습 이력 저장
        history[f'epoch {epoch+1}']['train_loss'] = train_loss
        history[f'epoch {epoch+1}']['val_loss'] = val_loss

        # 최적의 모델 변수 저장
        if val_loss <= best_loss:
            best_loss = val_loss
            best_epoch = epoch + 1
            history['best']['epoch'] = best_epoch
            history['best']['loss'] = best_loss
            best_model_wts = copy.deepcopy(model.state_dict())
            save_dic = {
                "epoch" : epoch,
                "train_loss" : train_loss,
                "val_loss" : val_loss,
                "state_dict" : best_model_wts,
                "hyper_parameters" : None,
                "parameter_num" : None
            }

            # 최적 모델 저장
            best_model_name = f'epoch{str(best_epoch).zfill(4)}'
            os.makedirs(f'{model_save_path}/{best_model_name}', exist_ok=True)
            torch.save(model.state_dict(), f'{model_save_path}/{best_model_name}/weight.pt')
            
            # 이전의 최적 모델 삭제
            for i in range(epoch, 0, -1):
                pre_best_model_name = f'epoch{str(i).zfill(4)}'
                try:
                    shutil.rmtree(f'{model_save_path}/{pre_best_model_name}')
                    print(f'이전 모델 {pre_best_model_name} 삭제')
                except FileNotFoundError:
                    pass
            
            # 분류 모델인 경우
            if purpose == 'c':
                # best_acc = val_acc
                # best_val_confusion_matrix = val_confusion_matrix
                # best_val_pred_label_ary = val_pred_label_ary
                history['best']['acc'] = val_acc
                val_confusion_matrix.to_csv(f'{model_save_path}/{best_model_name}/confusion_matrix.csv', encoding='utf-8-sig')
                
        # 학습 history 저장
        with open(f'{model_save_path}/train_history.json', 'w', encoding='utf-8') as f:
            json.dump(history, f, indent='\t', ensure_ascii=False)

        # 검증 결과 출력
        print(f'epoch {epoch+1} validation loss {val_loss}\n')
        if purpose == 'c':
            print(val_confusion_matrix)

        # 시간 출력(epoch 당)
        h, m, s = tu.time_measure(epoch_start)
        print(f'에포크 시간: {h}시간 {m}분 {s}초\n')
    
    # 시간 출력(전체)
    h, m, s = tu.time_measure(whole_start)
    print(f'전체 학습 소요 시간: {h}시간 {m}분 {s}초\n')

    # 마지막 결과 저장
    os.makedirs(f'{model_save_path}/epoch{str(epoch + 1).zfill(4)}', exist_ok=True)
    torch.save(model.state_dict(), f'{model_save_path}/epoch{str(epoch + 1).zfill(4)}/weight.pt')
    
    # 분류 모델인 경우 추가 저장
    if purpose == 'c':
        val_confusion_matrix.to_csv(f'{model_save_path}/epoch{str(epoch + 1).zfill(4)}/confusion_matrix.csv', encoding='utf-8-sig')

    # # 최적의 학습모델 불러오기
    # print(f'best: {best_epoch}')
    # model.load_state_dict(best_model_wts)

    return save_dic



def model_test(model, test_dataloader, device):
    '''
    학습을 진행하여 최적의 학습된 모델 및 학습 이력을 얻어내는 함수

    parameters
    -------------------------------------------------------------
    model
        학습을 진행할 model
    
    test_dataloader
        학습용 test data 로 이루어진 dataloader
    
    device
        학습 진행시 활용할 device (cpu or gpu)

    loss_function: nn.criterion
        학습용 loss_function 

    -------
    pred_label_ary: int list, shape=(n, )
        입력된 데이터에 대한 결과(예측) 값 array

    true_label_ary
        실제 라벨 array
    '''
    # validation
    model.eval()
    with torch.no_grad():
        logit_ary, b_label_ary, running_loss, result_list = iterator(
            mode='test',
            purpose='',
            dataloader=test_dataloader,
            model=model, 
            device=device
        )

    return logit_ary, b_label_ary, running_loss, result_list
