#from IMC_library import function
import function

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

iou,dico_objet,df_mask,df_truth=function.calcul_iou(path_img,path_mask,path_truth,min_size,max_size)
function.outline_iou(path_img,df_mask,threshold,c=0)
function.outline_iou("./segmentation_quality/mask_outline_iou.png",df_truth,threshold,c=255)
