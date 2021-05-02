import sys
import csv
import numpy as np
import statistics
import scipy.stats

def anova(index, norobot_data, video_data, robot_data):
    norobot_mean = norobot_data.mean(axis = 0)[index]
    video_mean = video_data.mean(axis = 0)[index]
    robot_mean = robot_data.mean(axis = 0)[index]

    group_means = [norobot_mean, video_mean, robot_mean]
    total_mean = statistics.mean(group_means)

    norobot_values = norobot_data[:,index]
    video_values = video_data[:,index]
    robot_values = robot_data[:,index]

    SST = 0

    for i in group_means:
        SST += 5 * (i - total_mean)**2

    MST = SST / 2                   # MST = SST / (k - 1)

    norobot_sse = 0

    for value in norobot_values:
        norobot_sse += (value - norobot_mean)**2

    video_sse = 0
    for value in video_values:
        video_sse += (value - video_mean)**2

    robot_sse = 0
    for value in robot_values:
        robot_sse += (value - robot_mean)**2
    
    SSE = norobot_sse + video_sse + robot_sse

    MSE = SSE / (15 - 3)            # MSE = SSE / (n - k)

    F = MST / MSE

    pval = 1-scipy.stats.f.cdf(F, 2, 12)
    # print(F)
    # print("pval",pval)

    ###
    SS = SSE + SST

    ss = 0
    for value in norobot_values:
        ss += (value - total_mean)**2
    for value in video_values:
        ss += (value - total_mean)**2
    for value in robot_values:
        ss += (value - total_mean)**2
    # print(ss, SS)

    ###
    print("index", index)
    print("SST", SST)
    print("SSE", SSE)
    print("MST", MST)
    print("MSE", MSE)
    print("SS", SS)
    print("F", F)
    print("P-value", pval)
    print("\n")
    return



    




def main(args):
    df = args[1]
    datafile = open(df, "r")

    read_csv = csv.reader(datafile, delimiter=",")

    data = []
    for row in read_csv:
        x = list()
        # x.append(row[1])

        if row[1] == "norobot":
            x.append(1)
        elif row[1] == "video":
            x.append(2)
        else:
            x.append(3)
        
        values = [eval(i) for i in row[2:]]


        x += values
        
        x.append(statistics.mean(values))

        data.append(x)

    norobot_data = []
    video_data = []
    robot_data = []

    for trial in data:
        if trial[0] == 1:
            norobot_data.append(trial)
        elif trial[0] == 2:
            video_data.append(trial)
        else:
            robot_data.append(trial)

    norobot_data = np.array(norobot_data)
    video_data = np.array(video_data)
    robot_data = np.array(robot_data)

    

    for i in [1, 2, 3, 4]:
        anova(i, norobot_data, video_data, robot_data)


if __name__ == "__main__":
    main(sys.argv)




'''

H_0 : mean_norobot = mean_video = mean_robot
H_a : not mean_norobot = mean_video = mean_robot

ANOVA Table RESULTS
    time_1:
        Source          dof     SS          MS          F
        Treatments      2       95432.4     47716.2     0.60383     
        Error           12      948262.0    79021.8
        Total           14      1043694.4
        p-value         0.5625096331593546

    
    time_2:
        Source          dof     SS          MS          F
        Treatments      2       17142.5     8571.2      0.16672     
        Error           12      616930.4    51410.9
        Total           14      634072.9
        p-value         0.8483630364091982

    time_3:
        Source          dof     SS          MS          F
        Treatments      2       49522.8     24761.4     0.241145     
        Error           12      1232189.2   102682.4
        Total           14      1281712.0
        p-value         0.7894446486187324

    Average Time:
        Source          dof     SS          MS          F
        Treatments      2       37014.0     18507.0     0.479521     
        Error           12      463136.6    38594.7
        Total           14      500150.6
        p-value         0.6304490558407776
'''
