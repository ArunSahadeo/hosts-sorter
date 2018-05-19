#!/usr/bin/env python3 -u

import json, os, subprocess, sys

commented_lines = []

def update_hosts(hosts_file, commented_lines, sorted_lines):
    with open('hosts', 'a+') as f:
        for commented_line in commented_lines:
            f.write(commented_line)
        for sorted_line in sorted_lines:
            if len(sorted_line[0]) < 9:
                f.write('\t%s\t\t\t\t%s\n' % (sorted_line[0], sorted_line[1]))
            elif len(sorted_line[0]) > 9:
                f.write('\t%s\t%s\n' % (sorted_line[0], sorted_line[1]))
            else:
                f.write('\t%s\t\t%s\n' % (sorted_line[0], sorted_line[1]))
    new_hosts_file = os.path.join(os.getcwd(), 'hosts')
    try:
        os.remove(hosts_file)
        print('%s has been deleted.' % (hosts_file))
    except Exception as e:
        print(e)
    try:
        os.rename(new_hosts_file, hosts_file)
        print('Hosts file updated.')
    except Exception as e:
        print(e)

def get_sorted(hosts_file):
    with open(hosts_file, 'r+') as f:
        sorted_lines = []
        lines = f.readlines()
        for line in lines:
            parts = line.split()
            if line.startswith('#'):
                commented_lines.append(line)
                continue
            elif line.isspace():
                continue
            if len(parts) > 1:
                sorted_lines.append(parts)
        unique_lines = []
        for sorted_line in sorted_lines:
            if not any(sorted_line[1] in unique_line for unique_line in unique_lines):
                unique_lines.append(sorted_line)
        sorted_lines = unique_lines
    return sorted(sorted_lines, key=lambda sorted_line: sorted_line[1])

def check_paths(paths_file):
    if not os.path.isfile(paths_file):
        print('%s does not exist in the filesystem' % (paths_file))
        return

    with open(paths_file, 'r') as f:
        paths = json.load(f)
        paths = paths['paths']

        for path in paths:
            if len(path) < 1 or not os.path.isfile(path):
                print('%s does not exist in the filesystem' % (path))
                continue
            return path

def locate_hosts():
    paths_config = None
    if os.name == 'nt':
        paths_config = 'win_paths.json'
        hosts_file = check_paths(paths_config)
    elif os.name == 'posix':
        if os.geteuid() != 0:
            print('You are not running as root!')
            subprocess.call(['sudo', 'python', sys.argv[0]])
        paths_config = 'nix_paths.json'
        check_paths(paths_config)
        hosts_file = check_paths(paths_config)
    return hosts_file

hosts_file = locate_hosts()

if hosts_file is None:
	raise Exception('Cannot find hosts file on system')

sorted_lines = get_sorted(hosts_file)

update_hosts(hosts_file, commented_lines, sorted_lines)
