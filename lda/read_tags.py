#!/usr/bin/env python

from sys import stdin

def main():
    for line in stdin:
        tag, count = line.split()
        count = int(count)
        if count >= 5:
            print tag[1:]

if __name__ == '__main__':
    main()
