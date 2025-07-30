#from IMC_library import function
import function

path_img=input("Saisir le chemin d'acces du dossier contenant les images: ")
path_mask=input("Saisir le chemin d'acces du dossier contenant les masques: ")

function.size_distribution(path_img,path_mask)