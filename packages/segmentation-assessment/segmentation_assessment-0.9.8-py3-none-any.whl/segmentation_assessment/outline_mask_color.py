#from IMC_library import function
import function
import os
import matplotlib
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2
path_img=input("Enter the path to the folder containing the images: ")
path_mask=input("Enter the path to the folder containing the masks: ")
path_truth=input("Enter the path to the folder containing the masks done manually: ")
threshold=float(input("Enter iou threshold: "))
min_size=float(input("Enter the minimum size (or -1 for auto): "))
max_size=float(input("Enter the maximum size (or -1 for auto): "))
if min_size==-1 or max_size==-1:
    step=int(input("Enter the increment step: "))

if min_size==-1:
    min_size,iou=function.calcul_min_size(path_img,path_mask,path_truth,step)
if max_size==-1:
    max_size,iou_max=function.calcul_max_size(path_img,path_mask,path_truth,step)

function.outline_mask_color(path_img,path_mask,path_truth,min_size,max_size)