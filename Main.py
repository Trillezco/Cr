from interface import Interface
import sys

# create interface object
a = Interface()

f = sys.argv[1]

a.extract_qties(f)

# define array of float
# my_array = [1e0, 1e1, 1.23456e4]

# define single float
# my_float = 2e1

# result(:) = array(:) + float
# result = a.do_something(my_array, my_float)

# print result, expected [21.0, 30.0, 12365.6]
# print(result)
