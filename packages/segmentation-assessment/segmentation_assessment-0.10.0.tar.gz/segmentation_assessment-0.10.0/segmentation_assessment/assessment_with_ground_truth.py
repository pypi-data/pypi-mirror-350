from segmentation_assessment import function
import sys
import os
import numpy as np
path_img=input("Enter the path to the folder containing the images: ")
path_mask=input("Enter the path to the folder containing the masks: ")
#path_truth=input("Enter the path to the folder containing the masks done manually: ")

threshold=float(input("Enter iou threshold: "))
step=int(input("Enter the increment step: "))

if os.path.isdir("./segmentation_quality")==False:
    os.mkdir("./segmentation_quality")

sys.stdout = open('./segmentation_quality/summarize.txt', 'w')

#distribution of the size of mask objects done manually
function.size_distribution(path_mask,title="size_distribution.png")

function.distribution_number_object(path_img=path_img,path_mask=path_mask,title="number_objects.png")

#iou calculation without filter
print("Evaluation of the algorithm without size filter")
print("\n")
dico_algo_ap=function.calcul_auc(path_img,path_mask,title="Average_precision_without_size_filter")
for algo in os.listdir(path_mask):
 if algo!="truth":
    list_iou=[]
    list_precision=[]
    list_recall=[]
    list_true_pos=[]
    list_false_pos=[]
    list_false_neg=[]
    for file_img,file_mask in zip(os.listdir(path_img),os.listdir(path_mask+"/"+algo)):
        iou,dico_objet,df_mask,df_truth=function.calcul_iou(path_img+"/"+file_img,path_mask+"/"+algo+"/"+file_mask,path_mask+"/truth/"+file_mask)
        list_iou.append(iou)
        recall,precision,true_pos,false_pos,false_neg=function.recall_precision(threshold,df_mask,df_truth)
        list_precision.append(precision)
        list_recall.append(recall)
        list_true_pos.append(true_pos)
        list_false_pos.append(false_pos)
        list_false_neg.append(false_neg)
    print("*"*50)
    print(algo)
    print("*"*50)
    print("Mean IOU= "+str(np.mean(list_iou))+" (without size filter)")
    print("Average precision: "+str(dico_algo_ap[algo]))
    print("")
    print("Number of predicted objects: "+str(np.sum(list_true_pos)+np.sum(list_false_pos)))
    print("Real object number: "+str(np.sum(list_true_pos)+np.sum(list_false_neg)))
    #recall, precision, true positives
    print("")
    print("For an IOU threshold= "+str(threshold)+" :")
    print("   Recall= "+str(np.mean(list_recall)))
    print("   Precision= ",str(np.mean(list_precision)))
    print("   Number of true positive= ",str(np.sum(list_true_pos)))
    print("   Number of false positive= ",str(np.sum(list_false_pos)))
    print("   Number of false negative= ",str(np.sum(list_false_neg)))
    print("")



#calculation of the minimum and maximum size of the predicted mask objects that must be filtered
#max_size,iou=
dico_algo_max=function.calcul_max_size(path_img,path_mask,step)
#calculation of the minimum and maximum size of the predicted mask objects that must be filtered
dico_algo_min=function.calcul_min_size(path_img,path_mask,step)

dico_algo_ap=function.calcul_auc(path_img,path_mask,"Average_precision_with_size_filter",dico_algo_min,dico_algo_max)

#distribution of the size of mask objects with size filter
function.size_distribution(path_mask,dico_algo_min,dico_algo_max,title="size_distribution_filtered.png")
function.distribution_number_object(path_img=path_img,path_mask=path_mask,dico_algo_max=dico_algo_max,dico_algo_min=dico_algo_min,title="number_objects_filtered.png")

print("\n"*3)
print("Evaluation of the algorithm with a size filter")
print("\n")
for algo in os.listdir(path_mask):
  if algo!="truth":
    list_iou=[]
    list_recall=[]
    list_false_neg=[]
    list_true_pos=[]
    list_false_pos=[]
    list_precision=[]
    print("*"*100)
    print(algo)
    print("*"*100)
    for file_img,file_mask in zip(os.listdir(path_img),os.listdir(path_mask+"/"+algo)):
        #calcul de l'iou et dictionnaire avec paire objet predit/manuel et l'iou en valeur
        iou,dico_objet,df_mask,df_truth=function.calcul_iou(path_img+"/"+file_img,path_mask+"/"+algo+"/"+file_mask,path_mask+"/truth/"+file_mask,dico_algo_min[algo],dico_algo_max[algo])
        list_iou.append(iou)
        recall,precision,true_pos,false_pos,false_neg=function.recall_precision(threshold,df_mask,df_truth)
        list_precision.append(precision)
        list_recall.append(recall)
        list_true_pos.append(true_pos)
        list_false_pos.append(false_pos)
        list_false_neg.append(false_neg)

        #Display of predicted masks colored according to the iou (iou<threshold: red, iou>threshold: blue)
        function.outline_iou(path_img+"/"+file_img,file_img,algo,df_mask,threshold,c=0)
        function.outline_iou("./segmentation_quality/outline_iou/"+algo+"/"+file_img[:-4]+".png",file_img[:-4]+".png",algo,df_truth,threshold,c=255)

        #Display of predicted masks colored and the outline of the ground truth
        function.outline_mask_color(path_img,path_mask,algo,dico_algo_min[algo],dico_algo_max[algo])
    print("Algorithme: "+algo)
    print("Best IOU= "+str(np.mean(list_iou))+" by filtering objects <"+str(dico_algo_min[algo])+" pixels and >"+str(dico_algo_max[algo]))
    print("Average precision: "+str(dico_algo_ap[algo]))
    print("")
    print("Number of predicted objects: "+str(np.sum(list_true_pos)+np.sum(list_false_pos)))
    print("Real object number: "+str(np.sum(list_true_pos)+np.sum(list_false_neg)))

    #Calcul recall, precision, true positivess
    print("for a IOU threshold= "+str(threshold)+" :")
    print("   Recall= ",str(np.around(np.mean(list_recall),2)))
    print("   Precision= ",str(np.around(np.mean(list_precision),2)))
    print("   Number of true positive= ",str(np.sum(list_true_pos)))
    print("   Number of false positive= ",str(np.sum(list_false_pos)))
    print("   Number of false negative= ",str(np.sum(false_neg)))
    print("")


sys.stdout.close()

quit()