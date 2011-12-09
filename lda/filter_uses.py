#!/usr/bin/env python

tags_file = 'all_tags.txt'
uses_file = 'all_uses.txt'

def main():
    tag_map = {}
    for line in [line.strip() for line in open(tags_file)]:
        tag_map[line] = True
    for line in [line.strip() for line in open(uses_file) if line.split()[-1][1:] in tag_map]:
        print line

if __name__ == '__main__':
    main()
