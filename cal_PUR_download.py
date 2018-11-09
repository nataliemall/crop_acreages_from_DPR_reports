# cal_PUR_download.py 



import subprocess
import shlex
import pdb 


year = '1999'

filename = 'pur' + str(year)
subprocess.call(shlex.split('./test_script.sh year filename'))
pdb.set_trace()



subprocess.call(shlex.split('./cal_PUR_download.sh year'))


pdb.set_trace()