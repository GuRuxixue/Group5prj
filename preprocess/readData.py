import math
NumVechicle=0
capacityVechicle=0
Depots=[]
pickups=[]
Deliveries=[]
num_pair = 0
speedprofile = []

'''Depot={
    "idx":"",
   "x":'',
    "y":''
}

pickup=[{
    "idx":"",
    "rk":profit/(cap*etw)
    "x":"",
    "y":"",
    "load":"",
    "profit":"",
    "etw":"",
    "ltw":""
}]
Delivery={
    "idx":"",
    "x":"",
    "y":"",
    "load":"",
    "profit":"",
    "etw":"",
    "ltw":""
}
speedprofile={
    "profile":"",
    "breakpoint":"",
    "speed":""
}'''
speedMatrix=[]
with open('../rawdata/FProb-35A.txt','r',encoding='utf8') as f:
    cont = True
    c=0
    li = []
    flag = 0
    pickups.append(({}))
    Deliveries.append(({}))
    while cont:
        cont = f.readline()
        li.append(cont.split())
        li = [x for x in li if x != []]
        #print(li)
        if cont =='\n' and li!=[]:
            c=c+1
            #print(li)
            #print(li[0])
            if c==1:
                NumVechicle=int(li[0][0])
                capacityVechicle=float(li[1][0])

            elif li[0][0]=="[Node]" or li[0][0] == "[Depot]":
                for i in li[1:]:
                    Depots.append(({
                        "idx": int(i[0]),
                        "x": float(i[1]),
                        "y": float(i[2])
                    }))
                #print("Depots",Depots)
            elif li[0][0] == "[pickup]" or li[0][0] == "[Pickup]":
                for i in li[1:]:
                    #print(i,i[4])
                    num_pair += 1
                    pickups.append(({
                        "rk": float(i[5])/(float(i[4])*(float(i[7]))),
                        "idx": int(i[0]),
                        "x": float(i[1]),
                        "y": float(i[2]),
                        "load": float(i[4]),
                        "profit":float(i[5]),
                        "etw": float(i[6]),
                        "ltw": float(i[7])
                    }))
                #print("pickups",pickups)

            elif li[0][0] == "[delivery]" or li[0][0] == "[Delivery]":
                #print("sdfsdf")
                for i in li[1:]:
                    #print(i)
                    Deliveries.append(({
                        "idx": int(i[0]),
                        "x": float(i[1]),
                        "y": float(i[2]),
                        "load": float(i[4]),
                        "profit":float(i[5]),
                        "etw": float(i[6]),
                        "ltw": float(i[7])
                    }))
                #print("Deliveries", Deliveries)

            elif li[0][0] == "[Speed":
                speed_num = int(li[0][1][:-1])
                #print("kkkkk",speed_num)
                #print("li",li)
                for i in li[1:]:
                    speedprofile.append([])
                    speedprofile[speed_num].append(({
                        "profile": int(speed_num),
                        "breakpoint": [float(i[0]),float(i[1])],
                        "speed": float(i[-1])
                    }))
                #print(speedprofile)

            elif li[0][1] == "choose":
                for i in li[1:]:
                    speedMatrix.append([int(s) for s in i])
            li = []
print("n",num_pair)
dis = [[0 for i in range(3*num_pair)] for j in range(3*num_pair)]
for i in range(1,num_pair+1):
    x1, y1 = pickups[i]["x"], pickups[i]["y"]
    x2,y2 = Depots[0]["x"],Depots[0]["y"]
    dis[0][i] = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)  #depot1 & pickup
    dis[i][0] = dis[0][i]
    for j in range(i+1,num_pair+1):
        x2, y2 = pickups[j]["x"], pickups[j]["y"]   #pickup & delivery
        dis[i][j] = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        dis[j][i] = dis[i][j]

d2 = 2*num_pair+1
for i in range(1,num_pair+1):
    x1, y1 = Deliveries[i]["x"], Deliveries[i]["y"]
    x2,y2 = Depots[1]["x"],Depots[1]["y"]
    dis[d2][i+num_pair] = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2) #depot2 & pickup
    dis[i+num_pair][d2] = dis[d2][i+num_pair]
    for j in range(i+1,num_pair+1):
        x2, y2 = Deliveries[j]["x"], Deliveries[j]["y"]
        dis[i+num_pair][j+num_pair] = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        dis[j+num_pair][i+num_pair] = dis[i+num_pair][j+num_pair]

for i in range(1,num_pair+1):
    for j in range(num_pair+1,d2):
        x1, y1 = Deliveries[j-num_pair]["x"], Deliveries[j-num_pair]["y"]
        x2, y2 = pickups[i]["x"], pickups[i]["y"]
        dis[i][j] = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        dis[j][i] = dis[i][j]
'''
for i in range(0,2*num_pair+2):
    for j in range(0,2*num_pair+2):
        print(dis[i][j],end = " ")
    print("\n")
# print("NumVechicle",NumVechicle,end="\n")
# print("capacity",capacityVechicle,end="\n")
# print("Depots",Depots,end="\n")
# print("pickup",pickups,end="\n")
# print("Delivery",Deliveries,end="\n")
# print("Speed Profile_0",speedprofile_0)
# print("Speed Profile_1",speedprofile_1)
# print("Speed Profile_2",speedprofile_2)
# print("Speed Profile_3",speedprofile_3)
# print("Speed Profile_4",speedprofile_4)
#print(speedprofile[0][0])
#print(pickups[1]["etw"])
'''
