values = [[] for i in range(5)]
with open('./etc/crontabs/root', 'r') as file:
    for i, line in enumerate(file):
        if 1 < i < 7:
            line = line.split('\t')
            row = i - 2
            for j in range(5):
                if line[j].isdigit():
                    values[row].append(int(line[j]))
    file.close()

bin_msg = ""
for row in values:
    for i in range(len(row)):
        if i == 0:
            bin_msg += format(row[i], f'0{5}b')
        elif i == 1:
            bin_msg += format(row[i], f'0{4}b')
        elif i == 2:
            bin_msg += format(row[i], f'0{4}b')
        elif i == 3:
            bin_msg += format(row[i], f'0{2}b')
        elif i == 4:
            bin_msg += format(row[i], f'0{3}b')

bin_chars = [bin_msg[i:i+7] for i in range(0, len(bin_msg), 7)]
int_msg = [int(char, 2) for char in bin_chars]
msg = "".join(chr(x) for x in int_msg if x > 0)
print(msg)
