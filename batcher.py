"""
Create a bat file with an embedded binary.
Such binary will be extracted at runtime and deleted after the execution.

* Note: This script expect to be run in the same directory of the BAT and binary file. *

Tested on Win7 x86

AUTHOR:
Paolo Montesel

LICENSE:
http://opensource.org/licenses/MIT

CREDITS:
http://stackoverflow.com/a/19596027
"""

import sys
import random

def random_escape_char():
  chars = ";,="
  return chars[random.randint(0, len(chars) - 1)]
  
def create_bat(out_file_name, in_bat_name, in_bin_name):

  in_bin = open(in_bin_name, "rb").read()
  line_start = random_escape_char()
  
  while in_bin.find("\n" + line_start) != -1:
    line_start += random_escape_char()
    
  preamble = ['@echo off\r\n', 'findstr /v "^{0}" "%~f0" >{1}"\r\n'.format(line_start, in_bin_name), '@echo on\r\n']
  epilogue = ['@echo off\r\n', 'del {0}\r\n'.format(in_bin_name), 'exit /b\r\n']
  
  lines = [line_start + line for line in preamble + open(in_bat_name, "r").readlines() + epilogue]

  out   = open(out_file_name, "wb")
  out.writelines(lines)
  out.write(in_bin)

if __name__ == "__main__":
  if len(sys.argv) != 4:
    print "Usage:", sys.argv[0], "<bat file> <bin file> <output file>"
    exit(0)

  in_bat_name  = sys.argv[1]
  in_bin_name  = sys.argv[2]
  out_file_name = sys.argv[3]
  
  print "Creating .BAT file \"{0}\"...".format(out_file_name)
  create_bat(out_file_name, in_bat_name, in_bin_name)
  print "Finished!"
