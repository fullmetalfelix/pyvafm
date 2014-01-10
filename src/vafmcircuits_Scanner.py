# -*- coding:utf-8 -*-
import math
from vafmbase import Circuit
import math
import vafmcircuits_Logic
from vafmcircuits import Machine

## \package vafmcircuits_Scanner
# This file contains the Scanning system
# \file vafmcircuits_Scanner.py
# This file contains the Scanning system

## \brief Scanner circuit.
#
# This is the circuit that allows the user to control the cantilever placement.
#
# - \b Initialisation \b parameters:
# 	- \a process = Name of the object which was used to initiate the machine.
#
# - \b Input \b channels: 
# 	- This circuit has no input channels.
#
# - \b Output \b channels:
#        - \a pos: The position of the cantilever.
#        - \a ScanPos: The positon of the cantilever when using the Scan function
#        - \a Record: This is either True or False and works in conjunction with the cantilever output signal, this is used to control when you want the cantilever to output a signal, by default this is set to True
#
# \b Example:
# \code
# machine = Machine(machine=None, name='machine', dt=0.01, pushed=True);
# scan = machine.AddCircuit(type='scanner',name='scann', Process = machine, pushed=True)
# \endcode
#
class scanner(Circuit):

	
	def __init__(self, machine, name, **keys):
			
			super(self.__class__, self).__init__( machine, name )

			if 'Process' in keys.keys():
					self.machine = keys['Process']
			else:
					raise NameError("Missing process input!")

			self.AddOutput("pos")
			self.AddOutput("ScanPos")
			self.AddOutput("Record")
			self.x = 0
			self.y = 0
			self.z = 0

			self.O['Record'].value = True
	
	## Place the cantilever to a position instantly.
	#
	# @param x, y and z is the coordinates to place the cantilever.
	#
	# \b Example:
	# \code{.py}
	# scan = machine.AddCircuit(type='scanner',name='scann', Process = machine, pushed=True)
	# scann.Place(1,2,3)
	# \endcode
	#

	def Place (self,x,y,z):
			self.x = x
			self.y = y
			self.z = z
			print "Cantilever placed at position " +str(x) + " " +str(y)+ " " +str(z)

	## Move the cantilever by a given translation vector at a given speed
	#
	# @param x, y and z is the vector direction the cantilever will move and v is the speed at which it will move at.
	# When v=1 the process will be completed in 1 second regardless of distacne, so by changing this value will determine how fast the cantilever will move for example if you set the speed to 2
	# it will move in 0.5 seconds.
	#
	# \b Example:
	# \code{.py}
	# scan = machine.AddCircuit(type='scanner',name='scann', Process = machine, pushed=True)
	# scann.Move(1,2,3,2)
	# \endcode
	#
	def Move (self,x,y,z,v):
			self.deltax = x
			self.deltay = y
			self.deltaz = z

			self.startingx = self.x
			self.startingy = self.y
			self.startingz = self.z

			self.xsection = self.deltax * v*self.machine.dt
			self.ysection = self.deltay * v*self.machine.dt
			self.zsection = self.deltaz * v*self.machine.dt

			if self.deltax != 0:
					time = int(self.deltax / self.xsection)

			if self.deltay != 0:
					time = int(self.deltay / self.ysection)

			if self.deltaz != 0:
					time = int(self.deltaz / self.zsection)

					
			for i in range( time ):
					self.x = self.x + self.xsection
					self.y = self.y + self.ysection
					self.z = self.z + self.zsection

					if i == time:
							self.x = self.startingx + self.deltax
							self.y = self.startingy + self.deltay
							self.z = self.startingz + self.deltaz

					self.machine.Update()
			print "Cantilever moved to position " +str( self.deltax ) + " " +str(self.deltay)+ " " +str(self.deltaz) +" in " +str(time*self.machine.dt) + " seconds"                



	## Move the cantilever to a new position at a given speed
	#
	# @param x, y and z is the coordiante the cantilever will move to and v is the speed at which it will move at.
	# When v=1 the process will be completed in 1 second regardless of distacne, so by changing this value will determine how fast the cantilever will move for example if you set the speed to 2
	# it will move in 0.5 seconds.
	#
	# \b Example:
	# \code{.py}
	# scan = machine.AddCircuit(type='scanner',name='scann', Process = machine, pushed=True)
	# scann.MoveTo(1,2,3,2)
	# \endcode
	#
	def MoveTo (self,x,y,z,v):

			self.deltax = x - self.x
			self.deltay = y - self.y
			self.deltaz = z - self.z

			self.startingx = self.x
			self.startingy = self.y
			self.startingz = self.z

			self.xsection = self.deltax * v*self.machine.dt
			self.ysection = self.deltay * v*self.machine.dt
			self.zsection = self.deltaz * v*self.machine.dt
			
			if self.deltax != 0:
					time = int(self.deltax / self.xsection)

			if self.deltay != 0:
					time = int(self.deltay / self.ysection)

			if self.deltaz != 0:
					time = int(self.deltaz / self.zsection)

			for i in range( time +1):
					self.x = self.x + self.xsection
					self.y = self.y + self.ysection
					self.z = self.z + self.zsection
					self.machine.Update()

			if i == time:
							self.x = x
							self.y = y
							self.z = z
			print "Cantilever moved to position " +str(x)+ " " +str(y)+ " " +str(z) +" in " +str(time*self.machine.dt) + " seconds"        

	## Causes the cantilever to remain at this current position for a given time
	#
	# @param time, this is how long (in seconds) the cantilever will remain at the given positon
	#
	# \b Example:
	# \code{.py}
	# scan = machine.AddCircuit(type='scanner',name='scann', Process = machine, pushed=True)
	# scann.Wait(10)
	# \endcode
	#
	def Wait (self, time):

			for i in range(int (time/self.machine.dt) +1):
					self.machine.Update()
			print "waited " + str(time) + " seconds"


	## Scans the cantilever along a given distane, in a given direction with a given speed and records points at a given interval.
	#
	# @param x y and z is the direction the cnatilever will move in. 
	#length is the distance the cantilever will travel. 
	#v is the speed, v=1 means the scan will be complete in 1 second, for example if the speed is increased to 2 then the scan will be completed in 0.5 seconds.
	#pts is how many iterations of the loop will be compleed until an output is produced. This is determined by the step size so for example if you wanted a output every 0.5 seconds with a step size
	#of 0.1 then you must set pts = 5 as 5 iterations of the loop will be completed before reaching 0.5 seconds.
	#
	# \b Example:
	# \code{.py}
	# scan = machine.AddCircuit(type='scanner',name='scann', Process = machine, pushed=True)
	# scann.MoveTo(1,2,3,2,)
	# \endcode
	#
	def Scan (self,x,y,z,length,v,pts):
			self.O['Record'].value = False
			
			self.deltax = x * length
			self.deltay = y * length
			self.deltaz = z * length

			counter = 0
			test = 0
			
			self.startingx = self.x
			self.startingy = self.y
			self.startingz = self.z

			self.xsection = self.deltax * v*self.machine.dt
			self.ysection = self.deltay * v*self.machine.dt
			self.zsection = self.deltaz * v*self.machine.dt



			if self.deltax != 0:
					time = int(self.deltax / self.xsection)

			if self.deltay != 0:
					time = int(self.deltay / self.ysection)

			if self.deltaz != 0:
					time = int(self.deltaz / self.zsection)

			for i in range( time +1):

					counter = counter + 1
					self.x = self.x + self.xsection
					self.y = self.y + self.ysection
					self.z = self.z + self.zsection

					#print self.x , self.y , self.z
					if i == time:
							self.x = self.startingx + length *x
							self.y = self.startingy + length *y
							self.z = self.startingz + length *z
					if pts == counter:
							self.O['Record'].value = True
							counter = 0
							
					self.machine.Update()        
			print "Cantilever moved to position " +str(x) +str(y) +str(z) +" in " +str(time*self.machine.dt) + " seconds"        

	def Loop (self, func, time):

			pass


	def Initialize (self):
			
			pass

			
	def Update (self):

			self.O['pos'].value = [self.x, self.y, self.z]

