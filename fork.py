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

#' '.join(args.flags)


for i in range(cpu_count):
  if (i == 0):
    subprocess.Popen(["afl-fuzz", "-m", "none", "-D", "-i", args.input, "-o", args.output, "-M", "Master", "-b", str(i), "-s", "123", "--", args.FILE, args.flags, "@@"])
    #print("afl-fuzz -m none -D -i " + args.input + " -o " + args.output + "-M Master -b " + str(i) + " -s 123 -- " + args.FILE + " " + args.flags + " @@")
  #else:
    #slavenum = "slave" + str(i)
    #subprocess.Popen(["afl-fuzz", "-m", "none", "-i", args.input, "-o", args.output, "-S", slavenum, "-b", str(i), "--", args.FILE, "@@"])

