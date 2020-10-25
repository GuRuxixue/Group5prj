import math
import random
import time
import ini_with_LS as ini
from preprocess import travel_time
import Fesibility as Fb
T0=10000 #initial temperature
T_end=10**(-8)
q=0.95# coefficient of Simulated annealingSimulated annealing
L=500 #interation times of each temperature
#init_sol
# [[0, 0], [7, 10.0], [5, 12.0], [15, -12.0], [9, 11.0], [19, -11.0], [17, -10.0], [21, 0]] 0 7 5 15 9 19 17 21  36.55798954052102
glo_de=[]
def SA(init_sol,num_pair,cur_best,ini_len):
    global glo_de
    best_sol = init_sol[:]
    best_pro = cur_best
    N=len(init_sol) # the number of p&d
    if N<=4: #only one request, no need to swap
        return ini_len,cur_best,init_sol
    locList=[0]*(N-2) # position of solution except (depots) for swapping

    def perturbation(locList):
        pickList=random.sample(locList,2)# random selet two position
        idx_1_curr_loc=pickList[0]
        idx_2_curr_loc =pickList[1]
        idx_1=init_sol[pickList[0]][0]
        idx_2=init_sol[pickList[1]][0]
        #print("swap request id",idx_1,idx_2,"loc",idx_1_curr_loc,idx_2_curr_loc)
        if idx_1<=num_pair:
            idx_1_deli_loc=init_sol.index([idx_1+num_pair,-init_sol[pickList[0]][1]])
           # print("idx_1 delivery pos",idx_1_deli_loc)
            if idx_2_curr_loc>=idx_1_deli_loc:
                return -1
        if idx_1>num_pair:
            idx_1_pick_loc=init_sol.index([idx_1-num_pair,-init_sol[pickList[0]][1]])
            #print("idx_1 pickup pos",idx_1_pick_loc)
            if idx_2_curr_loc<=idx_1_pick_loc:
                return -1
        if idx_2 <= num_pair:
            idx_2_deli_loc = init_sol.index([idx_2 + num_pair, -init_sol[pickList[1]][1]])
            #print("idx_2 delivery pos", idx_2_deli_loc)
            if idx_1_curr_loc>=idx_2_deli_loc:
                return -1
        if idx_2 > num_pair:
            idx_2_pick_loc = init_sol.index([idx_2 - num_pair, -init_sol[pickList[1]][1]])
            #print("idx_2 pick pos", idx_2_pick_loc)
            if idx_1_curr_loc<=idx_2_pick_loc:
                return -1
        tmp=init_sol[idx_1_curr_loc]
        init_sol[idx_1_curr_loc]=init_sol[idx_2_curr_loc]
        init_sol[idx_2_curr_loc]=tmp
        #print("after swap temp sol uncheck",init_sol)
        return init_sol

    starttime=time.time()
    count=0
    T=T0
    for i in range(1, N - 1):
        locList[i-1]=i
    # print(locList)
    # perturbation(locList)

    while T>T_end:
        #print(T)
        for i in range(L):
            current_sol = init_sol[:]
            current_profit=cur_best
            init_sol=perturbation(locList)
            depa = Fb.depature
            if init_sol==-1:
                init_sol=current_sol[:]
                continue

            fes, tra=Fb.check(init_sol)
            depa = Fb.depature
            if fes==True:
                temp_profit = (len(init_sol) / 2 - 1) * ini.Profit - tra  * ini.Spend
                cur_best = temp_profit
                if cur_best > best_pro:
                    best_pro = cur_best
                    best_sol = init_sol[:]
                    glo_de = Fb.depature
                    ini_len=tra
                    print("sa solution improved")
                diff=temp_profit-current_profit # calculate difference

                if diff<=0:
                    r= random.random()
                    #print('r',r,math.exp(-diff/T))
                    if math.exp(diff/T)<=r:
                        init_sol = current_sol[:]
                        cur_best=current_profit
            else:
                continue
            #print("currentp",current_profit)

        #print(current_cost)
        T=T*q
        count+=1
    endtime=time.time()
    # print("best route after SA", current_sol)
    # print("cur_best profit",cur_best)
    # print("Running time:",(endtime-starttime),count)
    return ini_len,best_pro,best_sol


def Tabu(init_sol,num_pair,cur_best,ini_len):
    global glo_de
    iteration = 500  #

    N = 2*num_pair+1  # the number of p&d
    if N <= 4:  # only one request, no need to swap
        return -1
    tabu_length = int(N * 0.3)
    tabu_list = [([0] * N) for i in range(N)]
    neighbors = dict()
    p_neighbors=dict()

    def cal_neighbor(init_sol,num_pair):
        global glo_de
        len_ro, cur_sol = len(init_sol), init_sol
        for i in range(1, len_ro - 1):
            for j in range(i + 1, len_ro - 1):  # ...i-1 -> j-> i+1 ->......-> j-1 -> i -> j+1
                tmp_sol = init_sol[0:i] + init_sol[j:j + 1] + init_sol[i + 1:j] + init_sol[i:i + 1] + init_sol[
                                                                                                      j + 1:]
                fes, tra = Fb.check(tmp_sol)
                depa = Fb.depature
                if fes == False:
                    continue
                tmpans = (len(tmp_sol) / 2 - 1) * ini.Profit - tra * ini.Spend
                neighbors[str(init_sol[i][0]) + ',' + str(init_sol[j][0])]=tmpans
                p_neighbors[str(init_sol[i][0]) + ',' + str(init_sol[j][0])]=tmp_sol
        return neighbors,p_neighbors

    neighbors,p_neighbors=cal_neighbor(init_sol,num_pair)
    current_sol = init_sol[:]
    starttime = time.time()

    for k in range(iteration):
        if neighbors=={} and neighbors=={}:
            return ini_len, cur_best, current_sol
        sorted_neighbors = sorted(neighbors.items(), key=lambda item: item[1],reverse=True)
        nid_i = nid_j = 0
        flag = 0
        current_sol = init_sol[:]
        #print("sorted_neighbors",sorted_neighbors)
        #print(neighbors,p_neighbors)
        for neighbor in sorted_neighbors:
            nids = neighbor[0].split(',')
            nid_i = int(nids[0])
            nid_j = int(nids[1])
            #print(neighbor)
            temp_profit=neighbor[1]
            if temp_profit > cur_best:
                current_profit = temp_profit
                cur_best = current_profit
                fes, tra = Fb.check(p_neighbors[neighbor[0]])
                glo_de=Fb.depature
                ini_len = tra

                flag = 1
            else:
                if tabu_list[nid_i][nid_j] != 0:
                    continue
                else:
                    current_profit = temp_profit
            break
        #print(str(nid_i) + ',' + str(nid_j))
        init_sol= p_neighbors[str(nid_i) + ',' + str(nid_j)]
        if flag == 1:
            current_sol = init_sol[:]
            print("tabu find better sol", cur_best,'\n',current_sol)
        # update tabu list
        for i in range(N):
            for j in range(N - i):
                if tabu_list[i][j] != 0:
                    tabu_list[i][j] -= 1
        tabu_list[nid_i][nid_j] += tabu_length
        #update neighbor
        #print("ini",init_sol)
        neighbors,p_neighbors=cal_neighbor(init_sol, num_pair)

    endtime = time.time()
    # print("best route after TS",current_sol)
    # print("currest best profit",cur_best)
    # print("Running time:", (endtime - starttime), iteration)
    return ini_len,cur_best, current_sol





