"""
    Script for encoding message into etc/crontabs/root file.

    Filename: encode.py
"""
import math


# Pad the binary strings with 0s to fill the whole cronjob line
def pad_bin_rep(bin_rep):
    while len(bin_rep) % 18 != 0:
        bin_rep += '0'
    return bin_rep


# Initialize the lines of the cronjob file, which will be overwritten
# with the encoded data
def write_initial_lines(num_lines):
    initial_lines = ["# do daily/weekly/monthly maintenance\n",
                     "# min\thour\tday\tmonth\tweekday\tcommand\n"]

    for i in range(num_lines):
        initial_lines.append("*\t*\t*\t*\t*\trun-parts /etc/periodic/job" + str(i) + "\n")

    with open('./getting-started-app/etc/crontabs/root', 'w') as file:
        file.writelines(initial_lines)
        file.close()


# Split the binary strings according to allowed length per column, and assign
# respective values to correct row and column
#
# Allowed bits per column: [5 bits, 4 bits, 4 bits, 2 bits, 3 bits]
def encode_bin_rep(bin_rep, columns, row):
    j = 0

    for bit in bin_rep:
        if j == 18:
            j = 0
            row += 1
        if j < 5:
            columns[0][row] += bit
            j += 1
        elif 5 <= j < 9:
            columns[1][row] += bit
            j += 1
        elif 9 <= j < 13:
            columns[2][row] += bit
            j += 1
        elif 13 <= j < 15:
            columns[3][row] += bit
            j += 1
        elif 15 <= j < 18:
            columns[4][row] += bit
            j += 1

    return columns, row


# Write the filler line of *'s which is used by the decoder
# to differentiate between message, username and next hop
def write_filler_line(columns, row):
    row += 1
    columns[0][row] = "*"
    columns[1][row] = "*"
    columns[2][row] = "*"
    columns[3][row] = "*"
    columns[4][row] = "*"
    row += 1

    return columns, row


# Main function that encodes the message, username and next hop, and
# writes it to the crontabs/root file
def encode_msg(msg, usr, img_name):

    # Convert each character in the message to its binary representation
    bin_msg = "".join(format(ord(x), f'0{7}b') for x in msg)

    # Convert each character in the username to its binary representation
    bin_usr = "".join(format(ord(x), f'0{7}b') for x in usr)

    # Convert each character in the next hop image's name to its binary representation
    bin_img_name = "".join(format(ord(x), f'0{7}b') for x in img_name)

    bin_msg = pad_bin_rep(bin_msg)
    bin_usr = pad_bin_rep(bin_usr)
    bin_img_name = pad_bin_rep(bin_img_name)

    # Based on binary length of all components plus the two filler lines, calculate
    # how many lines the cronjob file will need for encoding
    num_lines = math.ceil(((len(bin_msg) + len(bin_usr) + len(bin_img_name)) / 18)) + 2

    write_initial_lines(num_lines)

    columns = [["" for _ in range(num_lines)] for _ in range(5)]

    row = 0
    columns, row = encode_bin_rep(bin_msg, columns, row)
    columns, row = write_filler_line(columns, row)
    columns, row = encode_bin_rep(bin_usr, columns, row)
    columns, row = write_filler_line(columns, row)
    columns, row = encode_bin_rep(bin_img_name, columns, row)

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
