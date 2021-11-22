#Script designed to extract and rename mods to paradox games downloaded via steamdownloader
#Download/move the archives to the mod folder
#The only thing you need to enter is your mod path
import os
import zipfile

#Function that appends the "path" and "name" lines at the begginig of a file
def preappend_line(file_name, line):
    dummy = file_name + ".mod"
    with open(file_name, 'r') as read_obj, open(dummy, 'w') as write_obj:
        write_obj.write(line)
        for line in read_obj:
            #Don't write the old "name" and "path" lines:
            if ("path" not in line) and ("name" not in line) :
                write_obj.write(line)
    os.remove(file_name)
    os.rename(dummy,file_name)

def pdx_install(path):
    directory = os.fsencode(path) if os.path.exists(path) else print("Invalid path")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".zip"): #TODO: Works only with .zip extension            
            #Unzip the mod files
            folder_name = os.path.splitext(filename.lstrip("0123456789_"))[0]#Optional: Strips any numbers at the front
            print("Unpacking " + folder_name)
            with zipfile.ZipFile(path + "/" + filename, 'r') as zip_ref:
                zip_ref.extractall(path + "/" + folder_name)
            #Delete the archive
            #os.remove(path + "/" + filename) # Optional
            
            #Extract descriptor
            for file in os.listdir(path + "/" + folder_name):
                if os.fsdecode(file).endswith(".mod"):
                    desc = os.fsdecode(file)
            os.replace(path + "/" + folder_name + "/" + desc, path + "/" + folder_name + ".mod")
            desc_path = path + "/" + folder_name + ".mod"
            
            #Add the path and name lines to the descriptor
            preappend_line(desc_path, "path=\"" + path + "/" + folder_name + "\"\n" + "name=\"" + folder_name + "\"\n")
            print("Finitto!")

pdx_install(input("Enter the path to the mod folder (ex. C:/Users/A/Documents/Paradox Interactive/Stellaris/mod): \n").replace("\\","/"))
input("Press enter to exit...")