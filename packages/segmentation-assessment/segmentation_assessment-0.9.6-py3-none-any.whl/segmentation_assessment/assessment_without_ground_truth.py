from IMC_library import function

path_img=input("Enter the path to the folder containing the images: ")
path_mask=input("Enter the path to the folder containing the masks: ")
marker_display=input("Enter one marker to display it on the images(no necessary): ")
markers_signal=input("Enter the markers to calculate the percentage in/out (separate by a comma): ")


list_marker=marker_display.split(",")
function.display_outline_mask(path_img,path_mask,marker_display)

list_marker=markers_signal.split(",")
function.percentage_in_out(list_marker)

function.distribution_number_object()


function.size_distribution(path_mask)

