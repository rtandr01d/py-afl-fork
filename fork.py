import multiprocessing
import subprocess
import argparse

parser = argparse.ArgumentParser(description="AFL++ Multi Process")
parser.add_argument('-i', '--input', help='Seed Corpus')
parser.add_argument('-o', '--output', help='Output Dir')
parser.add_argument("FILE")
parser.add_argument ('--flags', nargs="?", help='Flags for target binary', required=False)

cpu_count = multiprocessing.cpu_count()

args = parser.parse_args()

errorout = open("error.txt", "w")

for i in range(cpu_count):
  if (i == 0):
    subprocess.Popen(["tmux new-window \; send-keys 'afl-fuzz -i " + args.input + " -o " + args.output + " -m none -D -M Master -b " + str(i) + " -s 123 -- " + args.FILE + " " + args.flags + " @@' Enter"], shell=True)
  else:
    slavenum = "slave" + str(i)
    subprocess.Popen(["tmux new-window \; send-keys 'afl-fuzz -i " + args.input + " -o " + args.output + " -m none -S Slave" + str(i) + " -b " + str(i) + " -s 12" + str(i) + "  -- " + args.FILE + " " + args.flags + " @@' Enter"], shell=True)

