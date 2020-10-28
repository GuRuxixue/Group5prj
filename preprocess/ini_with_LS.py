import numpy as np
import math
import random
import sys
import ALNS_VND
import travel_time
import readData
import time
import Fesibility as Fb
import intra_relocate
import intra_swap
import localsearch
path = sys.argv[0]
pickup = readData.pickups
delivery = readData.Deliveries
num_pair = readData.num_pair
Cap = readData.capacityVechicle
rank = []
inf = float(1<<30)
depature = [1000000 for i in range(num_pair*2+2)]
glo_depa = [1000000 for i in range(2*num_pair+2)]
Vehicle_dep ,Vehicle_end,Profit,ini_len,Spend = 0,0,40,inf,1


def find_place(curpi,curde):
    global ini_len,cur_best
    cur_best = (len(init_sol)/2-1)* Profit - ini_len*Spend
    #print("cur_best = ",cur_best)
    tt = cur_best
    for i in range(0,len(init_sol)-1):
        # insert pi and de as neighbor
        tmp_sol = init_sol[0:i+1] + [[curpi,pickup[curpi]["load"]]] + [[curde,delivery[curde-num_pair]["load"]]] + init_sol[i+1:]
        fes,tra = Fb.check(tmp_sol)

        tmpans =(len(tmp_sol) / 2 - 1) * Profit - tra*Spend
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

            tmpans = (len(tmp_sol) / 2 - 1) * Profit - tra*Spend
            #print("tmpsol is : ", tmp_sol, tmpans)
            if fes == True and tmpans > cur_best:
                cur_sol = tmp_sol
                cur_best = tmpans
                ini_len = tra
    if cur_best == tt:
        return init_sol,tt
    #print("cur_sol = ",cur_sol,ini_len)
    return cur_sol,cur_best

def Insert(curpi,curde):
    global init_sol,ini_len,cur_best,depature
    if len(init_sol) == 1 and pickup[curpi]["load"] <= Cap:   # first pair
        depature[curpi] = pickup[curpi]["etw"]
        depature[curde] = max(delivery[curde-num_pair]["etw"], depature[curpi] + travel_time.Tao(curpi,curde,depature[curpi]))
        if depature[curde] > delivery[curde-num_pair]["ltw"]:
            depature = [inf for _ in range(num_pair * 2 + 2)]
            return
        dt = travel_time.rTao(0,curpi,depature[curpi])
        depature[0] = depature[curpi]-dt
        if dt == -1:
            tt = travel_time.Tao(0,curpi,0)
            if tt > pickup[curpi]["ltw"]:
                depature = [inf for i in range(num_pair * 2 + 2)]
                return
            depature[0] = 0
            #print(".",depature[0])
            depature[curpi],dt = tt,tt
            #print(",",depature[curpi])
            depature[curde] = max(delivery[curde - num_pair]["etw"],
                                  depature[curpi] + travel_time.Tao(curpi, curde, depature[curpi]))
        if depature[curde] <= delivery[curde - num_pair]["ltw"] and dt != -1:
            Vehicle_dep = depature[curpi] - dt
            Vehicle_end = depature[curde] + travel_time.Tao(curde,2*num_pair+1,depature[curde])
            ini_len = ( Vehicle_end - Vehicle_dep)
            init_sol.append([curpi,pickup[curpi]["load"]])
            init_sol.append([curde,delivery[curde-num_pair]["load"]])
            init_sol.append([2*num_pair+1,0])
            return
    else:# ini_sol already have some nodes
        init_sol,cur_best = find_place(curpi,curde)

def Heuris(cur_pro, init_sol,dur):
    # local search -- swap
    global glo_de
    tmp_pro, tmp_sol = cur_pro, init_sol
    dur, init_sol, cur_pro = intra_swap.swap(init_sol, num_pair, cur_pro, dur)
    if cur_pro != tmp_pro:
        glo_de = intra_swap.glo_de
        print("yeah,swap works  ", tmp_sol, '\n', " ----->> ", init_sol, "\n" + "best profit", cur_pro,
              '\n' + "departure time", glo_de)


    # local search -- relocate
    tmp_pro, tmp_sol = cur_pro, init_sol
    dur, init_sol, cur_pro = intra_relocate.relocate(init_sol, num_pair, cur_pro, dur)
    if cur_pro != tmp_pro:
        glo_de = intra_relocate.glo_de
        print("yeah,relocate works  ", tmp_sol, '\n', " ----->> ", init_sol, "\n" + "best profit", cur_pro,
              '\n' + "departure time", glo_de)

    # local search -- sa
    tmp_pro, tmp_sol = cur_pro, init_sol
    dur, cur_pro, init_sol = localsearch.SA(init_sol, num_pair, cur_pro, dur)
    if cur_pro != tmp_pro:
        glo_de = localsearch.glo_de
        print("yeah,sa works  ", tmp_sol, '\n', " ----->> ", init_sol, "\n" + "best profit", cur_pro,
              '\n' + "departure time", glo_de)

    # local search -- ts
    tmp_pro, tmp_sol = cur_pro, init_sol
    dur, cur_pro, init_sol = localsearch.Tabu(init_sol, num_pair, cur_pro, dur)
    if cur_pro != tmp_pro:
        glo_de = localsearch.glo_de
        print("yeah,Tabu works  ", tmp_sol, '\n', " ----->> ", init_sol, "\n" + "best profit",cur_pro,
              '\n' + "departure time", glo_de)
    ck, dur = Fb.check(init_sol)
    cur_pro = (len(init_sol) / 2 - 1) * Profit - dur
    return dur,init_sol,cur_pro

        #ALNS_VND.ALNS(init_sol, len(last_sol), num_pair, last_best,dur)



if __name__=='__main__':

    for m in pickup:
        if m == {}:
            continue
        rank.append((-m["rk"], m["idx"]))
    rank.sort()
    box, map = [], {}
    for i in range(len(rank)):
        for j in range(num_pair - i):
            box.append(rank[i][1])
    # print(len(rank),num_pair,box)
    num_initial =10
    step, cur_longest = 0, 0
    ans_pro = -1000000
    start = time.perf_counter()
    while num_initial > 0:  # generate 10 initial solution

        end = time.perf_counter()
        if end - start > 3 * num_pair:
            print("Time out !!! Stop")
            break
        num, ini_len = 0, 0
        cur_best = 0
        vis = [0 for i in range(num_pair + 1)]
        depature = [inf for i in range(2 * num_pair + 2)]
        # print(vis)
        init_sol = []
        sol_time = {}
        init_sol.append([0, 0])

        while num < num_pair:
            nd = random.choice(box)
            # print("rrr",nd)
            if vis[nd] != 0:
                continue
            num += 1
            vis[nd] = 1
            curpi = nd
            curde = nd + num_pair  # print(curpi,curde)
            Insert(curpi, curde)
            if len(init_sol) == 4:
                glo_dep = depature
            # print(init_sol,'\n',depature)
        # print(init_sol)
        # print(init_sol,'\n', glo_depa)
        ini_s = ""
        for i in range(len(init_sol)):
            ini_s += str(init_sol[i][0]) + " "

        if ini_s in map:
            continue
        with open('sol.txt', 'a') as f:
            for i in init_sol:
                # print(i[0],end = " ")
                f.write(str(i[0]))
                f.write(' ')
            f.write('\n')
        num_initial -= 1
        map[ini_s] = 1
        ck, dur = Fb.check(init_sol)
        pro_best = (len(init_sol) / 2 - 1) * Profit - dur
        #start to opt
        "'init_sol,pro_best"''
        dur, init_sol, pro_best = Heuris(pro_best, init_sol, dur)

        if len(init_sol) > 6:
            init_sol, dur, pro_best = ALNS_VND.ALNS(init_sol, len(init_sol), num_pair, pro_best, dur)
            ck, dur = Fb.check(init_sol)
            pro_best = (len(init_sol) / 2 - 1) * Profit - dur
            de = Fb.depature
        else:
            ck, dur = Fb.check(init_sol)
            pro_best = (len(init_sol) / 2 - 1) * Profit - dur
            de = Fb.depature

        if pro_best > ans_pro:
            last_sol = init_sol
            last_dur = dur
            ans_pro = pro_best
            # print("addddd",depature)
            last_depature = de

        print("numn_inital  = ", num_initial, pro_best)

        # print(cur_longest)
    # print(last_best,last_sol,num_pair,last_depature)
    # ck,dur = Fb.check(init_sol)
    # pro = (len(init_sol) / 2 - 1) * Profit - dur
    # glo_depa = Fb.depature
    # print(last_sol,'\n',Fb.depature)
    print("last_sol",last_sol,'\n','last_duration',last_dur,'\n','final best solution',ans_pro)
    with open('sol_best.txt', 'w') as f:

        f.write(str(str(last_sol)))
        f.write('\n')
        f.write(str(last_depature))
        f.write('\n')
        f.write(str(last_dur))
        f.write('\n')
        f.write(str(ans_pro))
        f.write('\n')


