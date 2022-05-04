import datetime
import os
import re, uuid

# joins elements of getnode() after each 2 digits.
# using regex expression
#print ("The MAC address in formatted and less complex way is : ", end="")
# mac id in raw format print(uuid.getnode())




def data_return():
    macid = (':'.join(re.findall('..', '%012x' % uuid.getnode())))
    current_time = datetime.datetime.now() 
    date = str(current_time.date())
    time = str(current_time.time())
    unit_reading = 0
    data = [ unit_reading , str(macid) , date , time ]
    return data



print(data_return())