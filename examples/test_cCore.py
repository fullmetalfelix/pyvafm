#!/usr/bin/env python

import sys
sys.path.append('./src')

from vafmbase import ChannelType
from vafmcircuits import Machine

import vafmcircuits
import vafmcircuits_Logic
import vafmcircuits_Filters



def main():
	
	
	machine = Machine(name='machine', dt=0.01, pushed=True);
	
	wave = machine.AddCircuit(type='waver',name='wave', amp=1, freq=1, pushed=True )
	adder= machine.AddCircuit(type='opAdd',name='add', pushed=True)
	test= machine.AddCircuit(type='SKHP',name='test', pushed=True, gain = 1, Q = 1, fcut = 0.5)

	
	outer= machine.AddCircuit(type='output', name='outer', file='test.dat', dump=1 )
	
	outer.Register('global.time', 'test.out', 'wave.sin')

	machine.Connect('wave.cos','test.signal')
	
	machine.Wait(1.03)

	

if __name__ == '__main__':
	main()
