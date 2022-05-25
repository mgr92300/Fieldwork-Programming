import os

monitorPath = r'C:\Users\michael\Desktop\RISCV_Investigacion\Python Project\Test\Monitor\\'
mibenchPath = r'C:\Users\michael\Desktop\RISCV_Investigacion\Python Project\Test\Mibench results\\'

i = 0
j = 0
k = 0
#Mibench loop
for file_name in os.listdir(mibenchPath):
    if (file_name != "Key.txt"):
        file = mibenchPath + file_name
        newFile = mibenchPath + "Results_"+ str(j) + "_" + str(i) + ".txt"
        os.rename(file,newFile)
        i += 1
        if (i > 9):
            j += 1
            i = 0


#Monitor loop
for file_name in os.listdir(monitorPath):
    file = monitorPath + file_name
    newFile = monitorPath + "SEM_log_"+ str(k) + ".log"
    os.rename(file,newFile)
    k += 1


print("Finished Program")