import multiprocessing
import subprocess
import argparse

parser = argparse.ArgumentParser(description="AFL++ Multi Process")
parser.add_argument('-i', '--input', help='Seed Corpus')
parser.add_argument('-o', '--output', help='Output Dir')
parser.add_argument("FILE")

cpu_count = multiprocessing.cpu_count()

args = parser.parse_args()

for i in range(cpu_count):
  if (i == 0):
    subprocess.run(['afl-fuzz', '-i', args.input, '-o', args.output, '-s', '123', '--', args.FILE, '@@'], shell=True, check=True)
  else:
    print("Slave" + str(i))
