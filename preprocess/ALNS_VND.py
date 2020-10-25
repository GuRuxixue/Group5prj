import ini_with_LS as ini
import readData
import random
import Fesibility as Fb
import intra_relocate
import intra_swap
import math
import travel_time
from random import sample
import heapq
pickup,delivery,Cap = readData.pickups,readData.Deliveries,readData.capacityVechicle
speedMatrix,dis,speed = readData.speedMatrix,readData.dis,readData.speedprofile
T0=5000 #initial temperature
q=0.95# coefficient of Simulated annealingSimulated annealing
depature = [1000000 for i in range(2*ini.num_pair+2)]
num_destroy,num_repair = 3,3
w_removal,pr_removal = [1 for i in range(num_destroy)],[0 for i in range(num_destroy)]
w_reinsert,pr_reinsert = [1 for i in range(num_repair)],[0 for i in range(num_repair)]
pi_removal,theta_removal = [0 for i in range(num_destroy)],[0 for i in range(num_destroy)]  #last time score & num of select
pi_reinsert,theta_reinsert= [0 for i in range(num_repair)], [0 for i in range(num_repair)]
armax,armin,arRate = 0.25, 1/ini.num_pair, 0.01
gamma,rou1,rou2,rou3 = 0.85,30,8,1   #parameters
Pro,Spend = 40,1
MaxI = 100 #100, ALNS iterator
de =[1000000 for i in range(2*ini.num_pair+2)]
bank = []
def Profit(tmp_sol,dur_tmp):
    tmpans = (len(tmp_sol) / 2 - 1) * Pro - dur_tmp * Spend
    return tmpans

dict_removal = {0:"Random_Rev",1:"dis_Rev",2:"Dur_Rev",3:"CL_Rev"}
def Random_Rev(S,num_removel,num_pair):
    global de
    #print(S,num_pair,num_removel)
    M = []
    for i in range(1,len(S)-1):
        if S[i][0] <= num_pair:
            M.append(S[i])
    k = []
    #print("M, numre",M,num_removel)
    slice = random.sample(M, num_removel)  #random delete num_removal pickup node
    for i in range(len(slice)):
        k.append(slice[i][0])
        k.append(slice[i][0]+num_pair)
    #print("k = ",k,num_pair)
    tmpsol= []
    for i in range(len(S)):
        if S[i][0] in k :
            continue
        tmpsol.append(S[i])
    #print("random   tmpsol  = ",tmpsol,'\n',S,k)
    ck,dur = Fb.check(tmpsol)
    de = Fb.depature
    #print("after removal : ",tmpsol,'\n',de)
    return ck,dur,tmpsol,k
def dur_Rev(S, num_removal, num_pair,dur_S):
    global de
    p = 20 #random parameter ???????
    pos = [-1 for i in range(num_pair+1)]
    Q,k = [],[]
    cost = [-1000000 for i in range(num_pair+1)]
    for i in range(1, len(S) - 1):
        if S[i][0] > num_pair:
            pos[S[i][0]-num_pair] = i

    for i in range(1,len(S)-1):
        if  S[i][0] <= num_pair and len(S)>4:
            j = pos[S[i][0]]
            #print(S[i][0],j)
            tmpsol = S[:i] + S[i+1:j] + S[j+1:]
            ck,dur = Fb.check(tmpsol)
            if ck == True:
                cost[S[i][0]] = dur_S - dur
            else:
                cost[S[i][0]] = dur_S * random.random()*0.2
            Q.append([-cost[S[i][0]],S[i][0]])

    Q.sort()
    while num_removal > 0:
        y = random.random()
        r = int(math.pow(y,p)*len(Q))
        k.append(Q[r][1])
        k.append(Q[r][1]+num_pair)
        Q.pop(r)
        num_removal -= 1
    tmpsol = []
    for i in range(len(S)):
        if S[i][0] in k:
            continue
        tmpsol.append(S[i])
    #print("dur   tmpsol  = ", tmpsol, '\n',S, k)
    ck, dur = Fb.check(tmpsol)
    de = Fb.depature
    #print("tmpsol : ",tmpsol,k)
    return ck, dur, tmpsol, k
def get_dis(sol):
    dis = 0
    for i in range(1,len(sol)):
        dis += readData.dis[sol[i][0]][sol[i-1][0]]
    #dis += readData.dis[sol[-2][0]][2*ini.num_pair+1]
    return dis
def dis_Rev(S, num_removal, num_pair):
    global de
    p = 20  # random parameter ???????
    pos = [-1 for i in range(num_pair + 1)]
    cost = [-1000000 for i in range(num_pair + 1)]
    Q, k = [], []
    dis_S = get_dis(S)

    for i in range(1, len(S) - 1):
        if S[i][0] > num_pair:
            pos[S[i][0]-num_pair] = i

    for i in range(1,len(S)-1):
        if S[i][0] <= num_pair:
            j = pos[S[i][0]]
            #print("pos [",S[i][0]," ]= ",j)
            tmpsol = S[:i] + S[i+1:j] + S[j+1:]
            dis = get_dis(tmpsol)
            #print("s,tmp.dis ",S,'\n',tmpsol,'\n',dis)
            cost[S[i][0]] = dis_S - dis
            Q.append([-cost[S[i][0]], S[i][0]])

    Q.sort()
    while num_removal > 0:
        y = random.random()
        r = int(math.pow(y, p) * len(Q))
        k.append(Q[r][1])
        k.append(Q[r][1] + num_pair)
        num_removal -= 1
        Q.pop(r)
        #print("Q = ",Q)
    tmpsol = []
    for i in range(len(S)):
        if S[i][0] in k:
            continue
        tmpsol.append(S[i])
    ck, dur = Fb.check(tmpsol)
    de = Fb.depature
    return ck, dur, tmpsol, k

dict_reinsert = {0:"Random_Ins",1:"Greedy_Ins",2:"bank_Ins"}
def Random_Ins(tmpsol, num_removal, num_pair,ins_id):
    global de
    pos = random.randint(1,len(tmpsol)-1)  #,,,pos
    #print("random insert position delivery: ", pos + 1, len(tmpsol) - 1)
    tmpsol = tmpsol[:pos]+[[ins_id,pickup[ins_id]["load"]]]+ tmpsol[pos:]

    pod = random.randint(pos+1, len(tmpsol) - 1)
    #print("random insert position pickup: ", pod + 1, len(tmpsol) - 1)
    newsol = tmpsol[:pod] + [[ins_id+num_pair, delivery[ins_id]["load"]]] + tmpsol[pod:]
    ck, dur = Fb.check(newsol)
    de = Fb.depature
    #print("after reinsert:",newsol,'\n',ck)
    return ck, dur, newsol
def Greedy_Ins(tmpsol, num_removal, num_pair,ins_id):
    global de
    cur_best = -1000000
    curpi,curde = ins_id,ins_id+num_pair
    init_sol = tmpsol

    for i in range(0,len(tmpsol)-1):
        # insert pi and de as neighbor
        tmp_sol = init_sol[0:i+1] + [[curpi,pickup[curpi]["load"]]] + [[curde,delivery[curde-num_pair]["load"]]] + init_sol[i+1:]
        fes,tra = Fb.check(tmp_sol)

        tmpans = Profit(tmp_sol,tra)
        #print("tmpsol is : ", tmp_sol, tmpans)
        if fes == True and tmpans > cur_best:
            cur_best = tmpans
            cur_sol = tmp_sol
            ini_len = tra
        for j in range(i+1,len(init_sol)-1):
            #insert pi and de separately
            tmp_sol = init_sol[0:i+1] + [[curpi,pickup[curpi]["load"]]] + init_sol[i+1:j+1]+\
                      [[curde,delivery[curde-num_pair]["load"]]] + init_sol[j+1:]
            fes,tra= Fb.check(tmp_sol)

            tmpans = Profit(tmp_sol,tra)
            #print("tmpsol is : ", tmp_sol, tmpans)
            if fes == True and tmpans > cur_best:
                cur_sol = tmp_sol
                cur_best = tmpans
                ini_len = tra
    if cur_best == -1000000:
        return False,-1000000,tmpsol
    ck,dur = Fb.check(cur_sol)
    de = Fb.depature
    return ck,dur,cur_sol
def bank_Ins(tmpsol,dur_tmp, num_removal, num_pair,ins_id):
    global de
    cur_sol,cur_best = tmpsol,Profit(tmpsol,dur_tmp)
    curpi, curde = ins_id, ins_id + num_pair
    init_sol,ini_len = tmpsol,dur_tmp

    for i in range(0, len(tmpsol) - 1):
        # insert pi and de as neighbor
        tmp_sol = init_sol[0:i + 1] + [[curpi, pickup[curpi]["load"]]] + [
            [curde, delivery[curde - num_pair]["load"]]] + init_sol[i + 1:]
        fes, tra = Fb.check(tmp_sol)
        tmpans = Profit(tmp_sol, tra)
        # print("tmpsol is : ", tmp_sol, tmpans)
        if fes == True and tmpans > cur_best:
            cur_best = tmpans
            cur_sol = tmp_sol
            ini_len = tra
        for j in range(i + 1, len(init_sol) - 1):
            # insert pi and de separately
            tmp_sol = init_sol[0:i + 1] + [[curpi, pickup[curpi]["load"]]] + init_sol[i + 1:j + 1] + \
                      [[curde, delivery[curde - num_pair]["load"]]] + init_sol[j + 1:]
            fes, tra = Fb.check(tmp_sol)

            tmpans = Profit(tmp_sol, tra)
            # print("tmpsol is : ", tmp_sol, tmpans)
            if fes == True and tmpans > cur_best:
                cur_sol = tmp_sol
                cur_best = tmpans
                ini_len = tra
        # print(curpi,curde,'\n',"asd",tmpsol,'\n',cur_sol)
    ck, dur = Fb.check(cur_sol)
    de = Fb.depature
    return ck, dur, cur_sol

#roulette_wheel select reinsert operator reg-k(1,2,3)
def roulette_wheel_reinsert():
    tot_w_reinsert = 0
    for i in range(num_repair):
        w_reinsert[i] = (1 - gamma) * w_reinsert[i] + gamma * pi_reinsert[i] / max(1, theta_reinsert[i])
        tot_w_reinsert += w_reinsert[i]
    for i in range(num_repair):
        pr_reinsert[i] = w_reinsert[i] / max(1e-9,tot_w_reinsert)
    t = random.random()
    for i in range(num_repair):
        if t <= pr_reinsert[i]:
            return i
        else:
            t -= pr_reinsert[i]
    return 0

# roulette_wheel select removal operator
def roulette_wheel_removal():
    tot_w_removal = 0
    for i in range(num_destroy):
        w_removal[i] = (1-gamma)*w_removal[i] + gamma * pi_removal[i]/max(1,theta_removal[i])
        tot_w_removal += w_removal[i]
    for i in range(num_destroy):
        pr_removal[i] = w_removal[i]/max(1e-9,tot_w_removal)
    t = random.random()
    for i in range(num_destroy):
        if t <= pr_removal[i]:
            return i
        else:
            t -= pr_removal[i]
    return 0

def preprocess(tmp_sol,lensol,num_pair):
    start = pickup[tmp_sol[1][0]]["etw"]
    lastdep, lastnode, curload = start, tmp_sol[1][0], tmp_sol[1][1]
    depature[lastnode] = start
    t1 = travel_time.rTao(0, lastnode, start)
    if t1 == -1: #start time at depot < 0
        start = travel_time.Tao(0, tmp_sol[1][0], 0)
        tt = travel_time.Tao(0, lastnode, 0)
        depature[0],depature[lastnode],lastdep = 0,tt,tt

    for i in range(2, lensol - 1):
        curnode = tmp_sol[i][0]
        curload += tmp_sol[i][1]
        if curnode > num_pair:
            t = delivery[curnode - num_pair]["etw"]
        else:
            t = pickup[curnode]["etw"]

        lastdep = max(t, lastdep + travel_time.Tao(lastnode, curnode, lastdep))
        depature[curnode] = lastdep
        lastnode = curnode

    lastdep += travel_time.Tao(lastnode, tmp_sol[-1][0], lastdep)
    depature[tmp_sol[-1][0]] = lastdep
    return

def Distroy_and_Repair(S,num_removal,num_pair,dur_S,Removal_id,Reinsert_id):
    global de,bank
    if Removal_id == 0:
        #print("hey",len(S),num_removal)
        ck, dur_tmp, tmpsol,revlist = Random_Rev(S, num_removal, num_pair)
        #print("revlist")
    elif Removal_id == 1:
        #print("distance removal: ")
        ck, dur_tmp, tmpsol, revlist = dis_Rev(S, num_removal, num_pair)
    elif Removal_id == 2:
        #print("duration removal: ",S)
        ck, dur_tmp, tmpsol, revlist = dur_Rev(S, num_removal, num_pair,dur_S)
    k = []
    for i in range(0, len(revlist), 2):
        k.append(revlist[i])
    random.shuffle(k)
    if Reinsert_id == 0:
        for i in range(len(k)):
            ck, dur_tmp, tmpsol = Random_Ins(tmpsol, num_removal, num_pair, k[i])
        if ck == False:  # random insert can not get a feasible solution, then intra_swap & relocate
            dur_tmp, tmpsol, pro_tmp = intra_swap.swap(tmpsol, num_pair, -1000000, 1000000)  # local search
            if pro_tmp != -1000000:
                de = intra_swap.glo_de
                ck = True
                # print("insert fail, swap work ",tmpsol,'\n',de)
            dur_tmp, tmpsol, pro_tmp = intra_relocate.relocate(tmpsol, num_pair, -1000000, 1000000)
            if pro_tmp != -1000000:
                de = intra_relocate.glo_de
                ck = True
    elif Reinsert_id == 1:
        for i in range(len(k)):
            ck, dur_tmp, tmpsol = Greedy_Ins(tmpsol, num_removal, num_pair, k[i])
            if ck == False:
                #print("sad ", dict_removal[Removal_id],"+", dict_reinsert[Reinsert_id], "not work", '\n', S, '\n', tmpsol)
                dur_tmp, tmpsol,pro_tmp = intra_swap.swap(tmpsol, num_pair, -1000000,1000000)  # local search
                if pro_tmp != -1000000:
                    de = intra_swap.glo_de
                    ck = True
                    #print("insert fail, swap work ",tmpsol,'\n',de)
                dur_tmp, tmpsol,pro_tmp = intra_relocate.relocate(tmpsol, num_pair, -1000000,1000000)
                if pro_tmp != -1000000:
                    de = intra_relocate.glo_de
                    ck = True
                    #print("insert fail, relocte work ", tmpsol, '\n', de)
            #else:
                #print("wow ", dict_removal[Removal_id], "+",dict_reinsert[Reinsert_id], "worksssss", '\n', S, '\n', tmpsol)
    elif Reinsert_id == 2:
        M, bank = [], []
        for i in range(1, len(tmpsol) - 1):
            if tmpsol[i][0] <= num_pair:
                M.append(tmpsol[i][0])
        for i in range(1, num_pair + 1):
            if i not in M:
                bank.append(i)
        for i in range(len(bank)):
            ck, dur_tmp, tmpsol = bank_Ins(tmpsol,dur_tmp, num_removal, num_pair, bank[i])
            #if ck == False:
                #ck, dur_tmp, tmpsol = bank_Ins(S, dur_S, num_removal, num_pair, bank[i])
            if ck == True:
                ck,dur_tmp = Fb.check(tmpsol)
                de = Fb.depature
                #("wow ", dict_removal[Removal_id],"+", dict_reinsert[Reinsert_id], "worksssss", '\n', S, '\n', tmpsol)
            else:
                #print("sad ", dict_removal[Removal_id],"+", dict_reinsert[Reinsert_id], "not work", '\n', S, '\n', tmpsol)
                dur_tmp, tmpsol,pro_tmp = intra_swap.swap(tmpsol, num_pair, -1000000,1000000)  # local search
                if pro_tmp != -1000000:
                    de = intra_swap.glo_de
                    ck = True
                    #print("insert fail, swap work ",tmpsol,'\n',de)

                dur_tmp, tmpsol,pro_tmp = intra_relocate.relocate(tmpsol, num_pair, -1000000,1000000)
                if pro_tmp != -1000000:
                    de = intra_relocate.glo_de
                    ck = True
                    #print("insert fail, relocte work ", tmpsol, '\n', de)
    if ck == False or len(tmpsol)<=4 or len(S)-len(tmpsol)>=0:
        return dur_S,S
    else:
        return dur_tmp,tmpsol

def ALNS(S,lenS,num_pair,S_profit,dur_S): # init_sol,num_pair,cur_best,ini_len
    #print("bank = ",bank)
    print("initial S & dur_S: ", S,'\nduration',dur_S)
    S_best,T,dur_Sbest = S,T0,dur_S
    NonImp,Terminal = 0,0

    while Terminal < MaxI:
        num_removal = max(0,min(int(len(S)/2-2),int(min(armax, armin + arRate * NonImp) * num_pair)))
        Removal_id = roulette_wheel_removal()
        Reinsert_id = roulette_wheel_reinsert()
        #print(Removal_id,dict_removal[Removal_id],Reinsert_id,dict_reinsert[Reinsert_id],'\n',S)
        #print("why wrong? ", len(S),num_removal)
        dur_Snew,S_new = Distroy_and_Repair(S, num_removal,num_pair,dur_S,Removal_id,Reinsert_id) #(S,num_removal,Removal_id,Reinsert_id)
        if len(S_new) <= 2:
            NonImp += 1
            theta_removal[Removal_id] += 5
            theta_reinsert[Reinsert_id] += 5
            Terminal += 1
            continue
        # SA part
        T = T*q
        diff = Profit(S_new,dur_Snew) - Profit(S,dur_S)
        if diff > 0:
            S = S_new
            print("Yes, better than now")
            dur_S = dur_Snew
            pi_removal[Removal_id] += rou2
            pi_reinsert[Reinsert_id] += rou2
        else:
            r = random.random()
            # print(math.exp(-diff/T))
            if math.exp(diff / T) <= r:  #????????????? -diff or diff
                S = S_new
                print("Yes,another chance")
                dur_S = dur_Snew
                pi_removal[Removal_id] += rou3
                pi_reinsert[Reinsert_id] += rou3
        if Profit(S_new,dur_Snew) > Profit(S_best,dur_Sbest):
            NonImp = 0
            print("Yes, the best one ")
            S_best = S_new
            dur_Sbest = dur_Snew
            pi_removal[Removal_id] += rou1
            pi_reinsert[Reinsert_id] += rou1
        else:
            NonImp += 1

        theta_removal[Removal_id] += 5
        theta_reinsert[Reinsert_id] += 5

        Terminal += 1
    return S_best,dur_Sbest,Profit(S_best,dur_Sbest)
#if __name__ == "__main__":
    # execute only if run as a script
    #print("")
