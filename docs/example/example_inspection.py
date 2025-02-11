#!/usr/bin/env python3
import wat
import math

if __name__ == '__main__':
    caller_info = wat.caller
    # Assuming caller_info contains the necessary information to perform the operation
    # Perform a mathematical operation using the information from wat.caller
    result = math.sqrt(caller_info)  # Example operation, adjust as necessary
    print(result)