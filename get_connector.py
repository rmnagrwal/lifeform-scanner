"""

@author: Raman Agarwal
        Electrical Engineering Student
        Indian Institute of Technology, Delhi
"""


import sys
import platform

def get_connector():
    platform_type1 = platform.system()
    #This to to check wether the system is windows or lunix so that the connector used in specifying file paths can be choosed appropriately.
    if platform_type1 == 'Windows':
        connector1= '\\' #This is the connector used in windows
    elif platform_type1 == 'Linux':
        connector1= '/' #this connector is used in lunix platform

    return connector1