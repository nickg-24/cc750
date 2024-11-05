import math


def encode_msg(msg, usr, img_name):

    # Convert each character in the message to its binary representation
    bin_msg = "".join(format(ord(x), f'0{7}b') for x in msg)
    bin_usr = "".join(format(ord(x), f'0{7}b') for x in usr)
    bin_img_name = "".join(format(ord(x), f'0{7}b') for x in img_name)

    while len(bin_msg) % 18 != 0:
        bin_msg += '0'

    while len(bin_usr) % 18 != 0:
        bin_usr += '0'

    while len(bin_img_name) % 18 != 0:
        bin_img_name += '0'

    num_lines = math.ceil(((len(bin_msg) + len(bin_usr) + len(bin_img_name)) / 18)) + 2

    initial_lines = ["# do daily/weekly/monthly maintenance\n",
                     "# min\thour\tday\tmonth\tweekday\tcommand\n"]

    for i in range(num_lines):
        initial_lines.append("*\t*\t*\t*\t*\trun-parts /etc/periodic/job" + str(i) + "\n")

    with open('./getting-started-app/etc/crontabs/root', 'w') as file:
        file.writelines(initial_lines)
        file.close()

    # Encoding bits
    # [5 bits, 4 bits, 4 bits, 2 bits, 3 bits]
    col_1, col_2, col_3, col_4, col_5 = [["" for j in range(num_lines)] for i in range(5)]
    j = 0
    row = 0

    for bit in bin_msg:
        if j == 18:
            j = 0
            row += 1
        if j < 5:
            col_1[row] += bit
            j += 1
        elif 5 <= j < 9:
            col_2[row] += bit
            j += 1
        elif 9 <= j < 13:
            col_3[row] += bit
            j += 1
        elif 13 <= j < 15:
            col_4[row] += bit
            j += 1
        elif 15 <= j < 18:
            col_5[row] += bit
            j += 1

    row += 1
    col_1[row] = "*"; col_2[row] = "*"; col_3[row] = "*"; col_4[row] = "*"; col_5[row] = "*"

    j = 0
    row += 1
    for bit in bin_usr:
        if j == 18:
            j = 0
            row += 1
        if j < 5:
            col_1[row] += bit
            j += 1
        elif 5 <= j < 9:
            col_2[row] += bit
            j += 1
        elif 9 <= j < 13:
            col_3[row] += bit
            j += 1
        elif 13 <= j < 15:
            col_4[row] += bit
            j += 1
        elif 15 <= j < 18:
            col_5[row] += bit
            j += 1

    row += 1
    col_1[row] = "*"; col_2[row] = "*"; col_3[row] = "*"; col_4[row] = "*"; col_5[row] = "*"

    j = 0
    row += 1
    for bit in bin_img_name:
        if j == 18:
            j = 0
            row += 1
        if j < 5:
            col_1[row] += bit
            j += 1
        elif 5 <= j < 9:
            col_2[row] += bit
            j += 1
        elif 9 <= j < 13:
            col_3[row] += bit
            j += 1
        elif 13 <= j < 15:
            col_4[row] += bit
            j += 1
        elif 15 <= j < 18:
            col_5[row] += bit
            j += 1

    columns = [col_1, col_2, col_3, col_4, col_5]

    lines = []
    with open('./getting-started-app/etc/crontabs/root', 'r') as file:
        for i, line in enumerate(file):
            if i > 1:
                line = line.split('\t')
                row = i - 2
                for j in range(5):
                    val = columns[j][row]
                    if val != "" and val != "*":
                        line[j] = str(int(val, 2))
                lines.append("\t".join(line))
            else:
                lines.append(line)
        file.close()

    with open('./getting-started-app/etc/crontabs/root', 'w') as file:
        file.writelines(lines)
        file.close()
