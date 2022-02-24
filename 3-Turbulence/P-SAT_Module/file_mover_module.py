import glob
import shutil
import os

# I prefer to set path and mask as variables, but of course you can use values
# inside glob() and move()
import datetime

target_folder_name = str(datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S_%f"))
source_files = '*Filtered_by*'
cmd = "mkdir Filtered_" + target_folder_name
os.system(cmd)
target_folder = "Filtered_"+target_folder_name

# retrieve file list
filelist = glob.glob(source_files)
for single_file in filelist:
    # move file with full paths as shutil.move() parameters
    shutil.move(single_file, target_folder)



source_files = '*_files_list.txt'   

# retrieve file list
filelist = glob.glob(source_files)
for single_file in filelist:
    # move file with full paths as shutil.move() parameters
    shutil.move(single_file, target_folder)




source_files = '*.dat'   

# retrieve file list
filelist = glob.glob(source_files)
for single_file in filelist:
    # move file with full paths as shutil.move() parameters
    shutil.move(single_file, target_folder)





# with open("input_files.txt", 'r') as f:
#     lines = f.readlines()
#     for line in lines:
#         shutil.move(line.strip(), target_folder)
#         # process_input_files(line.strip())
