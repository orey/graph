#-------------------------------------------------------------------------------
# Name:        gt_clone.py
# Purpose:     Cloning graph transformation
#
# Author:      O. Rey
#
# Created:     September 2018
# Copyleft:    GNU GPL v3
#-------------------------------------------------------------------------------
import copy, uuid
from graph import *

def gt_clone(root, **kwargs):
    def clone_node(root):
        obj = copy.deepcopy(root)
        obj.attributes["uuid"] = uuid.uuid1()
        return obj
    gt_check_params(root, False)
    if type(root) == Node:
        return clone_node(root)
        
    
def main():
    print('Please run the unit tests')


if __name__ == "__main__":
    main()
