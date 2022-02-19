# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 14:10:42 2022

@author: Okhrimchuk Roman
for Sierentz Global Merchants


Test task
"""
# TODO Import the necessary libraries

import  re

# TODO Write here is_palindrome function 

def is_palindrome(a):
    my_string = str(a).lower().replace(' ', '')
    my_string = re.sub(r'[^a-z0-9]', '', my_string)
    reverse_string = my_string[::-1]
    return my_string == reverse_string

