import argparse
import subprocess
import sys
import os

#from jgtml import jgtapp, mlfcli, ttfcli
#from jgtml.fdb_scanner_2408 import main as fdbscan_main

def run_mlfcli(instrument, timeframe):
    subprocess.run(['mlfcli', '-i', instrument, '-t', timeframe, '--full', '-pn', 'mfi'], check=True)

def run_jgtmlcli(instrument, timeframe):
    subprocess.run(['jgtmlcli', '-i', instrument, '-t', timeframe, '--full', '-pn', 'mfi'], check=True)

def run_fdbscan(instrument, timeframe):
    subprocess.run(['fdbscan', '-i', instrument, '-t', timeframe, '--full'], check=True)

def main():
    parser = argparse.ArgumentParser(description="Run various commands")
    subparsers = parser.add_subparsers(dest='command')

    parser_mlfcli = subparsers.add_parser('mlfcli', help='Run mlfcli')
    parser_mlfcli.add_argument('-i', '--instrument', required=True, help='Instrument')
    parser_mlfcli.add_argument('-t', '--timeframe', required=True, help='Timeframe')

    parser_jgtmlcli = subparsers.add_parser('jgtmlcli', help='Run jgtmlcli')
    parser_jgtmlcli.add_argument('-i', '--instrument', required=True, help='Instrument')
    parser_jgtmlcli.add_argument('-t', '--timeframe', required=True, help='Timeframe')

    parser_fdbscan = subparsers.add_parser('fdbscan', help='Run fdbscan')
    parser_fdbscan.add_argument('-i', '--instrument', required=True, help='Instrument')
    parser_fdbscan.add_argument('-t', '--timeframe', required=True, help='Timeframe')

    parser_help = subparsers.add_parser('help', help='Show help')
    parser_help.add_argument('command', nargs='?', help='Command to show help for')

    parser_interactive = subparsers.add_parser('interactive', help='Run in interactive mode')

    args = parser.parse_args()

    if args.command == 'mlfcli':
        run_mlfcli(args.instrument, args.timeframe)
    elif args.command == 'jgtmlcli':
        run_jgtmlcli(args.instrument, args.timeframe)
    elif args.command == 'fdbscan':
        run_fdbscan(args.instrument, args.timeframe)
    elif args.command == 'help':
        if args.command:
            parser.parse_args([args.command, '--help'])
        else:
            parser.print_help()
    elif args.command == 'interactive':
        interactive_mode()

def interactive_mode():
    while True:
        print("\nInteractive Mode")
        print("1. Run mlfcli")
        print("2. Run jgtmlcli")
        print("3. Run fdbscan")
        print("4. Show help")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            instrument = input("Enter instrument: ")
            timeframe = input("Enter timeframe: ")
            run_mlfcli(instrument, timeframe)
        elif choice == '2':
            instrument = input("Enter instrument: ")
            timeframe = input("Enter timeframe: ")
            run_jgtmlcli(instrument, timeframe)
        elif choice == '3':
            instrument = input("Enter instrument: ")
            timeframe = input("Enter timeframe: ")
            run_fdbscan(instrument, timeframe)
        elif choice == '4':
            command = input("Enter command to show help for: ")
            parser.parse_args([command, '--help'])
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
