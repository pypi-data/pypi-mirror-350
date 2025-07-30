import os
import time
from pathlib import Path
from typing import Literal

import pandas as pd
import copy
import torch
from torch import nn
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from ..Butils import b_get_device, b_get_gpu_nvidia
from ...Btqdm import B_Tqdm
from ...Btools.Bwriter import B_Writer
from ...Bbasic.Btext_style import B_Color, B_Appearance
from ..Bearly_stop import *
from ...Bbasic import Byzh

def inputs_function(inputs):
    return inputs
def outputs_function(outputs):
    return outputs
def labels_function(labels):
    return labels

class _saveDuringTrain:
    def __init__(self, path, rounds):
        self.path = path
        self.rounds = rounds
        self.cnt = 0
    def __call__(self):
        self.cnt += 1
        if self.cnt > self.rounds:
            self.cnt = 0
            return True
        return False

class _Func:
    def __init__(self, func=None):
        self.func = func
    def set_func(self, func):
        self.func = func
    def __call__(self, **kwargs):
        if self.func is None:
            return None
        result = self.func(**kwargs)
        return result


class B_Trainer(Byzh):
    def __init__(
        self,
        model,
        optimizer,
        criterion,
        train_loader,
        val_loader,
        test_loader = None,
        device = None,
        lrScheduler = None,
        isBinaryCls:bool = False,
        isParallel:bool = False,
        isSpikingjelly12:bool = False,
        isSpikingjelly14:bool = False,
    ):
        '''
        训练:\n
        train_eval_s\n
        训练前函数:\n
        load_model, load_optimizer, load_lrScheduler, set_writer, set_stop_by_acc\n
        训练后函数:\n
        save_latest_checkpoint, save_best_checkpoint, calculate_model
        :param model:
        :param train_loader:
        :param val_loader:
        :param test_loader:
        :param optimizer:
        :param criterion:
        :param device: 不指定则自动判断
        :param lrScheduler:
        :param isBinaryCls: 若是二分类, 则输出额外信息
        :param isParallel: 是否多GPU
        :param isSpikingjelly12: 是否为SNN
        '''
        super().__init__()
        self.train_acc_lst = []
        self.train_loss_batches_lst = []
        self.train_loss_epoch_lst = []
        self.val_acc_lst = []
        self.val_f1_lst = []
        self.val_L0_True_lst = []
        self.val_L1_True_lst = []

        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.test_loader = test_loader
        self.optimizer = optimizer
        self.criterion = criterion
        self.device = device if device is not None else b_get_device()
        self.lrScheduler = lrScheduler
        self.isBinaryCls = isBinaryCls
        self.isParallel = isParallel
        self.isSpikingjelly12 = isSpikingjelly12
        self.isSpikingjelly14 = isSpikingjelly14
        self.epoch = 0
        self.writer = None

        self.model.to(self.device)

        self._isTraining = False
        # save_temp
        self._save_during_train = None
        # early stop
        self._stop_by_acc = _Func()
        self._stop_by_acc_delta = _Func()
        self._stop_by_loss = _Func()
        self._stop_by_loss_delta = _Func()
        self._stop_by_overfitting = _Func()
        self._stop_by_byzh = _Func()
        # early reload
        self._reload_by_loss = _Func()
        # save_best
        self._best_acc = 0
        self._best_model_state_dict = None
        self._best_optimizer_state_dict = None
        self._best_lrScheduler_state_dict = None

        if self.isParallel:
            if str(self.device) == str(torch.device("cuda")):
                if torch.cuda.device_count() > 1:
                    print(f"[set] 当前cuda数量:{torch.cuda.device_count()}, 使用多GPU训练")
                    self.model = nn.DataParallel(self.model)
                else:
                    print(f"[set] 当前cuda数量:{torch.cuda.device_count()}, 使用单GPU训练")

    def train_eval_s(
            self,
            epochs,
            test:bool=False,
            inputs_func=inputs_function,
            outputs_func=outputs_function,
            labels_func=labels_function
    ):
        '''
        :param epochs:
        :param test: 在传递test_loader后, 若为True, 则同时在测试集测试
        :param inputs_func: 对inputs的处理函数
        :param outputs_func: 对outputs的处理函数
        :param labels_func: 对labels的处理函数
        :return:
        '''
        self._isTraining = True

        # 检查inputs_func是否为函数
        if not callable(inputs_func):
            raise ValueError("inputs_func传入的参数应该要是一个函数!!!")
        # 检查outputs_func是否为函数
        if not callable(outputs_func):
            raise ValueError("outputs_func传入的参数应该要是一个函数!!!")
        # 检查labels_func是否为函数
        if not callable(labels_func):
            raise ValueError("labels_func传入的参数应该要是一个函数!!!")

        for epoch in range(epochs):
            self.epoch = epoch
            train_acc, train_loss, current_lr = self._train_once(epoch, epochs, inputs_func, outputs_func, labels_func)
            val_acc = self._eval_once(inputs_func, outputs_func, labels_func)
            if test:
                test_acc = self._test_once(inputs_func, outputs_func, labels_func)
            print() # 换行
            # 日志
            if self.writer is not None:
                info = f'Epoch [{epoch}/{epochs}], lr: {current_lr:.2e} | ' \
                       f'train_loss: {train_loss:.3f} | train_acc: {train_acc:.3f}, val_acc: {val_acc:.3f}'
                if test:
                    info += f', test_acc: {test_acc:.3f}'
                self.writer.toFile(info)
            # 保存模型
            if self._save_during_train is not None:
                if self._save_during_train():
                    self.save_best_checkpoint(self._save_during_train.path)
            # 早停and重加载
            match self._stop_and_reload(train_loss, train_acc, val_acc):
                case "break":
                    break
                case "continue":
                    pass

    def _stop_and_reload(self, train_loss, train_acc, val_acc):
        ##### 早停
        if self._stop_by_acc(val_acc=val_acc):
            info = f'[stop] 模型在连续{self._stop_by_acc.func.rounds}个epoch内停滞, 触发stop_by_acc'
            self._print_and_toWriter(info)
            info = "[stop] " + str(self._stop_by_acc.func.cnt_list)
            self._print_and_toWriter(info, if_print=False)
            return "break"
        if self._stop_by_acc_delta(val_acc=val_acc):
            info = f'[stop] 模型在连续{self._stop_by_acc_delta.func.rounds}个epoch内过拟合, 触发stop_by_acc_delta'
            self._print_and_toWriter(info)
            info = "[stop] " + str(self._stop_by_acc_delta.func.cnt_list)
            self._print_and_toWriter(info, if_print=False)
            return "break"
        if self._stop_by_loss(train_loss=train_loss):
            info = f'[stop] 模型在连续{self._stop_by_loss.func.rounds}个epoch内停滞, 触发stop_by_loss'
            self._print_and_toWriter(info)
            info = "[stop] " + str(self._stop_by_loss.func.cnt_list)
            self._print_and_toWriter(info, if_print=False)
            return "break"
        if self._stop_by_loss_delta(train_loss=train_loss):
            info = f'[stop] 模型在连续{self._stop_by_loss_delta.func.rounds}个epoch内停滞, 触发stop_by_loss_delta'
            self._print_and_toWriter(info)
            info = "[stop] " + str(self._stop_by_loss_delta.func.cnt_list)
            self._print_and_toWriter(info, if_print=False)
            return "break"
        if self._stop_by_byzh(train_loss=train_loss, val_acc=val_acc):
            info = f'[stop] 模型触发stop_by_byzh'
            self._print_and_toWriter(info)
            info = "[stop] " + self._stop_by_byzh.func.output
            self._print_and_toWriter(info, if_print=False)
            return "break"
        ##### 过拟合
        if self._stop_by_overfitting(train_acc=train_acc, val_acc=val_acc):
            info = f'[stop] 模型在连续{self._stop_by_overfitting.func.rounds}个epoch内过拟合, 触发stop_by_overfitting'
            self._print_and_toWriter(info)
            info = "[stop] " + str(self._stop_by_overfitting.func.cnt_list)
            self._print_and_toWriter(info, if_print=False)
            return "break"
        ##### 重加载
        match self._reload_by_loss(train_loss=train_loss):
            case 'normal':
                pass
            case 'reload':
                info = f'模型触发reload_by_loss(第{self._reload_by_loss.func.cnt_reload}次加载)'
                self._print_and_toWriter(info)
                # 加载
                self.model.load_state_dict(self._best_model_state_dict)
                self.optimizer.load_state_dict(self._best_optimizer_state_dict)
                if self.lrScheduler is not None:
                    self.lrScheduler.load_state_dict(self._best_lrScheduler_state_dict)
                self.calculate_model()
        return "continue"
    def calculate_model(self, dataloader=None, model=None):
        '''
        如果不指定, 则用类内的
        :param dataloader: 默认self.val_loader
        :param model: 默认self.model
        :return: accuracy, f1_score, confusion_matrix, inference_time, params
        '''
        if dataloader==None:
            dataloader = self.val_loader
        if model==None:
            model = self.model
        model.eval()
        correct = 0
        total = 0
        y_true = []
        y_pred = []
        inference_time = []
        with torch.no_grad():
            for inputs, labels in dataloader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                start_time = time.time()
                outputs = model(inputs)
                end_time = time.time()
                _, predicted = torch.max(outputs, 1)

                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                y_true.extend(labels.cpu().numpy())
                y_pred.extend(predicted.cpu().numpy())
                inference_time.append(end_time - start_time)

                self._spikingjelly_process()
            # 平均推理时间
            inference_time = sum(inference_time) / len(inference_time)
            # acc & f1 & cm
            accuracy = correct / total
            f1_score = self._get_f1_score(y_true, y_pred)
            confusion_matrix = self._get_confusion_matrix(y_true, y_pred)
            # 参数量
            params = sum(p.numel() for p in model.parameters())

            info = f'[calc] accuracy: {accuracy:.3f}, f1_score: {f1_score:.3f}'
            self._print_and_toWriter(info)
            info = f'------ inference_time: {inference_time:.2e}s, params: {params / 1e3}K'
            self._print_and_toWriter(info)

            if self.isBinaryCls:
                TN = confusion_matrix[0, 0]
                FP = confusion_matrix[0, 1]
                FN = confusion_matrix[1, 0]
                TP = confusion_matrix[1, 1]
                L0_True = self._get_L0_True(TN, FP)
                L1_True = self._get_L1_True(FN, TP)

                info = f'------ L0_True: {L0_True:.3f}, L1_True: {L1_True:.3f}'
                self._print_and_toWriter(info)

        return accuracy, f1_score, confusion_matrix, inference_time, params

    def classify_unlabeled_data(self, dataloader) -> list:
        '''
        返回 预测标签
        '''
        self.model.eval()
        labels = []
        with torch.no_grad():
            for elements in dataloader:
                if len(elements) == 2:
                    inputs, _ = elements
                else:
                    inputs = elements
                inputs = inputs.to(self.device)
                outputs = self.model(inputs)
                _, predicted = torch.max(outputs, 1)
                labels.extend(predicted.cpu().numpy())
                self._spikingjelly_process()
        return labels

    def classify_labeled_data(self, dataloader) -> (list, list, float):
        '''
        返回 真实标签, 预测标签, acc
        '''
        self.model.eval()
        true_label = []
        pred_label = []
        with torch.no_grad():
            for inputs, labels in dataloader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                outputs = self.model(inputs)
                _, predicted = torch.max(outputs, 1)
                true_label.extend(labels.cpu().numpy())
                pred_label.extend(predicted.cpu().numpy())
                self._spikingjelly_process()
        # acc
        acc = (np.array(true_label) == np.array(pred_label)).sum() / len(true_label)
        return true_label, pred_label, acc

    def save_latest_checkpoint(self, path):
        '''
        字典checkpoint包含net, optimizer, lrScheduler
        '''
        parent_path = Path(path).parent
        os.makedirs(parent_path, exist_ok=True)

        checkpoint = {
            'model': self.model.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'lrScheduler': self.lrScheduler.state_dict() if self.lrScheduler is not None else None
        }
        torch.save(checkpoint, path)
        print(f"[save] latest_checkpoint 已保存到 {path}")

    def save_best_checkpoint(self, path):
        '''
        字典checkpoint包含net, optimizer, lrScheduler
        '''
        parent_path = Path(path).parent
        os.makedirs(parent_path, exist_ok=True)

        checkpoint = {
            'model': self._best_model_state_dict,
            'optimizer': self._best_optimizer_state_dict,
            'lrScheduler': self._best_lrScheduler_state_dict
        }
        torch.save(checkpoint, path)
        print(f"[save] best_checkpoint 已保存到 {path}")
    def load_model(self, path):
        checkpoint = torch.load(path, map_location='cpu')
        model_state_dict = checkpoint['model']

        flag_model = isinstance(self.model, nn.DataParallel)
        flag_dict = list(model_state_dict.keys())[0].startswith('module.')
        if (not flag_model) and flag_dict:
            model_state_dict = {k[7:]: v for k, v in model_state_dict.items()}
        if flag_model and (not flag_dict):
            model_state_dict = {'module.' + k: v for k, v in model_state_dict.items()}

        self.model.load_state_dict(model_state_dict)
        self.model.to(self.device)
        print(f"[load] model 已从 {path} 加载")
    def load_optimizer(self, path):
        checkpoint = torch.load(path)
        optimizer_state_dict = checkpoint['optimizer']
        self.optimizer.load_state_dict(optimizer_state_dict)
        print(f"[load] optimizer 已从{path}加载")
    def load_lrScheduler(self, path):
        checkpoint = torch.load(path)
        lrScheduler_state_dict = checkpoint['lrScheduler']
        if self.lrScheduler is not None and lrScheduler_state_dict is not None:
            self.lrScheduler.load_state_dict(lrScheduler_state_dict)
            print(f"[load] lrScheduler 已从{path}加载")
        else:
            print(f"[load] path中的lrScheduler为None, 加载失败")

    def set_writer1(self, path: Path, mode: Literal["a", "w"] = "a"):
        '''
        请在训练前设置set_writer
        '''
        self.writer = B_Writer(path, ifTime=True)
        if mode == 'a':
            pass
        if mode == 'w':
            self.writer.clearFile()

        self.writer.toFile("[dataset] -> " + self.train_loader.dataset.__class__.__name__, ifTime=False)
        self.writer.toFile("[batch_size] -> " + str(self.train_loader.batch_size), ifTime=False)
        self.writer.toFile("[lr] -> " + str(self.optimizer.param_groups[0]['lr']), ifTime=False)
        self.writer.toFile("[criterion] -> " + str(self.criterion), ifTime=False)
        self.writer.toFile("[optimizer] -> " + str(self.optimizer), ifTime=False)
        if self.lrScheduler is not None:
            self.writer.toFile("[lrScheduler] -> " + str(self.lrScheduler), ifTime=False)
        self.writer.toFile("[model] -> " + str(self.model), ifTime=False)

        print(f'[set] 日志将保存到{path}')
        return self.writer

    def set_writer2(self, writer: B_Writer, mode: Literal["a", "w"] = "a"):
        '''
        请在训练前设置set_writer
        '''
        self.writer = writer
        if mode == 'a':
            pass
        if mode == 'w':
            self.writer.clearFile()

        self.writer.toFile("[dataset] -> " + self.train_loader.dataset.__class__.__name__, ifTime=False)
        self.writer.toFile("[batch_size] -> " + str(self.train_loader.batch_size), ifTime=False)
        self.writer.toFile("[lr] -> " + str(self.optimizer.param_groups[0]['lr']), ifTime=False)
        self.writer.toFile("[criterion] -> " + str(self.criterion), ifTime=False)
        self.writer.toFile("[optimizer] -> " + str(self.optimizer), ifTime=False)
        if self.lrScheduler is not None:
            self.writer.toFile("[lrScheduler] -> " + str(self.lrScheduler), ifTime=False)
        self.writer.toFile("[model] -> " + str(self.model), ifTime=False)

        print(f'[set] 日志将保存到{self.writer.path}')
        return self.writer

    def set_save_during_train(self, path: Path, rounds=10):
        '''
        请在训练前设置set_save_during_train
        '''
        self._save_during_train = _saveDuringTrain(path, rounds)
        self._print_and_toWriter(f"[set] save_during_train")
    def set_stop_by_acc(self, rounds=10, delta=0.01):
        '''
        请在训练前设置set_stop_by_acc
        :param rounds: 连续rounds次, val_acc - max_val_acc > delta, 则停止训练
        '''
        self._stop_by_acc.func = B_StopByAcc(rounds=rounds, delta=delta)
        self._print_and_toWriter(f"[set] stop_by_acc")
    def set_stop_by_overfitting(self, rounds=10, delta=0.1):
        '''
        请在训练前设置set_stop_by_overfitting
        :param rounds: 连续rounds次, train_acc - val_acc > delta, 则停止训练
        '''
        self._stop_by_overfitting.func = B_StopByOverfitting(rounds=rounds, delta=delta)
        self._print_and_toWriter(f"[set] stop_by_overfitting")
    def set_stop_by_acc_delta(self, rounds=10, delta=0.003):
        '''
        请在训练前设置set_stop_by_acc_delta
        :param rounds: 连续rounds次, |before_acc - val_acc| <= delta, 则停止训练
        '''
        self._stop_by_acc_delta.func = B_StopByAccDelta(rounds=rounds, delta=delta)
        self._print_and_toWriter(f"[set] stop_by_acc_delta")
    def set_stop_by_loss(self, rounds=10, delta=.0, target_loss=0.01):
        '''
        请在训练前设置set_stop_by_loss
        :param rounds: 连续rounds次, train_loss > min_train_loss - delta, 则停止训练
        '''
        self._stop_by_loss.func = B_StopByLoss(rounds=rounds, delta=delta, target=target_loss)
        self._print_and_toWriter(f"[set] stop_by_loss")
    def set_stop_by_loss_delta(self, rounds=10, delta=0.002):
        '''
        请在训练前设置set_stop_by_loss_delta
        :param rounds: 连续rounds次, |before_loss - now_loss| <= delta, 则停止训练
        '''
        self._stop_by_loss_delta.func = B_StopByLossDelta(rounds=rounds, delta=delta)
        self._print_and_toWriter(f"[set] stop_by_loss_delta")
    def set_stop_by_byzh(self, loss_rounds=50, loss_target=0.001, acc_rounds=50, acc_target=1):
        '''
        请在训练前设置set_stop_by_byzh
        '''
        self._stop_by_byzh.func = B_StopByByzh(loss_rounds, loss_target, acc_rounds, acc_target)
        self._print_and_toWriter(f"[set] stop_by_byzh")
    def set_reload_by_loss(self, max_reload_count=5, reload_rounds=10, delta=0.01):
        '''
        请在训练前设置set_reload_by_loss\n
        :param reload_rounds: 连续reload_rounds次都是train_loss > min_train_loss + delta
        '''
        self._reload_by_loss.func = B_ReloadByLoss(max_reload_count, reload_rounds, delta)
        self._print_and_toWriter(f"[set] reload_by_loss")

    def draw(self, path: Path, if_show=False):
        """
        :param path: 如果以.csv结尾, 则保存为csv文件, 否则保存为图片
        :param if_show:
        :return:
        """
        path = Path(path)
        parent_path = path.parent
        os.makedirs(parent_path, exist_ok=True)
        file_name = path.name
        suffix = file_name.split('.')[-1]
        if suffix == 'csv':
            df = pd.DataFrame(
                data=[self.train_loss_batches_lst, self.train_acc_lst, self.val_acc_lst],
                index=["train_loss", "train_acc", "val_acc"]
            )
            df.to_csv(path, index=True, header=False)
            return

        if if_show == False:
            matplotlib.use('Agg')

        palette = sns.color_palette("Set2", 3)

        plt.figure(figsize=(8, 8))
        plt.subplots_adjust(hspace=0.4)

        plt.subplot(3, 1, 1)
        # 每十个画一次(防止点多卡顿)
        temp = [x for i, x in enumerate(self.train_loss_batches_lst) if (i + 1) % 10 == 0]
        plt.plot(temp, color="red", label="train_loss")
        plt.xlabel("iter 1/10", fontsize=18)
        plt.ylabel("loss", fontsize=18)
        plt.legend(loc='upper right', fontsize=16)
        plt.grid(True)

        plt.subplot(3, 1, 2)
        plt.plot(self.train_acc_lst, color="red", label="train_acc")
        plt.plot(self.val_acc_lst, color="blue", label="val_acc")
        # 找到train_acc的峰值点并标记
        train_acc_peak_index = np.argmax(self.train_acc_lst)
        plt.scatter(train_acc_peak_index, self.train_acc_lst[train_acc_peak_index], color="red", marker="v", s=100)
        # 找到val_acc的峰值点并标记
        val_acc_peak_index = np.argmax(self.val_acc_lst)
        plt.scatter(val_acc_peak_index, self.val_acc_lst[val_acc_peak_index], color="blue", marker="v", s=100)
        plt.xlabel("epoch", fontsize=18)
        plt.ylabel("acc", fontsize=18)
        plt.ylim(-0.05, 1.05)
        plt.legend(loc='lower right', fontsize=16)
        plt.grid(True)

        if self.isBinaryCls:
            plt.subplot(3, 1, 3)
            plt.plot(self.val_f1_lst, color=palette[0], label="f1")
            plt.plot(self.val_L0_True_lst, color=palette[1], label="L0_True")
            plt.plot(self.val_L1_True_lst, color=palette[2], label="L1_True")

            # 找到val_f1的峰值点并标记
            val_f1_peak_index = np.argmax(self.val_f1_lst)
            plt.scatter(val_f1_peak_index, self.val_f1_lst[val_f1_peak_index], color=palette[0], marker="v", s=100)

            # 找到val_L0_True的峰值点并标记
            val_L0_True_peak_index = np.argmax(self.val_L0_True_lst)
            plt.scatter(val_L0_True_peak_index, self.val_L0_True_lst[val_L0_True_peak_index], color=palette[1],
                        marker="v", s=100)

            # 找到val_L1_True的峰值点并标记
            val_L1_True_peak_index = np.argmax(self.val_L1_True_lst)
            plt.scatter(val_L1_True_peak_index, self.val_L1_True_lst[val_L1_True_peak_index], color=palette[2],
                        marker="v", s=100)

            plt.xlabel("epoch")
            plt.ylabel("score")
            plt.ylim(-0.05, 1.05)
            plt.legend(loc='lower right')

        plt.tight_layout()
        plt.savefig(path)
        print(f"[draw] picture 已保存到{path}")
        if if_show:
            plt.show()
        plt.close()

    def draw_cm(self, cm, path: Path, cmap='Reds', str_truelabel:list[str]=None, str_predlabel:list[str]=None, if_show=False):
        '''
        draw_confusion_matrix
        '''
        cm = np.array(cm)
        labels = [i for i in range(len(cm))]

        if str_truelabel is None:
            str_truelabel = labels
        if str_predlabel is None:
            str_predlabel = labels

        # 绘制热力图
        plt.figure(figsize=(7, 6))
        ax = sns.heatmap(cm, annot=True, fmt="d", cmap=cmap, xticklabels=str_truelabel, yticklabels=str_predlabel, annot_kws={"size": 16})
        # ax.xaxis.set_ticks_position("top")  # 将 X 轴的刻度移动到顶部
        # ax.xaxis.set_label_position("top")  # 将 X 轴的标签移动到顶部
        plt.title('Confusion Matrix', fontsize=20)
        plt.xlabel("True Labels", fontsize=16)
        plt.ylabel("Predicted Labels", fontsize=16)
        plt.tight_layout()

        plt.savefig(path)
        print(f"[draw_cm] picture 已保存到{path}")
        if if_show:
            plt.show()
        plt.close()

        return plt

    def draw_cm2(self, true_label, pred_label, path: Path, cmap='Reds', str_truelabel:list[str]=None, str_predlabel:list[str]=None, if_show=False):
        '''
        draw_confusion_matrix
        '''
        cm = self._get_confusion_matrix(true_label, pred_label)
        labels = [i for i in range(len(cm))]

        if str_truelabel is None:
            str_truelabel = labels
        if str_predlabel is None:
            str_predlabel = labels

        # 绘制热力图
        plt.figure(figsize=(7, 6))
        ax = sns.heatmap(cm, annot=True, fmt="d", cmap=cmap, xticklabels=str_truelabel, yticklabels=str_predlabel, annot_kws={"size": 16})
        # ax.xaxis.set_ticks_position("top")  # 将 X 轴的刻度移动到顶部
        # ax.xaxis.set_label_position("top")  # 将 X 轴的标签移动到顶部
        plt.title('Confusion Matrix', fontsize=20)
        plt.xlabel("True Labels", fontsize=16)
        plt.ylabel("Predicted Labels", fontsize=16)
        plt.tight_layout()

        plt.savefig(path)
        print(f"[draw_cm] picture 已保存到{path}")
        if if_show:
            plt.show()
        plt.close()

        return plt

    def _print_and_toWriter(self, info: str, if_print=True):
        if if_print:
            print(info)
        if self.writer is not None:
            self.writer.toFile(info)
    def _train_once(self, epoch, epochs, inputs_func, outputs_func, labels_func):
        bar = B_Tqdm(total=len(self.train_loader))
        current_lr = self.optimizer.param_groups[0]['lr']

        self.model.train()
        correct = 0
        total = 0
        losses = 0
        for iter, (inputs, labels) in enumerate(self.train_loader):
            # 基本训练
            inputs, labels = inputs.to(self.device), labels.to(self.device)
            labels = labels_func(labels)
            inputs = inputs_func(inputs)
            outputs = self.model(inputs)
            outputs = outputs_func(outputs)

            loss = self.criterion(outputs, labels)
            self.optimizer.zero_grad()  # 清零梯度
            loss.backward()  # 计算梯度
            self.optimizer.step()  # 更新参数
            # SNN
            self._spikingjelly_process()
            # 进度条
            bar.update(
                1,
                color=B_Color.BLUE + B_Appearance.HIGHLIGHT,
                prefix=f"{B_Color.BLUE}Epoch [{epoch:0{len(str(epochs))}}/{epochs}]",
                suffix=f"lr: {current_lr:.2e}, loss: {loss.item():.3f}"
            )
            # 数据记录
            self.train_loss_batches_lst.append(loss.item())
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            losses += loss.item()
        accuracy = correct / total
        train_loss = losses / len(self.train_loader)
        # 资源占用信息
        usage = ' '
        if self.device == torch.device('cuda'):
            gpu = b_get_gpu_nvidia()[0]
            usage = f' (GPU: {gpu[-2]}/{gpu[-1]}) '
        elif self.device == torch.device('cpu'):
            # 获取cpu的使用率
            usage = ' (CPU) '

        print(f'Epoch [{epoch:0{len(str(epochs))}}/{epochs}]{usage}(train_loss: {train_loss:.3f}) train_Acc: {accuracy:.3f}', end='')
        self.train_acc_lst.append(accuracy)
        self.train_loss_epoch_lst.append(train_loss)
        # 更新学习率
        if self.lrScheduler:
            self.lrScheduler.step()

        return accuracy, train_loss, current_lr

    def _eval_once(self, inputs_func, outputs_func, labels_func):
        self.model.eval()
        correct = 0
        total = 0
        y_true = []
        y_pred = []
        with torch.no_grad():
            for inputs, labels in self.val_loader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                labels = labels_func(labels)
                inputs = inputs_func(inputs)
                outputs = self.model(inputs)
                outputs = outputs_func(outputs)
                _, predicted = torch.max(outputs, 1)

                self._spikingjelly_process()

                total += labels.size(0)
                correct += (predicted == labels).sum().item()

                y_true.extend(labels.cpu().numpy())
                y_pred.extend(predicted.cpu().numpy())

            # 记录accuracy
            accuracy = correct / total
            print(f', val_Acc: {accuracy:.3f}', end='')
            self.val_acc_lst.append(accuracy)

            # 保存最优模型
            if accuracy > self._best_acc:
                self._best_acc = accuracy
                self._best_model_state_dict = copy.deepcopy(self.model.state_dict())
                self._best_optimizer_state_dict = copy.deepcopy(self.optimizer.state_dict())
                self._best_lrScheduler_state_dict = copy.deepcopy(self.lrScheduler.state_dict()) if self.lrScheduler else None

            if self.isBinaryCls:
                cm = self._get_confusion_matrix(y_true, y_pred)
                TN = cm[0, 0]
                FP = cm[0, 1]
                FN = cm[1, 0]
                TP = cm[1, 1]

                f1 = self._get_f1_score(y_true, y_pred)
                self.val_f1_lst.append(f1)

                L0_True = self._get_L0_True(TN, FP)
                self.val_L0_True_lst.append(L0_True)

                L1_True = self._get_L1_True(FN, TP)
                self.val_L1_True_lst.append(L1_True)

        return accuracy

    def _test_once(self, inputs_func, outputs_func, labels_func):
        assert self.test_loader is not None, "test_loader is None"

        self.model.eval()
        with torch.no_grad():
            correct = 0
            total = 0
            for inputs, labels in self.test_loader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                labels = labels_func(labels)
                inputs = inputs_func(inputs)
                outputs = self.model(inputs)
                outputs = outputs_func(outputs)
                _, predicted = torch.max(outputs, 1)

                self._spikingjelly_process()

                total += labels.size(0)
                correct += (predicted == labels).sum().item()

            # 记录accuracy
            accuracy = correct / total

            print(f', test_Acc: {accuracy:.3f}', end='')
        return accuracy
    def _spikingjelly_process(self):
        if self.isSpikingjelly14:
            from spikingjelly.activation_based import functional
            functional.reset_net(self.model)
        elif self.isSpikingjelly12:
            from spikingjelly.clock_driven import functional
            functional.reset_net(self.model)
    def _get_confusion_matrix(self, y_true, y_pred):
        from sklearn.metrics import confusion_matrix
        result = confusion_matrix(y_true, y_pred)
        return result
    def _get_f1_score(self, y_true, y_pred):
        from sklearn.metrics import f1_score
        result = f1_score(y_true, y_pred, average='macro')
        return result
    def _get_recall(self, y_true, y_pred):
        from sklearn.metrics import recall_score
        result = recall_score(y_true, y_pred, average='macro')
        return result
    def _get_precision(self, y_true, y_pred):
        from sklearn.metrics import precision_score
        result = precision_score(y_true, y_pred, average='macro')
        return result

    def _get_L0_True(self, TN, FP):
        return TN / (TN + FP)

    def _get_L1_True(self, FN, TP):
        return TP / (TP + FN)