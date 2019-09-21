"""
Script to parse JSON as input and output nested dictionary of arrays
"""
import os
import sys
import argparse
import logging
import json
from collections import OrderedDict
#remove this aftter
import json
from pprint import pprint

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Process JSON and output dictionaries")

    # Add the arg options
    parser.add_argument('keys', metavar='N', type=str, nargs='*',
                    help='n keys to be specified')

    args = parser.parse_args()
    return args


def parse_input():
    """Function to read and process json file"""
    input_file = json.load(sys.stdin)
    # Handle cases where user attempts to input keys that do not exist in input file
    try:
        for arg in sys.argv[1:]:
            key = [data_dict[arg] for data_dict in input_file]
    except KeyError as e:
        logging.error("Key %s not found in JSON input file. "
                      " Please specify key parameter to match input file keys", e)
    else:
        return input_file
    

def update_dict(json_data, arg_list):
    """Main function to handle creation and update of dictionary"""
    original_dict = OrderedDict()
    args_num = len(arg_list)
    if args_num == 1:
        leaf = arg_list[0]
    else:
        leaf = arg_list[-1]
    count = 0
    print(args_num)

    while count < args_num:
        arg = arg_list[count]
        prev_arg = arg_list[count - 1]
        # move the following into a different function
        for key in json_data:
            if arg != leaf:
                if count == 0:
                    original_dict[key[arg]] = {}
                else:
                    traverse_dict(original_dict, key[arg], key[prev_arg])
            else:

                leaf_title = key[leaf]
                data = {
                        "curr_arg": arg, "parent": prev_arg, 
                        "leaf_title": leaf_title, "forex_dict": key,
                }
                prop_leaves(original_dict, data, arg_list)
                    
        count += 1

    pprint(json.dumps(original_dict))
    return json.dumps(original_dict)
    #what about duplicate args???


def traverse_dict(d, required_key, prev_arg):
    """Function to recursively traverse through the nested dictionary and update keys"""
    for k, v in d.items():
        if v:
            traverse_dict(v, required_key, prev_arg)
        elif k == prev_arg:
            d[k][required_key] = {}
            break

def init_dict():
    """Should initialise the dictionary that will be used for nesting"""
    pass

def prop_leaves(nested_dict, data, arg_list):
    """Function propogates nested dictionary to yield arrays as leaves"""
    key = data['forex_dict']
    parent = data['parent']
    leaf = data['leaf_title']
    arg = data['curr_arg']
    file_name = os.path.basename(__file__)
    
    leaf_dict = { i: key[i] for i in key if i not in arg_list }
    if len(arg_list) == 1:
        nested_dict[leaf] = []
        nested_dict[leaf].append(leaf_dict)
    else:
        update_leaves(nested_dict, leaf, leaf_dict)

def update_leaves(d, leaf, leaf_dict):
    """Function to update the leaves of the nested dictionary"""
    if not isinstance(d, list):
        for k, v in d.items():
            if v:
                update_leaves(v, leaf, leaf_dict)
            else:
                d[k][leaf] = []
                # leaf dict is not working
                #print(leaf)
                d[k][leaf].append(leaf_dict)
                break

def main():
    """ Top-level function """
    parse_arguments()
    input_json = parse_input()

    #move this away from main function
    args_list = sys.argv[1:]
    update_dict(input_json, args_list)

if __name__ == '__main__':
    sys.exit(main())