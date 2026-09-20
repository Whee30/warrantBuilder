a = "2.0.10"

b = "2.0.2"





def vsplit(x):
    temp_vsplit = x.split('.')
    temp_list = []
    for item in temp_vsplit:
        temp_list.append(item)
    return temp_list


list_a = vsplit(a)
list_b = vsplit(b)

toggle = False

for index, item in enumerate(list_a):
    if int(item) > int(list_b[index]):
        toggle = True
        break



if toggle == True:
    print(f'{a} is more recent than {b}')
else:
    print(f'{a} is not more recent than {b}')