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



def ttest(index, norobot_data, video_data, robot_data):
    norobot_mean = norobot_data.mean(axis = 0)[index]
    video_mean = video_data.mean(axis = 0)[index]
    robot_mean = robot_data.mean(axis = 0)[index]

    norobot_std = norobot_data.std(axis = 0)[index]
    video_std = video_data.std(axis = 0)[index]
    robot_std = robot_data.std(axis = 0)[index]

    mean_0 = 0          # mean under the null - no improvement
    
    norobot_t = norobot_mean/(norobot_std / (15)**0.5)
    video_t = video_mean/(video_std / (15)**0.5)
    robot_t = robot_mean/(robot_std / (15)**0.5)

    

    norobot_pval = 1 - scipy.stats.t.cdf(norobot_t, 14)
    video_pval = 1 - scipy.stats.t.cdf(video_t, 14)
    robot_pval = 1 - scipy.stats.t.cdf(robot_t, 14)

    print("Index", index)
    print("Mean - no robot", norobot_mean)
    print("T value - no robot", norobot_t)
    print("P-value - no robot", norobot_pval)

    print("Mean - video", video_mean)
    print("T value - video", video_t)
    print("P-value - video", video_pval)

    print("Mean - robot", robot_mean)
    print("T value - robot", robot_t)
    print("P-value - robot", robot_pval)

    print("\n")






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

        x.append(values[0] - values[1])
        x.append(values[1] - values[2])
        x.append(values[0] - values[2])

        data.append(x)

    norobot_data = []
    video_data = []
    robot_data = []
    # print(data)

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

    

    # for i in [5, 6, 7]:
    #     anova(i, norobot_data, video_data, robot_data)

    for i in [5, 6, 7]:
        ttest(i, norobot_data, video_data, robot_data)


if __name__ == "__main__":
    main(sys.argv)




'''

H_0 : mean_norobot = mean_video = mean_robot
H_a : not mean_norobot = mean_video = mean_robot

alpha = 0.05
qf(0.95, 2, 12) = 3.885294
Rejection Region: {F > 3.885294}

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
    
    Improvement from time_1 to time_2
        Source          dof     SS          MS          F
        Treatments      2       99302.9     49651.5     1.1005396     
        Error           12      541386.8    45115.6
        Total           14      640689.7
        p-value         0.36404861871620386

    Improvement from time_2 to time_3
        Source          dof     SS          MS          F
        Treatments      2       34797.7     17398.9     0.1037937     
        Error           12      2011551.2   167629.2
        Total           14      2046348.9
        p-value         0.9022116073486796

    Improvement from time_1 to time_3
        Source          dof     SS          MS          F
        Treatments      2       19066.8     9533.4     0.068463    
        Error           12      1670977.6   139248.1
        Total           14      1690044.4
        p-value         0.9341897168496459
'''

'''
H_0: mean improvement = 0
H_a: mean improvement > 0



Improvement between time_1 and time_2
Mean - no robot 262.2
T value - no robot 5.581827247691283
P-value - no robot 3.380587255563672e-05
Mean - video 63.8
T value - video 0.9839638259926194
P-value - video 0.17091676826650537
Mean - robot 146.6
T value - robot 5.158170177143269
P-value - robot 7.265008933243777e-05


Improvement between time_2 and time_3
Mean - no robot -89.2
T value - no robot -0.9274569021697335
P-value - no robot 0.815298302242971
Mean - video 23.4
T value - video 0.2024783964679772
P-value - video 0.4212278577733659
Mean - robot -2.4
T value - robot -0.036968008327296194
P-value - robot 0.5144837641036524


Improvement from time_1 to time_3
Mean - no robot 173.0
T value - no robot 2.5331918015827544
P-value - no robot 0.011941444190466166
Mean - video 87.2
T value - video 0.779810428227249
P-value - video 0.22424287864651182
Mean - robot 144.2
T value - robot 2.0169198592088846
P-value - robot 0.03165118966953784
'''