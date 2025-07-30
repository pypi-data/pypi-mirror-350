import function
#from IMC_library import function

path_img=input("Saisir le chemin d'acces du dossier contenant les images: ")
path_mask=input("Saisir le chemin d'acces du dossier contenant les masques: ")
path_truth=input("Saisir le chemin d'acces du dossier contenant les masques fait manuellement: ")
threshold=float(input("Saisir le seuil: "))

print("\n")
iou,dico_objet,df_mask,df_truth=function.calcul_iou(path_img,path_mask,path_truth)
recall,precision,true_pos,false_pos,false_neg=function.recall_precision(threshold,df_mask,df_truth)
print("IOU moyen: "+str(iou))
print("Recall= ",recall)
print("Precision= ",precision)
print("Nombre de vrai positif= ",true_pos)
print("Nombre de faux positif= ",false_pos)
print("Nombre de faux negatif= ",false_neg)



