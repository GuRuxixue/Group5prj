import ini_with_LS as ini
import readData

import travel_time
pickup = readData.pickups
delivery = readData.Deliveries
num_pair = readData.num_pair
Cap = readData.capacityVechicle
depature = [1000000 for i in range(2*num_pair+2)]

def feasible(node1,node2): #check time window
    global depature
    if node1 > num_pair:
        t1 = delivery[node1-num_pair]["ltw"]
    else:
        t1 = pickup[node1]["ltw"]
    if node2 > num_pair:
        t2 = delivery[node2-num_pair]["ltw"]
    else:
        t2 = pickup[node2]["ltw"]
    #print("t1,t2 = ",t1,t2,depature[node1],depature[node2])
    if  depature[node1] <= t1  and depature[node2] <= t2:
        return True
    return False

def check(tmp_sol):
    global depature
    depature = [1000000 for i in range(2*num_pair+2)]
    #print("tmp_sol, into feasiblity ",tmp_sol)
    pair = [[0 for _ in range(2)] for _ in range(num_pair + 1)]  # find pickup pos and delivery pos
    for i in range(1, len(tmp_sol)-1):
        no_id = tmp_sol[i][0]
        if no_id > num_pair:
            #print(tmp_sol[i][0] - num_pair)
            pair[tmp_sol[i][0] - num_pair][1] = i
        else:
            pair[tmp_sol[i][0]][0] = i
    #print("check",tmp_sol)
    for i in range(1,num_pair+1):
        if pair[i][0] > pair[i][1]:  #pickup time > delivery time
            return False,-1

    #print(tmp_sol," = ")
    start = pickup[tmp_sol[1][0]]["etw"]
    lastdep,lastnode,curload = start,tmp_sol[1][0],tmp_sol[1][1]
    depature[lastnode] = start
    t1 = travel_time.rTao(0,lastnode,start)
    if t1 != -1: depature[0] = start-t1
    if t1 == -1:
        start = travel_time.Tao(0,tmp_sol[1][0],0)
        if start > pickup[tmp_sol[1][0]]["ltw"]:
            return False,-1
        depature[0] = 0
        lastdep, lastnode, curload = start, tmp_sol[1][0], tmp_sol[1][1]
        depature[lastnode] = start

    for i in range(2,len(tmp_sol)-1):
        #print(tmp_sol[i])
        curnode = tmp_sol[i][0]
        curload += tmp_sol[i][1]
        if curload > Cap:
            return False,-1
        if curnode > num_pair: t = delivery[curnode-num_pair]["etw"]
        else: t = pickup[curnode]["etw"]

        lastdep = max(t, lastdep+travel_time.Tao(lastnode,curnode,lastdep) )
        depature[curnode] = lastdep
        #print("lastdep = ",depature[lastnode],lastnode," --> ", curnode,depature[curnode])
        if feasible(lastnode,curnode) == False:
            return False,-1
        lastnode = curnode

    lastdep += travel_time.Tao(lastnode, tmp_sol[-1][0], lastdep)
    depature[tmp_sol[-1][0]] = lastdep
    #print("asd",lastdep-depature[0])
    return True,lastdep-depature[0]  # duration,