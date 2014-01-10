#!/usr/bin/env python
import subprocess
import sys
sys.path.append('./src')

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_Logic
import vafmcircuits_Filters
import vafmcircuits_signal_processing



def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	wave = machine.AddCircuit(type='waver',name='wave', amp=1, freq=1, pushed=True )
	adder= machine.AddCircuit(type='opAdd',name='add', pushed=True)
	test= machine.AddCircuit(type='gain',name='test', pushed=True, gain = 2, Q = 1, fcut = 0.0000001)

	
	outer= machine.AddCircuit(type='output', name='outer', file='log.dat', dump=1 )
	
	outer.Register('global.time', 'test.out', 'wave.sin')

	machine.Connect('wave.sin','test.signal')
	
	machine.Wait(1.03)

	proc = subprocess.Popen(['gnuplot','-p'], 
	                        shell=True,
	                        stdin=subprocess.PIPE,
	                        )	

	proc.stdin.write("plot 'log.dat' using 1:2 title 'test', 'log.dat' using 1:3 title 'input' \n")

if __name__ == '__main__':
	main()
