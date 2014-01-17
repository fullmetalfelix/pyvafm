# -*- coding:utf-8 -*-


## \package vafmcircuits_Cantilever
# This file contains the cantilever circuit

import numpy 
import math
from vafmbase import Circuit
import math
import vafmcircuits_Logic
import vafmcircuits_Scanner
from vafmcircuits import Machine

class Cantilever(Circuit):

	def __init__(self, machine, name, **keys):

		super(self.__class__, self).__init__( machine, name )
		
		if 'NumberOfModesV' in keys.keys():
			self.NumberOfModesV = keys['NumberOfModesV']
			print str(self.NumberOfModesV) + " vertical modes found"
		else:
			print ("WARNING: Number of vertical modes not given setting default to 1!")
			self.NumberOfModesV = 1 

		if 'NumberOfModesL' in keys.keys():
			self.NumberOfModesL = keys['NumberOfModesL']
			print str(self.NumberOfModesL) + " lateral modes found"
		else:
			print ("WARNING: Number of lateral modes not given setting default to 1!")
			self.NumberOfModesV = 1 

		self.AddInput("exciterz")
		self.AddInput("excitery")
		self.AddInput("position")
		self.AddInput("Record")

		self.AddInput("ForceV")
		self.AddInput("ForceL")
		
		self.AddOutput("zPos")
		self.AddOutput("yPos")

		self.AddOutput("xABSv")
		self.AddOutput("yABSv")
		self.AddOutput("zABSv")

		self.AddOutput("xABSl")
		self.AddOutput("yABSl")
		self.AddOutput("zABSl")

		for i in range(1 , self.NumberOfModesV+1):
			self.AddOutput("vV" + str(i) )
			self.AddOutput("zV" + str(i) )

		for i in range(1 , self.NumberOfModesL+1):
			self.AddOutput("vL" + str(i) )
			self.AddOutput("zL" + str(i) )