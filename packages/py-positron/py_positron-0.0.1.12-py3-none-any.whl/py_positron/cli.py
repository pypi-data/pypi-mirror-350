#!/usr/bin/env python3
import argparse
import sys
import os
def main():
    parser=argparse.ArgumentParser()

    parser.add_argument("command", help="Command to run. Available commands: help, create, start, install, pip, activate, venv, update", type=str,choices=["help","create","start","install","activate","venv","pip","update"],default="help",nargs="?")
    parser.add_argument("-v","--version", help="Show the version of PyPositron.", action="store_true")
    parser.add_argument("nargs",nargs=argparse.REMAINDER,help="Arguments for the command. Type 'positron <command> -h' for more information on the command.")
    args=parser.parse_args()
    argv=args.nargs
    if args.version:
        import py_positron
        print("PyPositron version:", py_positron.__version__)
        exit(0)
    if args.command=="help":
        parser.print_help()
        exit(0)
    elif args.command=="create":
        from py_positron import create
        #import create
        create.create()
        exit(0)
    elif args.command=="install" or args.command=="pip":
        from py_positron import install
       # import install
        install.install(argv)
        exit(0)
    elif args.command=="start":
        from py_positron import startproj as start
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
    elif args.command=="update":
        from py_positron import updatecmd as update
        #import update
        update.update(argv)
        exit(0)
    else:
        print("NotImplemented")
        exit(0)
    
    