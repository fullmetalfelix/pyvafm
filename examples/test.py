#!/usr/bin/env python
import subprocess
import sys
sys.path.append('/Users/johntracey/Desktop/C and Py/src')


from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_Logic
import vafmcircuits_Filters
import vafmcircuits_signal_processing
import vafmcircuits_Scanner



def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	scan = machine.AddCircuit(type='Scanner',name='scann', Process = machine , pushed=True)
	outer= machine.AddCircuit(type='output', name='outer', file='log.dat', dump=1 )
	
	outer.Register('scann.x', 'scann.y','scann.z')
  
	scan.Place(4,5,6)
	scan.Move(1,1,1,1)
	scan.MoveTo(6,7,4,3)
	scan.Scan(5,5,6,1,10)
#	machine.Wait(1.03)

	
if __name__ == '__main__':
	main()
