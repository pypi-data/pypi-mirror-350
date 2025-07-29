#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True

from prelapse import prelapse_main

# from duckduckgo_search.cli import safe_entry_point
# if __name__ == '__main__':
#     sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
#     sys.exit(safe_entry_point())

# prelapse/main.py
# import argparse

# def prelapse_main():
#     parser = argparse.ArgumentParser(description="Description of your program")
#     parser.add_argument('--config', type=str, help='Path to the configuration file')
#     # Add more arguments as needed
#
#     args = parser.parse_args()
#
#     # Your main logic here
#     print(f"Config file path: {args.config}")

if __name__ == "__main__":
    prelapse_main()
