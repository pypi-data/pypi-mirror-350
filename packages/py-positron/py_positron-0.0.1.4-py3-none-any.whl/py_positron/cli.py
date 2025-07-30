#!/usr/bin/env python3
import argparse
import sys
import os
def main():
    parser=argparse.ArgumentParser()
    
    parser.add_argument("command", help="Command to run. Available commands: help, create, start, install, activate, venv", type=str,choices=["help","create","start","install","activate","venv"])
    parser.add_argument("nargs",nargs=argparse.REMAINDER,help="Arguments for the command. Type 'positron <command> -h' for more information on the command.")
    args=parser.parse_args()
    argv=args.nargs
    if args.command=="help":
        parser.print_help()
        exit(0)
    elif args.command=="create":
        from py_positron import create
        #import create
        create.create()
        exit(0)
    elif args.command=="install":
        from py_positron import install
       # import install
        install.install(argv)
        exit(0)
    elif args.command=="start":
        from py_positron import start
        #import start
        start.start(argv)
    # elif args.command=="activate":
    #     #from py_positron import activate
    #     import activate
    #     activate.activate()
    #     exit(0)
    elif args.command=="venv":
        from py_positron import createvenv
        #import createvenv
        createvenv.venv()
        exit(0)
    else:
        print("NotImplemented")
        exit(0)
    
    