#-------------------------------------------------------------------------------
# Name:        core.py
# Purpose:     Reusable graph structures
#
# Author:      O. Rey
#
# Created:     September 2018
# Copyleft:    GNU GPL v3
#-------------------------------------------------------------------------------
import datetime, uuid

from graph import *

class DatetimeTracking(Edge):
    def __init__(self, sourceUUID, targetUUID):
        super().__init__(sourceUUID, targetUUID, "TRACKING", "PREVIOUS", \
                       {"datetime":datetime.datetime.now()})

class EdgePath(Edge):
    """
    Warning, this is an unconventional concept. 
    """
    def __init__(self, e_source, e_target, domain):
        super().__init__(e_source.get_uuid(), e_target.get_uuid(), domain, \
                         "PREVIOUS", {"datetime":datetime.datetime.now()})
        self.e_source = e_source
        self.e_target = e_target
    def __repr__(self):
        return ">>EdgePath||SourceID:" + str(self.source.int) + "|TargetID:" \
               + str(self.target.int) + '||' + super().get_descr() + '|'


def test():
    t1 = DatetimeTracking(uuid.uuid1(),uuid.uuid1())
    print(t1)
    n1 = Node("Meca","Assembly")
    n2 = Node("Meca","Part")
    e1 = Edge(n1.get_uuid(),n2.get_uuid(),"Meca","CONTAINS")
    n3 = Node("Meca","Assembly")
    n4 = Node("Meca","Part")
    e2 = Edge(n3.get_uuid(),n4.get_uuid(),"Meca","CONTAINS")
    t2 = EdgePath(e1, e2, "Meca")
    print(t2)
    print("Please, run the unittests")

if __name__ == "__main__":
    test()
