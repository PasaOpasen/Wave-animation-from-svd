# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 00:41:46 2020

@author: qtckp

https://www.pharmacoengineering.com/2018/11/29/converting-matlab-code-to-python/
"""

%matplotlib inline
from oct2py import octave
from oct2py import Oct2Py
import numpy as np



oc = Oct2Py()


y = oc.eval("[1 2 3];")
y











