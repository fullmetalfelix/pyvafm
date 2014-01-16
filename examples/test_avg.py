#!/usr/bin/env python

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_avg
import vafmcircuits_math


def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	
	#Add Circuits
	
	
  	machine.AddCircuit(type='waver',name='osc', amp=1, freq=1, pushed=True )
	machine.AddCircuit(type='avg', name='avg', time=0.5, pushed=True)
	machine.AddCircuit(type='avg', name='avg2', time=0.5, moving=True, pushed=True)
  	
	machine.Connect("osc.sin","avg.signal","avg2.signal")

	out1 = machine.AddCircuit(type='output',name='output',file='test_avg.log', dump=2)
	out1.Register('global.time', 'osc.sin', 'avg.out','avg2.out')
	
	machine.Wait(10)

	

if __name__ == '__main__':
	main()

