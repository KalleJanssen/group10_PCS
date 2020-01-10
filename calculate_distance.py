from best_position import *

filename = open("data/output.txt", "r").read().splitlines()

# start and finish time in year month day hour minute second
start = datetime(2019, 10, 2, 12, 0, 0)
finish = datetime(2019, 10, 2, 12, 0, 2)

dicti = cycle_through_time(start, finish, filename)
final_list = list(dicti.values())
for k in final_list:
    copy_list = k
    for i in k:
        copy_list.remove(i)
        for j in copy_list:
            total = np.sqrt((i[0] - j[0])**2 + (i[1] - j[1])**2 + (i[1] - j[1])**2)
            if total < 10 and i != j:
                print(total)
