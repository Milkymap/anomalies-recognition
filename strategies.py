import cv2 

import numpy as np 
import operator as op 
import itertools as it, functools as ft 

import torch as th 
import torch.nn as nn 
import torch.nn.functional as F 

from loguru import logger 

from os import path 
from torchvision import models 

def read_image(path2image, size=None):
    image = cv2.imread(path2image, cv2.IMREAD_COLOR)
    if size is not None:
        image = cv2.resize(image, size, cv2.INTER_CUBIC)
    return image 

def load_vectorizer(path2vectorizer):  # models/resnet.th 
    if path.isfile(path2vectorizer):
        vectorizer = th.load(path2vectorizer)
    else:
        logger.debug('the model will be downloaded')
        _, file_name = path.split(path2vectorizer)
        model_name = file_name.split('.')[0]
        try:
            grabber = op.attrgetter(model_name)(models)
        except Exception as e:
            raise ValueError(f'{model_name} is not a valid name, please check torchvision.models')
        vectorizer = grabber(pretrained=True, progress=True)
        vectorizer = nn.Sequential(*list(vectorizer.children())[:-1])
        for prm in vectorizer.parameters():
            prm.requires_grad = False
        vectorizer.eval()
        th.save(vectorizer, path2vectorizer) 
        logger.success('vectorizer was saved')
    return vectorizer



