# SWT_ML
Inferring shear wave velocity structure from surface wave dispersion data using Neural Network

with Mengyu Wu

## Contents
rawData: IRIS

data:   scripts to convert information in rawData to ML input (inputs are also saved here temporarily)
    syn_disp_from_vs:  calculating synthetic dispersion based on vs profile
    dataPrepare.py:    preparing training dataset(US) and testing dataset(CN)

train:  scripts to do training and predicting
    Main_Train.py:    run training (set self.pretrained = False, self.start = 0 in config.py before training)
    Main_Predict.py:  predicting (set self.pretrained = True, self.start = 600 in config.py before predicting)
    checkLayer.py:    plot a map to check result


## work flow
1. data/dataPrepare.py, four parts separated by docstring
2. Main_Train.py
3. Main_Predict.py

## poster
![Poster](Poster.jpg)
