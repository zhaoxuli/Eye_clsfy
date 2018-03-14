#! /usr/bin/python
# -*- coding:UTF-8 -*-

if __name__ == '__main__':
    file = raw_input()
    with open(file, 'r+') as file_in:
        lines = file_in.readlines()
        file_in.seek(0, 0)
        for line in lines:
            new_line = line.replace('/home/fenghan/Videos', '/home/users/dawei.yang/feng.han')
            file_in.write(new_line)
