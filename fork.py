import multiprocessing
import subprocess
import argparse

parser = argparse.ArgumentParser(description="AFL++ Multi Process")
parser.add_argument('-i', '--input', help='Seed Corpus')
parser.add_argument('-o', '--output', help='Output Dir')
parser.add_argument('-d', '--dictionary', help='Fuzzing Dictionary')
parser.add_argument('-Q', '--qemu', required=False, help='Fuzzin QEMU mode', action='store_true')
parser.add_argument('-L', '--library', required=False, help='Library directory for QEMU mode')
parser.add_argument("FILE")
parser.add_argument ('--flags', nargs="?", help='Flags for target binary', required=False)

cpu_count = multiprocessing.cpu_count()

args = parser.parse_args()

errorout = open("error.txt", "w")

for i in range(cpu_count):
  if (i == 0):
    if(args.qemu):
      subprocess.Popen(["tmux new-window \; send-keys 'QEMU_LD_PREFIX=" + args.library + " afl-fuzz -Q -i " + args.input + " -o " + args.output + " -m none -D -M Master -b " + str(i) + " -- " + args.FILE  + " @@' Enter"], shell=True)
    else:
      subprocess.Popen(["tmux new-window \; send-keys 'afl-fuzz -i " + args.input + " -o " + args.output + " -x " + args.dictionary + " -m none -D -M Master -b " + str(i) + " -s 123 -- " + args.FILE + " " + args.flags + " @@' Enter"], shell=True)
  else:
    slavenum = "slave" + str(i)
    if(args.qemu):
      subprocess.Popen(["tmux new-window \; send-keys 'QEMU_LD_PREFIX=" + args.library + " afl-fuzz -Q -i " + args.input + " -o " + args.output + " -m none -S Slave" + str(i) + " -b " + str(i) + " -- " + args.FILE + " @@' enter"], shell=True)
    else:
      subprocess.Popen(["tmux new-window \; send-keys 'afl-fuzz -i " + args.input + " -o " + args.output + " -x " + args.dictionary + " -m none -s slave" + str(i) + " -b " + str(i) + " -s 12" + str(i) + "  -- " + args.FILE + " " + args.flags + " @@' enter"], shell=True)

