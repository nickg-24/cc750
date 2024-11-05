def decode(filename):
    values = []
    with open(filename, 'r') as file:
        for i, line in enumerate(file):
            if 1 < i:
                values.append([])
                line = line.split('\t')
                row = i - 2
                for j in range(5):
                    if line[j].isdigit():
                        values[row].append(int(line[j]))
        file.close()

    bin_msg = ""
    i = 0
    while i < len(values):
        row = values[i]
        if len(row) == 0:
            i += 1
            break
        for j in range(len(row)):
            if j == 0:
                bin_msg += format(row[j], f'0{5}b')
            elif j == 1:
                bin_msg += format(row[j], f'0{4}b')
            elif j == 2:
                bin_msg += format(row[j], f'0{4}b')
            elif j == 3:
                bin_msg += format(row[j], f'0{2}b')
            elif j == 4:
                bin_msg += format(row[j], f'0{3}b')
        i += 1

    bin_usr = ""
    while i < len(values):
        row = values[i]
        if len(row) == 0:
            i += 1
            break
        for j in range(len(row)):
            if j == 0:
                bin_usr += format(row[j], f'0{5}b')
            elif j == 1:
                bin_usr += format(row[j], f'0{4}b')
            elif j == 2:
                bin_usr += format(row[j], f'0{4}b')
            elif j == 3:
                bin_usr += format(row[j], f'0{2}b')
            elif j == 4:
                bin_usr += format(row[j], f'0{3}b')
        i += 1

    bin_img_name = ""
    while i < len(values):
        row = values[i]
        if len(row) == 0:
            i += 1
            break
        for j in range(len(row)):
            if j == 0:
                bin_img_name += format(row[j], f'0{5}b')
            elif j == 1:
                bin_img_name += format(row[j], f'0{4}b')
            elif j == 2:
                bin_img_name += format(row[j], f'0{4}b')
            elif j == 3:
                bin_img_name += format(row[j], f'0{2}b')
            elif j == 4:
                bin_img_name += format(row[j], f'0{3}b')
        i += 1

    bin_msg_chars = [bin_msg[i:i+7] for i in range(0, len(bin_msg), 7)]
    int_msg = [int(char, 2) for char in bin_msg_chars]
    msg = "".join(chr(x) for x in int_msg if x > 0)
    print(msg)

    bin_usr_chars = [bin_usr[i:i+7] for i in range(0, len(bin_usr), 7)]
    int_usr = [int(char, 2) for char in bin_usr_chars]
    usr = "".join(chr(x) for x in int_usr if x > 0)
    print(usr)

    bin_img_name_chars = [bin_img_name[i:i+7] for i in range(0, len(bin_img_name), 7)]
    int_img_name = [int(char, 2) for char in bin_img_name_chars]
    img_name = "".join(chr(x) for x in int_img_name if x > 0)
    print(img_name)

    return msg, usr, img_name
