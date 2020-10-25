import readData

speedMatrix = readData.speedMatrix
#print(speedMatrix)
dis = readData.dis
speed = readData.speedprofile

def Tao(i,j,t0):
    #print("TAO : ",i,j,t0)
    t = t0
    c = speedMatrix[i][j]
    break_point = []
    for w in range(4):
        break_point.append( speed[c][w]["breakpoint"][0] )

    break_point.append( speed[c][3]["breakpoint"][1] )
    #print(t0)

    d = dis[i][j]
    #print("ll",i,j,dis[i][j])
    timezone = -1
    for i in range(4):
        if t >= break_point[i] and t < break_point[i + 1]:
            timezone = i
            break

    if timezone == -1:
        return -1
    v = speed[c][timezone]["speed"]
    #print("asd",d,v)
    d,v = float(d),float(v)
    tp = t + d / v

    while tp >= break_point[timezone + 1]:
        d = d - v * (break_point[timezone + 1] - t)
        #print("d = ",d,"v = ",v)
        t = break_point[timezone + 1]
        timezone += 1
        # print(timezone,type(timezone),c,type(c))
        if timezone == 5:
            return -1
        v = speed[c][timezone]["speed"]
        tp = t + d / v
    #print("?????",tp-t0)
    return tp - t0
'''
def Latest(i,j,tj):

    return t0
'''
#Tao(7,17,511)
def rTao(i,j,t0):
    #print("rTAO : ",i,j,t0)
    t = t0
    c = speedMatrix[i][j]
    break_point = []
    for w in range(4):
        break_point.append( speed[c][w]["breakpoint"][0] )

    break_point.append( speed[c][3]["breakpoint"][1] )
    #print( break_point)

    d = dis[i][j]
    #print("ll",i,j,dis[i][j])
    timezone = -1
    #print(break_point)
    for i in range(4):
        if t >= break_point[i] and t < break_point[i + 1]:
            timezone = i
            break
    if timezone == -1:
        return -1
    v = speed[c][timezone]["speed"]
    d,v = float(d),float(v)
    tp = t - d / v
    #print("tp = ",tp)
    while tp < break_point[timezone]:
        d = d - v * (t-break_point[timezone])
        #print("d = ",d,"v = ",v)
        t = break_point[timezone]
        timezone -= 1
        #print("timezone = " ,timezone)
        if timezone == -1:
            return -1
        v = speed[c][timezone]["speed"]
        tp = t - d / v
    #print(t0-tp)

    return t0-tp
#rTao(0,1,123)