# Get the message from the user
msg = input("Enter the message (Enter 0 to exit): ")

# Convert each character in the message to its binary representation
bin_msg = "".join(format(ord(x), f'0b') for x in msg)

initial_lines = ["# do daily/weekly/monthly maintenance\n",
                 "# min	hour	day	month	weekday	command\n",
                 "*\t*\t*\t*\t*\trun-parts /etc/periodic/15min\n",
                 "*\t*\t*\t*\t*\trun-parts /etc/periodic/hourly\n",
                 "*\t*\t*\t*\t*\trun-parts /etc/periodic/daily\n",
                 "*\t*\t*\t*\t*\trun-parts /etc/periodic/weekly\n",
                 "*\t*\t*\t*\t*\trun-parts /etc/periodic/monthly\n"]

with open('./etc/crontabs/root', 'w') as file:
    file.writelines(initial_lines)
    file.close()

# Encoding bits
# [5 bits, 4 bits, 4 bits, 2 bits, 3 bits]
col_1, col_2, col_3, col_4, col_5 = [["" for j in range(5)] for i in range(5)]
j = 0
row = 0
while len(bin_msg) % 18 != 0:
    bin_msg += '0'

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

columns = [col_1, col_2, col_3, col_4, col_5]

lines = []
with open('./etc/crontabs/root', 'r') as file:
    for i, line in enumerate(file):
        if 1 < i < 7:
            line = line.split('\t')
            row = i - 2
            for j in range(5):
                val = columns[j][row]
                if val != "":
                    line[j] = str(int(val, 2))
            lines.append("\t".join(line))
        else:
            lines.append(line)
    file.close()

with open('./etc/crontabs/root', 'w') as file:
    file.writelines(lines)
    file.close()
