import ini_with_LS as ini
import readData
import travel_time
import Fesibility as Fb
pickup = readData.pickups
delivery = readData.Deliveries
num_pair = readData.num_pair
Cap = readData.capacityVechicle
glo_de = []
def relocate(init_sol,num_pair,cur_best,ini_len):
    global glo_de
    len_ro,cur_sol = len(init_sol),init_sol
    for i in range(1,len_ro-1):
        node_id,no_load = init_sol[i][0],init_sol[i][1]
        #back
        for j in range(i+1,len_ro-1):   # ...i-1 -> i+1 ->......-> j -> i -> j+1
            if node_id <= num_pair and init_sol[j][0] == num_pair+node_id:
                break
            tmp_sol = init_sol[0:i] + init_sol[i + 1:j+1] + init_sol[i:i+1] + init_sol[j+1:]
            #print("aaaa",tmp_sol)
            fes, tra = Fb.check(tmp_sol)
            depa = Fb.depature
            if fes == False:
                continue
            tmpans = (len(tmp_sol) / 2 - 1) * ini.Profit - tra* ini.Spend
            if tmpans > cur_best:
                cur_sol = tmp_sol
                cur_best = tmpans
                ini_len = tra
                glo_de = depa
        #front  0...j->i->j+1...i-1->i+1....

        for j in range(1,i):  # ...j-1,i,j,.....->i-1->i+1->....
            tmp_sol = init_sol[0:j] + init_sol[i:i+1] + init_sol[j:i] + init_sol[i+1:]
            #print("aaaa",tmp_sol)
            fes, tra = Fb.check(tmp_sol)
            depa = Fb.depature
            if fes == False:
                continue
            tmpans = (len(tmp_sol) / 2 - 1) * ini.Profit - tra * ini.Spend
            if tmpans > cur_best:
                cur_sol = tmp_sol
                cur_best = tmpans
                ini_len = tra
                glo_de = depa

    #print("cur_best = ",cur_best,init_sol,ini_len)
    return ini_len,cur_sol,cur_best

#def swap