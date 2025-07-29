#! /usr/bin/python3

import sys
import time
import re
import os
import getopt
import subprocess

def main(argv):
  result = 'PASS'
  ping_work_list = ''
  ping_block_list = ''
  if len(argv) == 0:
    print('usage: PROG [-h] --ping_work_list <list_of_ip_addresses> --ping_block_list <list_of_ip_addresses>')
    sys.exit(2)
  try:
    opts, args = getopt.getopt(argv,'h',['ping_work_list=','ping_block_list='])
  except getopt.GetoptError:
    print('usage: PROG [-h] --ping_work_list <list_of_ip_addresses> --ping_block_list <list_of_ip_addresses>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('usage: PROG [-h] --ping_work_list <list_of_ip_addresses> --ping_block_list <list_of_ip_addresses>')
      sys.exit()
    elif opt in ('',"--ping_work_list"):
        ping_work_list = arg.split(",")
    elif opt in ('',"--ping_block_list"):
        ping_block_list = arg.split(",")

  i = 0
  num_of_tries = 0
  f = open('/tmp/log.txt','w')

  '''
    Try ping test for each IP that is supposed to work.
    If ping fails, it will re-try up to 3 times.
  '''
  while i < len(ping_work_list):
    cmd = 'ping -c 3 ' + ping_work_list[i]
    f.write(subprocess.getoutput('date')+'  :Trying to execute cmd ...\n')
    output = subprocess.getoutput(cmd)
    f.write(subprocess.getoutput('date')+'  :Successfully executed cmd ...\n')
    m = re.search('3 (packets )?received',output)
    if m:
      i += 1
      num_of_tries = 0
      f.write('###################### Below Test Passes #####################\n')
      f.write('Test Passes for cmd >>>>> '+cmd+'\n')
      f.write('##############################################################\n')
    elif num_of_tries < 3:
      num_of_tries += 1
      f.write('####################### Traffic Failed #######################\n')
      f.write('Executed cmd >>>>> '+cmd+'\n')
      f.write('Number of Tries: '+str(num_of_tries)+'\n')
      f.write(subprocess.getoutput('date')+'  :Will try again. Sleeping now ...\n')
      time.sleep(num_of_tries*3)
    else:
      result = 'FAIL'
      i += 1
      num_of_tries = 0
      f.write('################ Test Failed after 3 re-tries ################\n')
      f.write('Executed cmd >>>>> '+cmd+'\n')
      f.write('Output : \n')
      f.write(output)
      f.write('\n')
      f.write('##############################################################\n')
    f.flush()      

  '''
    Try ping test for each IP that is supposed to be blocked.
  '''
  i = 0
  while i < len(ping_block_list):
    cmd = 'ping -c 3 ' + ping_block_list[i]
    f.write(subprocess.getoutput('date')+'  :Trying to execute cmd ...\n')
    output = subprocess.getoutput(cmd)
    f.write(subprocess.getoutput('date')+'  :Successfully executed cmd ...\n')
    m = re.search('0 received',output)
    if m:
      i += 1
      f.write('###################### Below Test Passes #####################\n')
      f.write('Test Passes for cmd >>>>> '+cmd+'\n')
      f.write('##############################################################\n')
    elif num_of_tries < 3:
      num_of_tries += 1
      f.write('############ Ping should NOT work. Retrying.. ###########\n')
      f.write('Executed cmd >>>>> '+cmd+'\n')
      f.write('Number of Tries: '+str(num_of_tries)+'\n')
      f.write(subprocess.getoutput('date')+'  :Will try again. Sleeping now ...\n')
      time.sleep(num_of_tries*45)
    else:
      result = 'FAIL'
      i += 1
      f.write('########## Below Test Failed (Ping should NOT work) ##########\n')
      f.write('Executed cmd >>>>> '+cmd+'\n')
      f.write('Output : \n')
      f.write(output)
      f.write('\n')
      f.write('##############################################################\n')
    f.flush()
  f.close()

  with open('/tmp/result.txt','w') as result_file:
    result_file.write(result+'\n')

if __name__ == "__main__":
  main(sys.argv[1:])
