import yaml
import datetime
import time
from yaml.loader import SafeLoader

file1 = open("LogFile.txt", "w")


def timeWait(flowName, taskName, secs):
    ct1 = str(datetime.datetime.now())
    string = ct1 + ';' + flowName + '.' + taskName + ' Executing TimeFunction(' + secs + ')'
    file1.write(string + '\n')
    time.sleep(int(secs))


def seq(flowName, activities):
    for i in activities.keys():
        if activities[i]['Type'] == 'Task':
            if activities[i]['Function'] == "TimeFunction":
                ct1 = str(datetime.datetime.now())
                string = ct1 + ';' + flowName + '.' + i + ' Entry'
                file1.write(string + '\n')
                timeWait(flowName, i, activities[i]['Inputs']['ExecutionTime'])
                ct2 = str(datetime.datetime.now())
                string1 = ct2 + ';' + flowName + '.' + i + ' Exit'
                file1.write(string1 + '\n')

        if activities[i]['Type'] == 'Flow':
            seq(flowName + '.' + i, activities[i]['Activities'])

with open('Milestone1A.yaml') as f:
    docs1 = yaml.load(f, Loader=SafeLoader)
f.close()

with open('Milestone1B.yaml') as f:
    docs2 = yaml.load(f, Loader=SafeLoader)
f.close()

for k in docs1.keys():
    ct = str(datetime.datetime.now())
    s = ct + ';' + k + ' Entry'
    file1.write(s + '\n')
    if docs1[k]['Type'] == "Flow":
        if docs1[k]['Execution'] == 'Sequential':
            seq(k, docs1[k]['Activities'])

