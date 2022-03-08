import yaml
import datetime
import time
from yaml.loader import SafeLoader
import threading
import csv

file1 = open("LogFile1.txt", "w")
no_of_defects = -1


def timeWait(flowName, taskName, secs, input):
    ct1 = str(datetime.datetime.now())
    string = ct1 + ';' + flowName + '.' + taskName + ' Executing TimeFunction(' + input + ',' + secs + ')'
    file1.write(string + '\n')
    time.sleep(int(secs))


def seq1(flowName, activity, name):
    if activity['Type'] == 'Task':
        ct1 = str(datetime.datetime.now())
        string = ct1 + ';' + flowName + '.' + name + ' Entry'
        file1.write(string + '\n')
        timeWait(flowName, name, activity['Inputs']['ExecutionTime'], activity['Inputs']['FunctionInput'])
        ct2 = str(datetime.datetime.now())
        string1 = ct2 + ';' + flowName + '.' + name + ' Exit'
        file1.write(string1 + '\n')
    else:
        ct1 = str(datetime.datetime.now())
        string = ct1 + ';' + flowName + '.' + name + ' Entry'
        file1.write(string + '\n')
        if activity['Execution'] == 'Sequential':
            seq(flowName + '.' + name, activity['Activities'])
        ct1 = str(datetime.datetime.now())
        string = ct1 + ';' + flowName + '.' + name + ' Exit'
        file1.write(string + '\n')


def seq(flowName, activities):
    global no_of_defects
    for i in activities.keys():
        if activities[i]['Type'] == 'Task':
            if activities[i]['Function'] == "TimeFunction":
                ct1 = str(datetime.datetime.now())
                string = ct1 + ';' + flowName + '.' + i + ' Entry'
                file1.write(string + '\n')
                timeWait(flowName, i, activities[i]['Inputs']['ExecutionTime'],
                         activities[i]['Inputs']['FunctionInput'])
                ct2 = str(datetime.datetime.now())
                string1 = ct2 + ';' + flowName + '.' + i + ' Exit'
                file1.write(string1 + '\n')

            elif activities[i]['Function'] == "DataLoad":
                boole = True
                if 'Condition' in activities[i]:
                    val = int(activities[i]['Condition'][-1])
                    sign = activities[i]['Condition'][-3]
                    if sign == '>':
                        if no_of_defects < val:
                            boole = False
                    if sign == '<':
                        if no_of_defects > val:
                            boole = False
                if True:
                    if no_of_defects == -1 or boole:
                        ct1 = str(datetime.datetime.now())
                        string = ct1 + ';' + flowName + '.' + i + ' Entry'
                        file1.write(string + '\n')
                        filename = activities[i]['Inputs']['Filename']
                        string = ct1 + ';' + flowName + '.' + i + ' Executing DataLoad(' + filename + ')'
                        file1.write(string + '\n')
                        with open(filename, 'r', newline='') as file:
                            data = csv.reader(file)
                            for row in data:
                                no_of_defects += 1
                        file.close()
                        ct1 = str(datetime.datetime.now())
                        string = ct1 + ';' + flowName + '.' + i + ' Entry'

        if activities[i]['Type'] == 'Flow':
            ct1 = str(datetime.datetime.now())
            string = ct1 + ';' + flowName + '.' + i + ' Entry'
            file1.write(string + '\n')
            if activities[i]['Execution'] == 'Sequential':
                seq(flowName + '.' + i, activities[i]['Activities'])
            elif activities[i]['Execution'] == 'Concurrent':
                Threads = []
                for j in activities[i]['Activities'].keys():
                    t = threading.Thread(target=seq1, args=[flowName + '.' + i, activities[i]['Activities'][j], j])
                    Threads.append(t)
                    t.start()
                for j in range(len(Threads)):
                    Threads[j].join()

            ct1 = str(datetime.datetime.now())
            string = ct1 + ';' + flowName + '.' + i + ' Exit'
            file1.write(string + '\n')


with open('Milestone2A.yaml') as f:
    docs1 = yaml.load(f, Loader=SafeLoader)
f.close()

for k in docs1.keys():
    ct = str(datetime.datetime.now())
    s = ct + ';' + k + ' Entry'
    file1.write(s + '\n')
    if docs1[k]['Type'] == "Flow":
        if docs1[k]['Execution'] == 'Sequential':
            seq(k, docs1[k]['Activities'])
    ct = str(datetime.datetime.now())
    s = ct + ';' + k + ' Exit'
    file1.write(s + '\n')

file1.close()
