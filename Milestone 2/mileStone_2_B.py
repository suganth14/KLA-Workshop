import yaml
import datetime
import time
from yaml.loader import SafeLoader
import threading
import csv
from collections import OrderedDict

file1 = open("MileStone2_LogFile2_B.txt", "w")
no_of_defects = {}


def timeWait(flowName, taskName, secs, input):
    ct1 = str(datetime.datetime.now())
    string = ct1 + ';' + flowName + '.' + taskName + ' Executing TimeFunction(' + input + ',' + secs + ')'
    file1.write(str(string + '\n'))
    time.sleep(int(secs))


def seq1(flowName, activity, name):
    global no_of_defects
    if activity['Type'] == 'Task':
        if activity['Function'] == 'TimeFunction':
            boole = True
            if 'Condition' in activity:
                condition = activity['Condition'][15:20]
                val = int(activity['Condition'][-1])
                sign = activity['Condition'][-3]
                while condition not in no_of_defects:
                    pass
                if sign == '>':
                    if no_of_defects[condition] < val:
                        boole = False
                if sign == '<':
                    if no_of_defects[condition] > val:
                        boole = False
            if boole:
                ct1 = str(datetime.datetime.now())
                string = ct1 + ';' + flowName + '.' + name + ' Entry'
                file1.write(str(string + '\n'))
                timeWait(flowName, name, activity['Inputs']['ExecutionTime'], activity['Inputs']['FunctionInput'])
                ct2 = str(datetime.datetime.now())
                string1 = ct2 + ';' + flowName + '.' + name + ' Exit'
                file1.write(str(string1 + '\n'))
            else:
                ct1 = str(datetime.datetime.now())
                string = ct1 + ';' + flowName + '.' + name + ' Entry'
                file1.write(str(string + '\n'))
                ct1 = str(datetime.datetime.now())
                string = ct1 + ';' + flowName + '.' + name + ' Skipped'
                file1.write(str(string + '\n'))
                ct2 = str(datetime.datetime.now())
                string1 = ct2 + ';' + flowName + '.' + name + ' Exit'
                file1.write(str(string1 + '\n'))

        else:
            boole = True
            if 'Condition' in activity:
                condition = activity['Condition'][15:20]
                val = int(activity['Condition'][-1])
                sign = activity['Condition'][-3]
                if sign == '>':
                    if no_of_defects[condition] < val:
                        boole = False
                if sign == '<':
                    if no_of_defects[condition] > val:
                        boole = False
            if True:
                if boole:
                    ct1 = str(datetime.datetime.now())
                    string = ct1 + ';' + flowName + '.' + name + ' Entry'
                    file1.write(str(string + '\n'))
                    filename = activity['Inputs']['Filename']
                    string = ct1 + ';' + flowName + '.' + name + ' Executing DataLoad(' + filename + ')'
                    file1.write(str(string + '\n'))
                    with open(filename, 'r', newline='') as file:
                        data = csv.reader(file)
                        no_of_d = -1
                        for row in data:
                            no_of_d += 1
                        no_of_defects[name] = no_of_d
                    file.close()
                    ct1 = str(datetime.datetime.now())
                    string = ct1 + ';' + flowName + '.' + name + ' Exit'
                    file1.write(str(string + '\n'))

    else:
        ct1 = str(datetime.datetime.now())
        string = ct1 + ';' + flowName + '.' + name + ' Entry'
        file1.write(str(string + '\n'))
        if activity['Execution'] == 'Sequential':
            seq(flowName + '.' + name, activity['Activities'])
        if activity['Execution'] == 'Concurrent':
            Threads = []
            for j in activity['Activities'].keys():
                t = threading.Thread(target=seq1, args=[flowName + '.' + name, activity['Activities'][j], j])
                Threads.append(t)
                t.start()
            for j in range(len(Threads)):
                Threads[j].join()
        ct1 = str(datetime.datetime.now())
        string = ct1 + ';' + flowName + '.' + name + ' Exit'
        file1.write(str(string + '\n'))


def seq(flowName, activities):
    global no_of_defects
    for i in activities.keys():
        if activities[i]['Type'] == 'Task':
            if activities[i]['Function'] == "TimeFunction":
                boole = True
                if 'Condition' in activities[i]:
                    condition = activities[i]['Condition'][15:20]
                    val = int(activities[i]['Condition'][-1])
                    sign = activities[i]['Condition'][-3]
                    if sign == '>':
                        if no_of_defects[condition] < val:
                            boole = False
                    if sign == '<':
                        if no_of_defects[condition] > val:
                            boole = False
                if boole:
                    ct1 = str(datetime.datetime.now())
                    string = ct1 + ';' + flowName + '.' + i + ' Entry'
                    file1.write(str(string + '\n'))
                    timeWait(flowName, i, activities[i]['Inputs']['ExecutionTime'], activities[i]['Inputs']['FunctionInput'])
                    ct2 = str(datetime.datetime.now())
                    string1 = ct2 + ';' + flowName + '.' + i + ' Exit'
                    file1.write(str(string1 + '\n'))
                else:
                    ct1 = str(datetime.datetime.now())
                    string = ct1 + ';' + flowName + '.' + i + ' Entry'
                    file1.write(str(string + '\n'))
                    ct1 = str(datetime.datetime.now())
                    string = ct1 + ';' + flowName + '.' + i + ' Skipped'
                    file1.write(str(string + '\n'))
                    ct2 = str(datetime.datetime.now())
                    string1 = ct2 + ';' + flowName + '.' + i + ' Exit'
                    file1.write(str(string1 + '\n'))

            elif activities[i]['Function'] == "DataLoad":
                boole = True
                if 'Condition' in activities[i]:
                    condition = activities[i]['Condition'][15:20]
                    val = int(activities[i]['Condition'][-1])
                    sign = activities[i]['Condition'][-3]
                    if sign == '>':
                        if no_of_defects[condition] < val:
                            boole = False
                    if sign == '<':
                        if no_of_defects[condition] > val:
                            boole = False
                if True:
                    if boole:
                        ct1 = str(datetime.datetime.now())
                        string = ct1 + ';' + flowName + '.' + i + ' Entry'
                        file1.write(str(string + '\n'))
                        filename = activities[i]['Inputs']['Filename']
                        string = ct1 + ';' + flowName + '.' + i + ' Executing DataLoad(' + filename + ')'
                        file1.write(str(string + '\n'))
                        with open(filename, 'r', newline='') as file:
                            data = csv.reader(file)
                            d = -1
                            for row in data:
                                d += 1
                        no_of_defects[i] = d
                        file.close()
                        ct1 = str(datetime.datetime.now())
                        string = ct1 + ';' + flowName + '.' + i + ' Exit'
                        file1.write(str(string + '\n'))

        if activities[i]['Type'] == 'Flow':
            ct1 = str(datetime.datetime.now())
            string = ct1 + ';' + flowName + '.' + i + ' Entry'
            file1.write(str(string + '\n'))
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
            file1.write(str(string + '\n'))


with open('Milestone2B.yaml') as f:
    docs1 = OrderedDict(yaml.load(f, Loader=SafeLoader))
f.close()

for k in docs1.keys():
    ct = str(datetime.datetime.now())
    s = ct + ';' + k + ' Entry'
    file1.write(str(s + '\n'))
    if docs1[k]['Type'] == "Flow":
        if docs1[k]['Execution'] == 'Sequential':
            seq(k, docs1[k]['Activities'])
    ct = str(datetime.datetime.now())
    s = ct + ';' + k + ' Exit'
    file1.write(str(s + '\n'))

file1.close()
