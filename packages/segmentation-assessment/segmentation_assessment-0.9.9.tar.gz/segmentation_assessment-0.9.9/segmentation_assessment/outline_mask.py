#from IMC_library import function
import function

path_img=input("Enter the path to the folder containing the images: ")
path_mask=input("Enter the path to the folder containing the masks: ")
marker=input("Enter one marker (no necessary): ")

#list_marker=marker.split(",")
function.display_outline_mask_files(path_img,path_mask,marker)