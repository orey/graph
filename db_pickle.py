#-------------------------------------------------------------------------------
# Name:        db_pickle.py
# Purpose:     Pickle storage for graph structure
#
# Author:      O. Rey
#
# Created:     September 2018
# Copyleft:    GNU GPL v3
#-------------------------------------------------------------------------------
import traceback, sys, pickle

ERR = [ "PickleDb can only be created with a valid filename" ]
DEFAULT_NAME = "default.pdb"

class PickleDb():
    '''
    Storage for graphs using pickle
    '''
    def __init__(self, filename):
        if type(filename) != str:
            raise TypeError(ERR[0])
        if filename == "":
            self.filename = DEFAULT_NAME
        else:
            self.filename = filename
    def append(self, obj):
        myfile = None
        try:
            myfile = open(self.filename, 'ab') # append/binary
            pickle.dump(obj, myfile)
            myfile.close()
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print("== Exception caught:", type(e), e.args)
            myfile.close()
            exit(0)
    def dump(self, obj):
        myfile = None
        try:
            myfile = open(self.filename, 'wb') # write replace/binary
            pickle.dump(obj, myfile)
            myfile.close()
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print("== Exception caught:", type(e), e.args)
            myfile.close()
            exit(0)
    def read_items(self):
        myfile = open(self.filename, 'rb') # read/binary
        objects = []
        count = 0
        try:
            while True:
                objects.append(pickle.load(myfile))
                count += 1
        except EOFError:
            print("Info: end of file reached. Found ", count, "items")
        except:
            traceback.print_exc(file=sys.stdout)
            myfile.close()
            exit(0)
        myfile.close()
        return objects
        
