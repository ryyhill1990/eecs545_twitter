#!/usr/bin/env python

from os import system
import twitter_lib

schema_file = 'schema.sql'
database_file = 'database.db'
command_delimiter = ';'
command_template = 'sqlite3 {0} \'{1}\''
touch_command = 'touch'

def main():
    system(' '.join((touch_command, database_file)))
    for command in ' '.join(line.strip() for line in open(schema_file)).split(command_delimiter):
        system(command_template.format(database_file, command))

if __name__ == '__main__':
    main()
