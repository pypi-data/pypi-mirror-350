import argparse
from .core import *

def main():
    parser = argparse.ArgumentParser(
                    prog='calculator',
                    description='Calculator package')
    
    parser.add_argument("operation",choices=['add',"sub","mul","div"])
    parser.add_argument("a", type=float)
    parser.add_argument("b",type=float)

    args=parser.parse_args()

    ops = {
        "add": add,
        "sub": subtract,
        "mul": multiply,
        "div": divide
    }

    result=ops[args.operation](args.a,args.b)

    print(result)
