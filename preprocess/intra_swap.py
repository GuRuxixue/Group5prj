import ini_with_LS as ini
import readData
import Fesibility as Fb
import travel_time
pickup = readData.pickups
delivery = readData.Deliveries
num_pair = readData.num_pair
Cap = readData.capacityVechicle
glo_de = []
def swap(init_sol,num_pair,cur_best,ini_len):
    global glo_de
    len_ro,cur_sol = len(init_sol),init_sol
    for i in range(1,len_ro-1):
        # node_id,no_load = init_sol[i][0],init_sol[i][1]
        # if node_id <= num_pair:
        for j in range(i+1,len_ro-1):   # ...i-1 -> j-> i+1 ->......-> j-1 -> i -> j+1
            tmp_sol = init_sol[0:i] + init_sol[j:j+1]  +init_sol[i + 1:j] + init_sol[i:i+1] + init_sol[j+1:]
            #print(init_sol,"aaaa",tmp_sol)
            fes, tra= Fb.check(tmp_sol)
            depa = Fb.depature
            if fes == False:
                continue

            tmpans = (len(tmp_sol) / 2 - 1) * ini.Profit - tra* ini.Spend
            #print("??",tra,tmp_sol,tmpans)
            if tmpans > cur_best:
                cur_sol = tmp_sol
                cur_best = tmpans
                ini_len = tra
                glo_de = Fb.depature
    # print("?",cur_best)
    return ini_len,cur_sol,cur_best

#def swap