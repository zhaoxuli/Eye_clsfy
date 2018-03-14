# ! /usr/bin/env python

import os

if __name__ == '__main__':
    new_file = []
    file = raw_input('enter the folders_for_training txt file path: ')
    with open(file, 'r') as input_file:
        for line in input_file.readlines():
            if line.strip().split(os.sep)[-1].find('open') != -1:
                new_line = line.strip() + ' 0'
            elif line.strip().split(os.sep)[-1].find('close') != -1:
                new_line = line.strip() + ' 1'
            else:
                new_line = line.strip()
            new_file.append(new_line)

    dir = os.path.dirname(file)
    file_name = os.path.basename(file)
    file_name = file_name.split('.')[0] + '_plus.txt'
    outfile = open(os.path.join(dir, file_name), 'w')
    for line in new_file:
        outfile.write(str(line) + '\n')
    outfile.close()
