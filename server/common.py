


#체스용으로 4개로 만듬.
def read_pos(str):
    print(str)
    str = str.split(",")
    list = []
    tup1 = (int(str[0]), int(str[1]))
    tup2 = (int(str[2]), int(str[3]))
    list.append(tup1)
    list.append(tup2)
    return list

# 체스용으로 4개로만든다. 0,1은 움직이기 전 좌표. <- 누구를 옮길지. 2,3 은 움직인 후의 좌표 <- 어디로 옮길지
def make_pos(click_list):
    return str(click_list[0][0]) + "," + str(click_list[0][1]) + "," + str(click_list[1][0]) + "," + str(click_list[1][1])