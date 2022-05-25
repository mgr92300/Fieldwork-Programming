import os

monitorPath = r'C:\Users\michael\Desktop\RISCV_Investigacion\Python Project\Test\Monitor\\'
resultsPath = r'C:\Users\michael\Desktop\RISCV_Investigacion\Python Project\Test\Mibench results\\'

def fileMapper(Path):
    logFiles = []
    for file_name in os.listdir(Path):
        logFiles.append(Path + file_name)        
    return(logFiles)

def _monitorReader(list,count):
    J = 0
    fileList = []
    while(J <= count):
        try:
            file = open(list[J], "r", encoding = "UTF-8", errors = 'ignore')
            if file.closed:
                print("SEM log file (SEMlog.txt) couldn't be found in this folder")
            else:
                lines = file.readlines()
                #Border("File Active: SEM_log_{}".format(J))
                fileList.append(__monitorInterpreter(lines))
                file.close()
        except (UnicodeEncodeError):
            print("Error found within detected file")
            print("File Detected: SEMlog_{}".format(J))
        J += 1
    __monitorCompilation(fileList)

def __monitorCompilation(compLists):
    sumList = [0,0,0,0,0,0,0,0]
    index = 0
    for list in compLists:
        for index in range(8):
            sumList[index] += list[index]

    injectionCount = sumList[0]
    repeatedCount = sumList[1]
    per = 100*(1 - (repeatedCount/injectionCount))
    CNEerror = sumList[2]
    CEerror= sumList[3]
    UEerror = sumList[4]
    UNEerror = sumList[5]
    fatalError = sumList[6]
    restarts = sumList[7]

    Border("Compilation report", '*')

    print("Out of a total of {} injections, {} addresses were repeated, making a {}% of non-repeated address values.".format(injectionCount, repeatedCount, round(per,2)))
    print("The injections produced a total of {} errors: ".format(CNEerror + CEerror + UEerror + UNEerror))
    print("\t - Correctable, Non Essential: {}".format(CNEerror))
    print("\t - Uncorrectable, Non Essential: {}".format(UNEerror))
    print("\t - Correctable, Essential: {}".format(CEerror))
    print("\t - Uncorrectable, Essential: {}".format(UEerror))
    
    print("The injections caused the SEM to enter in Fatal Error State {} times.".format(fatalError))
    print("The FPGA was reset {} times".format(restarts))

def __monitorInterpreter(lines):    
    addresses = []
    injectionCount = 0
    repeatedCount = 0
    CNEerror = 0
    UNEerror = 0
    CEerror = 0
    UEerror = 0
    fatalError = 0
    restarts = 0
    classificationOn = False
    injectionFlag = False

    for line in lines:
        #Injection counter
        if "I> N" in line:
            injectionCount += 1
            data = line.split(" ")
            if len(data) == 3:
                injectionAddress = data[2]
                if injectionAddress in addresses:
                    repeatedCount += 1
                else:
                    addresses.append(injectionAddress)
            
        elif "SC 10" in line:
            injectionFlag = True
        
        elif "SC 08" in line:
            classificationOn = True   
        
        elif "FC 00" in line:    #Correctable Not Essential
            CNEerror += 1

        #Classification Accumulator
        elif ("FC" in line and classificationOn):
            #Switch depending on the the hex code after     
            if "FC 20" in line:  #Uncorrectable Not essential
                UNEerror += 1
            elif "FC 40" in line:  #Correctable Essential
                CEerror += 1
            elif "FC 60" in line:  #Uncorrectable Non essential
                UEerror +=1
            classificationOn = False
        
        #Fatal error
        elif "SC 1F" in line:
            fatalError += 1
        elif "ICAP OK" in line:               #initialization code. Since i have to do it manually, this is actually a good place to count the FPGA restarts 
            restarts += 1

    per = 100*(1 - (repeatedCount/injectionCount))
    #print("Out of a total of {} injections, {} addresses were repeated, making a {}% of non-repeated address values.".format(injectionCount, repeatedCount, round(per,2)))
    #print("The injections produced a total of {} errors: ".format(CNEerror + CEerror + UEerror + UNEerror))
    #print("\t - Correctable, Non Essential: {}".format(CNEerror))
    #print("\t - Uncorrectable, Non Essential: {}".format(UNEerror))
    #print("\t - Correctable, Essential: {}".format(CEerror))
    #print("\t - Uncorrectable, Essential: {}".format(UEerror))
    
    #print("The injections caused the SEM to enter in Fatal Error State {} times.".format(fatalError))
    #print("The FPGA was reset {} times".format(restarts-1))

    valList = [injectionCount, repeatedCount, CNEerror, CEerror, UEerror, UNEerror, fatalError, restarts - 1]
    return(valList)

def _resultReader(key,list,count):
    keyFile = open(key, "r", encoding = "utf-8")
    keyLines = keyFile.readlines()
    I = 0
    fileList = []
    while(I < count):
        try:
            file = open(list[I], "r", encoding = "utf-8")
            if file.closed:
                print("Result log file (Result_{}.txt) couldn't be found in this folder".format(I))
            else:
                Lines = file.readlines()
                #print("File Active: Result_{}".format(I))
                fileList.append(__resultKeyComparator(keyLines,Lines))
               
            file.close()
        except:
            print("Error encountered")
            print("Result log file (Result_{}.txt) caused this error".format(I))  
        #printLines('-')
        I += 1
    __resultCompilation(fileList)
    
def __resultKeyComparator(key, lines):
    Match = 0
    PC = 0
    EC = 0
    FE = 0
    ProgramCounter = 0
    RC = 0
    totalLine = len(lines)
    for index,line in enumerate(lines):
        if line in key:
            Match += 1
            if line == key[0]:
                ProgramCounter = index
            elif line == key[-1]:
                Run = index - ProgramCounter
                if Run == len(key)-1:
                    PC += 1
                else:
                    RC += 1
                    if index + 1 >= len(lines):
                        RC -= 1
        else:
            EC += 1
            if (not lines[index].isascii()):
                FE += 1    

    if (PC == 0 and EC == 0 and FE == 0 and RC == 0):
        return([0,0,0,0,0, 0])
    else:
        resultList = [PC,EC,FE,RC, Match, totalLine]
        return(resultList)

def __resultCompilation(compLists):
    sumList = [0,0,0,0,0,0]
    index = 0
    for list in compLists:
        for index in range(6):
            sumList[index] += list[index]

    PC = sumList[0]
    EC = sumList[1]
    FE = sumList[2]
    RC = sumList [3]
    Match = sumList[4]
    totalLines = sumList[5]

    SuccessPer = (((PC*171) / Match))
    ERRper = 1- SuccessPer
    FatalitiesPer = (1-(FE/EC))

    Border("Compilation Report", '*')
    print("Out of total of {} lines, {} were successful.".format(totalLines, Match))
    print("Number of Successful Program Executions: {}".format(PC))
    print("The Rates of Success: {}%".format(round(100*SuccessPer,5)))
    print("The Number of Recoveries were: {}".format(RC))
    print("Number of Errors caused in all the lines: {}".format(EC))
    print("The Rate of Errors were: {}%".format(round(100*ERRper,5)))
    print("Number of Times those Errors affected output chars: {} ".format(FE))
    print("The Rate of Fatalities were: {}%".format(round(100*FatalitiesPer,5)))

def Border(Title = " ", char = '-'):
    printLines(char)
    print(Title)
    printLines(char)

def printLines(Line):
    print(Line*128)  

def main():
    Border("SEM Execution", '=')
    monitorLogFiles = fileMapper(monitorPath)
    monitorLen = len(monitorLogFiles) - 1    
    _monitorReader(monitorLogFiles, monitorLen)

    Border("MiBench Execution", '=')

    resultFiles = fileMapper(resultsPath) 
    resultLen = len(resultFiles) - 1 
    _resultReader(resultFiles[0], resultFiles[1:], resultLen)
    
if __name__ == '__main__':
    main()