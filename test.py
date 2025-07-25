

number = 43261596
array = []
while True:
    if number % 2 == 0:
        array.append(0)
        number = number / 2
    else:
        array.append(1)
        number = (number-1 ) /2

    if number == 0:
        print(array[::-1])
        break

added_sum = 0
looped = 0
while True:

    len_array = len(array)-1

    if array[len_array-looped] == 1:
        added_sum += pow(2, len_array-looped)

    looped += 1
    
    if looped == len(array):
        print(added_sum)
        exit()