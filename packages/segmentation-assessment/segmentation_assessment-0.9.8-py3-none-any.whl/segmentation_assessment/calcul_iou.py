#from IMC_library import function
import function

path_img=input("Saisir le chemin d'acces du dossier contenant les images: ")
path_mask=input("Saisir le chemin d'acces du dossier contenant les masques: ")
path_truth=input("Saisir le chemin d'acces du dossier contenant les masques fait manuellement: ")

iou=function.calcul_iou(path_img,path_mask,path_truth)
print(iou)