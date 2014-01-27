#!/usr/bin/env python3
# encoding: utf-8


import fptree as FPT


def fpt(tn):
    """
    returns: None
    pass in: an fptree node
    convenience function for informal, node-by-node introspection
    of the fptree object call unbound to variable
    """
    if tn.node_link:
        print("node_link? {0}".format(tn.node_link.name))
    else:
         print("node_link? none")
    print("name: {0}".format(tn.name))
    print("count: {0}".format(tn.count))
    print("children: {0}".format(list(tn.children.keys())))
    print("parent: {0}".format(tn.parent.name))
    print("\n")