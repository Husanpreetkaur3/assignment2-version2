#!/usr/bin/env python3

import subprocess
import sys
import argparse

'''
OPS445 Assignment 2
Program: duim.py
Author: Husanpreet Kaur
The python code in this file (duim.py) is original work written by
Husanpreet Kaur. No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or online resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: 
This script improves upon the `du` command by providing an enhanced 
disk usage report. It lists all subdirectories within a specified 
directory and generates a bar graph to visually represent the 
percentage of disk space occupied by each subdirectory relative to 
the total disk usage of the specified directory. 

The user can customize the bar graph length using a command-line 
argument and toggle between raw bytes or human-readable sizes.

Features:
1. Parses output of `du -d 1` using subprocess.
2. Converts percentages into customizable bar graphs.
3. Displays sizes in raw bytes or human-readable formats.
4. Includes argparse for command-line argument parsing.

Date: [Insert Current Date Here]
'''

def call_du_sub(target_directory):
    """Runs the `du -d 1` command and returns the output as a list."""
    try:
        process = subprocess.Popen(['du', '-d', '1', target_directory], stdout=subprocess.PIPE)
        output = process.communicate()[0].decode('utf-8')
        return output.strip().split('\n')
    except Exception as e:
        print(f"Error: {e}")
        return []


def percent_to_graph(percent, total_chars):
    """Converts percentage to a bar graph string."""
    if not (0 <= percent <= 100):
        raise ValueError("Percent must be between 0 and 100")
    
    # Proper rounding to handle edge cases
    num_equals = round((percent / 100) * total_chars)
    num_spaces = total_chars - num_equals
    
    return '=' * num_equals + ' ' * num_spaces


def create_dir_dict(du_output):
    """Parses the `du` command output into a dictionary."""
    dir_dict = {}
    for line in du_output:
        parts = line.split('\t')
        if len(parts) == 2:
            size = int(parts[0])
            path = parts[1]
            dir_dict[path] = size
    return dir_dict


def parse_command_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="DU Improved -- See Disk Usage Report with Bar Charts"
    )
    parser.add_argument(
        'target', nargs='?', default='.', help="The directory to scan."
    )
    parser.add_argument(
        '-H', '--human-readable', action='store_true', help="Print sizes in human-readable format."
    )
    parser.add_argument(
        '-l', '--length', type=int, default=20, help="Specify the length of the graph. Default is 20."
    )
    return parser.parse_args()


def convert_to_human_readable(size_in_bytes):
    """Converts bytes to human-readable format."""
    units = ['B', 'K', 'M', 'G', 'T']
    for unit in units:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.1f}{unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.1f}P"


def main():
    """Main function to display the disk usage report."""
    args = parse_command_args()
    target_directory = args.target
    total_chars = args.length

    # Get the `du` output
    du_output = call_du_sub(target_directory)
    if not du_output:
        print("No output from du. Check the target directory.")
        return

    # Create a dictionary from `du` output
    dir_dict = create_dir_dict(du_output)
    total_size = sum(dir_dict.values())

    # Print the report
    print(f"Total: {convert_to_human_readable(total_size) if args.human_readable else total_size} bytes  {target_directory}")
    for path, size in dir_dict.items():
        percent = (size / total_size) * 100
        bar = percent_to_graph(percent, total_chars)
        size_str = f"{convert_to_human_readable(size) if args.human_readable else size} bytes"
        print(f"{int(percent):3}% [{bar}] {size_str} {path}")


if __name__ == "__main__":
    main()
