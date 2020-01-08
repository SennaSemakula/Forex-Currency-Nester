"""
Script to parse JSON as input and output nested dictionaries with arrays as leaves
"""
import os
import sys
import argparse
from argparse import RawTextHelpFormatter
import logging
import json
from collections import OrderedDict
from pprint import pprint


def parse_arguments(arg_list):
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Parses JSON arrays and outputs "
                    "nested dictionaries with leaves as flat dictionaries \n"
                    "Example: \n "
                    "cat <input_json.json> | python nest.py <country> <city>",
        formatter_class=RawTextHelpFormatter)

    # Add the argument options
    parser.add_argument('keys', metavar='N', type=str,
                        nargs='*', help='n keys to be specified')

    parser.parse_args()

    if not arg_list:
        parser.error("No arguments specified. Please enter at least one key")
    return arg_list


def parse_input(user_input):
    """Function to read and process json file"""
    try:
        input_file = json.load(user_input)
    except ValueError as e:
        logging.error("Unable to process %s", e)

    # Handle cases where user attempts
    # to input keys that do not exist in input file
    try:
        for arg in sys.argv[1:]:
            key = [data_dict[arg] for data_dict in input_file]
    except KeyError as e:
        logging.error("Key %s not found in JSON input file. "
                      "Please specify key parameter "
                      "to match input file keys", e)
    else:
        return input_file


def update_dict(json_data, arg_list):
    """Main function to handle creation and update of nested dictionaries"""
    original_dict = OrderedDict()
    args_num = len(arg_list)
    leaf = arg_list[0] if args_num == 1 else arg_list[-1]
    count = 0

    # Create nested dictionaries based on arguments provided
    while count < args_num:
        arg = arg_list[count]
        prev_arg = arg_list[count - 1]

        for key in json_data:
            if arg != leaf:
                if count == 0:
                    original_dict[key[arg]] = {}
                else:
                    traverse_dict(original_dict, key[arg], key[prev_arg])
            else:
                # Create the leaves
                data = {"leaf": key[leaf], "forex_dict": key}
                prop_leaves(original_dict, data, arg_list)
        count += 1

    pprint(json.dumps(original_dict))
    return json.dumps(original_dict)


def traverse_dict(d, required_key, prev_arg):
    """Function to recursively traverse through
       the nested dictionary and update keys"""
    for k, v in d.items():
        if v:
            traverse_dict(v, required_key, prev_arg)
        elif k == prev_arg:
            d[k][required_key] = {}
            break


def prop_leaves(nested_dict, data, arg_list):
    """Function propogates nested dictionary to yield arrays as leaves"""
    key = data['forex_dict']
    leaf = data['leaf']

    leaf_dict = {i: key[i] for i in key if i not in arg_list}

    if len(arg_list) == 1:
        nested_dict[leaf] = []
        nested_dict[leaf].append(leaf_dict)
    else:
        update_leaves(nested_dict, leaf, leaf_dict)

# Could compound this function into traverse_dict but leave leaf logic seperate for now
def update_leaves(d, leaf, leaf_dict):
    """Function to update the leaves of the nested dictionary"""
    if not isinstance(d, list):
        for k, v in d.items():
            if v:
                update_leaves(v, leaf, leaf_dict)
            else:
                d[k][leaf] = []
                d[k][leaf].append(leaf_dict)
                break


def main():
    """ Top-level function """
    args = sys.argv[1:]
    arg_list = parse_arguments(args)
    input_json = parse_input(sys.stdin)

    update_dict(input_json, arg_list)


if __name__ == '__main__':
    sys.exit(main())
