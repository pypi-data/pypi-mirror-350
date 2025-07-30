#!/usr/bin/env python
#---------------------------------------------------------------------------
# Copyright 2021 Takafumi Ogawa
# Licensed under the Apache License, Version2.0.
#---------------------------------------------------------------------------
# pydecs-common module
#---------------------------------------------------------------------------
import os,sys
import copy
import numpy as np


def product_local(list1_in,list2_in):
    list3_out=[]
    for t1 in list1_in:
        for t2 in list2_in:
            if type(t1)==type([]):
                list3_out.append(t1+[t2])
            else:
                list3_out.append([t1,t2])
    return list3_out


