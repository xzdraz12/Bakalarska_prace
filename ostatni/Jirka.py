import _thread

variable = False



def one(delay):
    global variable
    count = 0
    while count < 5:
        count += 1
        print(count)
        if count == 3:
            variable = True





def two():
    while not variable:
        pass
    print(variable)
    _thread.exit()


two = _thread.start_new_thread(two, ())

print("hallo")
one(2)
#onet = _thread.start_new_thread(one, ( 1,))
