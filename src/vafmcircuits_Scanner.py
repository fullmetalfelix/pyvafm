# -*- coding:utf-8 -*-
import math
from vafmbase import Circuit
import math
import vafmcircuits_Logic
from vafmcircuits import Machine
import ctypes

class Scanner(Circuit):
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )

		self.AddOutput("x")
		self.AddOutput("y")
		self.AddOutput("z")
		self.AddOutput("Record")

		self.machine = machine
		self.cCoreID = Circuit.cCore.Scanner( self.machine.cCoreID )
		self.SetInputs(**keys)


	def Place (self,x,y,z):
		Circuit.cCore.Place( ctypes.c_double(x),ctypes.c_double(y),ctypes.c_double(z) )


	def Idle (self, time):	
		Circuit.cCore.Idle( ctypes.c_double(time) )


	def Move(self,x,y,z,v):
		Circuit.cCore.Move( ctypes.c_double(x),ctypes.c_double(y),ctypes.c_double(z),ctypes.c_double(v) )		

	def MoveTo(self,x,y,z,v):
		Circuit.cCore.MoveTo( ctypes.c_double(x),ctypes.c_double(y),ctypes.c_double(z),ctypes.c_double(v) )	

	def Scan(self,x,y,z,v, points):
		Circuit.cCore.Scan( ctypes.c_double(x),ctypes.c_double(y),ctypes.c_double(z),ctypes.c_double(v),points)	