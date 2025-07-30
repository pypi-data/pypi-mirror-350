import function
#from IMC_library import function
import numpy as np
import matplotlib.pyplot as plt
path_img=input("Saisir le chemin d'acces du dossier contenant les images: ")
path_mask=input("Saisir le chemin d'acces du dossier contenant les masques: ")
path_truth=input("Saisir le chemin d'acces du dossier contenant les masques fait manuellement: ")

function.calcul_auc(path_img,path_mask,path_truth,min_size,max_size)

