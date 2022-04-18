#!/usr/bin/env python3
#-*- coding: utf-8 -*-
'''
Author: Jing Hu
Date: 2020-11-23 14:36:51
LastEditTime: 2020-11-23 20:57:17
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /SurfTomoCNN-new/config.py
'''
class Config(object):
    def __init__(self):
        self.filepath_disp_training     = '../data_cas/Input_disp_combine_gaussian_map/'
        self.filepath_vs_training       = '../data_cas/Input_Vs/'

        self.filepath_disp_real    = '../data_cas/Input_predict/' 


        ''' 
        change start = 0, pretrained = False before training
        change start = 600, pretrained = True before predicting
        '''
        self.batch_size = 64     # training batch size
        self.nEpochs = 600       # maximum number of epochs to train for
        self.lr = 0.00001        # learning rate
        self.seed = 123          # random seed to use. Default=123
        self.plot = True         # show validation result during training
        self.alpha=0.0000        # damping, not used here 
        self.testsize=0.2
        self.pretrained = True
        self.start = 600
        self.pretrain_net = "./model_para/model_epoch_"+str(self.start)+".pth"

        # config added by Ayu
        # self.inchannel = 2   # 1 for phase vel only, 2 for both phase and group

if __name__ == '__main__':
    pass
