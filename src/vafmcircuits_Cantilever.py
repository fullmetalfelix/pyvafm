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


## \brief Scanner circuit.
#
# This is the circuit that allows calculates the cantilever oscilation, it contains both a vertial and lateral mode and can calculate a user defiend number of modes.
#
# - \b Initialisation \b parameters:\n
# 	- \a NumberOfModesV = Number of vertical modes
#	- \a NumberOfModesL = Number of lateral modes
#	- \a pushed = True|False
#
# - \b Input \b channels: \n
# 	- \a exciterz = The excitation of the vertical motion
# 	- \a excitery = The excitation of the lateral motion
#	- \a record = This allows outputs to be controlled so the cantilever will only output when record = true 
#	- \a ForceV = This is the channel that must be connected to the z output of the interpolation circuit
#	- \a ForceL = This is the channel that must be connected to the y output of the interpolation circuit
# 	- \a position = This is the channel that takes in the position of the cantilever holder and assigns holderx, holdery and holderz which is the acthul position of the cantilever in the forcefield.
#
# - \b Output \b channels:\n
# 	- \a zPos = The z displacment of the cantilever from the starting pos
# 	- \a yPos = The y displacment of the cantilever from the starting pos
#	- \a xABSv = The displacment in the x axis of the vertical mode including the starting positon (starting position + holderx position)
#	- \a yABSv = The displacment in the y axis of the vertical mode including the starting positon (starting position + holdery position + y tip position)
#	- \a zABSv = The displacment in the z axis of the vertical mode including the starting positon (starting position + holdery position + z tip position)
#	- \a xABSl = The displacment in the x axis of the lateral mode including the starting positon (starting position + holderx position)
#	- \a yABSl = The displacment in the y axis of the lateral mode including the starting positon (starting position + holdery position + y tip position)
#	- \a zABSl = The displacment in the z axis of the lateral mode including the starting positon (starting position + holdery position + z tip position)
#
#
#
# \b Example:
# \code
#  	canti = machine.AddCircuit(type='Cantilever', name= 'cantilever', NumberOfModesV=2, NumberOfModesL=0 ,pushed=True)
# \endcode
#

#####################################################################
#vertical mode variables
		self.Qv = []
		self.Kv = []
		self.Wv = []
		self.Fv = []
		self.gammav = []
		self.Mv  = []


		self.vv =  []
		self.av =  []
		self.velocityv = []

		self.xv  = []
		self.yv  = []
		self.zv  = []


#lateral mode variables
		self.Ql = []
		self.Kl = []
		self.Wl = []
		self.Fl = []
		self.gammal = []
		self.Ml  = []

		self.vl =  []
		self.al =  []
		self.velocityl = []
	
		self.xl  = []
		self.yl  = []
		self.zl  = []

#variables used by all



		self.holderx = 0
		self.holdery = 0
		self.holderz = 0

		self.startingx = 0
		self.startingy = 0
		self.startingz = 0



		self.ztip = 0
		self.ztipo = 0

		self.ytip = 0
		self.ytipo = 0

		self.xtip = 0

		self.QvCheck = False
		self.KvCheck = False
		self.FvCheck = False

		self.QlCheck = False
		self.KlCheck = False
		self.FlCheck = False

		self.MasslCheck = False
		self.MassvCheck = False

		self.startposcheck=False
#####################################################################
#Find the Number of Modes
		self.NumberOfModesV = 0
		self.NumberOfModesL = 0

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
#####################################################################

## Assign Q values to the vertical modes
#
# @param *args is list for any number of modes, although one must note that the number of Q's entered must be equal to the NumberOfModesV parameter.
#
# \b Example:
# \code{.py}
#  	canti = machine.AddCircuit(type='Cantilever', name= 'cantilever', NumberOfModesV=2, NumberOfModesL=0 ,pushed=True)	
#  	canti.InputQV(10,10)
# \endcode
#


#Get QV
	def InputQV(self, *args):
		for i in args:
			self.Qv.append(i)
		print " "
		print "found " + str (len(args)) + " vertical Q factors"
		self.QvCheck = True
		if len(args) != self.NumberOfModesV:
			raise NameError("ERROR: Number of Q factors entered does not equal the number of vertical modes entered")

#####################################################################


## Assign K factors to the vertical modes
#
# @param *args is list for any number of modes, although one must note that the number of K's entered must be equal to the NumberOfModesV parameter.
#
# \b Example:
# \code{.py}
#  	canti = machine.AddCircuit(type='Cantilever', name= 'cantilever', NumberOfModesV=2, NumberOfModesL=0 ,pushed=True)	
#  	canti.InputKV(10,10)
# \endcode
#
		
#Get KV
	def InputKV(self, *args):
		for i in args:
			self.Kv.append(i)
		print "found " + str (len(args)) + " vertical K factors"			
		self.KvCheck = True
		if len(args) != self.NumberOfModesV:
			raise NameError("ERROR: Number of K factors entered does not equal the number of vertical modes entered")

#####################################################################

## Assign F (funmental eigenfrequency) to the vertical modes
#
# @param *args is list for any number of modes, although one must note that the number of frequencies entered must be equal to the NumberOfModesV parameter.
#
# \b Example:
# \code{.py}
#  	canti = machine.AddCircuit(type='Cantilever', name= 'cantilever', NumberOfModesV=2, NumberOfModesL=0 ,pushed=True)	
#  	canti.InputFV(10,10)
# \endcode
#

#Get Fv
	def InputFV(self, *args):
		for i in args:
			self.Fv.append(i)
		print "found " + str (len(args)) + " vertical frequencies"		
		self.FvCheck = True	
		if len(args) != self.NumberOfModesV:
			raise NameError("ERROR: Number of Q factors entered does not equal the number of vertical modes entered")
#####################################################################

## Assign Q values to the lateral modes
#
# @param *args is list for any number of modes, although one must note that the number of Q's entered must be equal to the NumberOfModesL parameter.
#
# \b Example:
# \code{.py}
#  	canti = machine.AddCircuit(type='Cantilever', name= 'cantilever', NumberOfModesV=0, NumberOfModesL=2 ,pushed=True)	
#  	canti.InputQL(10,10)
# \endcode
#



#Get Ql


	def InputQL(self, *args):
		for i in args:
			self.Ql.append(i)
		print "found " + str (len(args)) + " lateral Q factors"	
		self.QlCheck = True

		if len(args) != self.NumberOfModesL:
			raise NameError("ERROR: Number of Q factors entered does not equal the number of Lateral modes entered")

#####################################################################

## Assign K factors to the lateral modes
#
# @param *args is list for any number of modes, although one must note that the number of K's entered must be equal to the NumberOfModesL parameter.
#
# \b Example:
# \code{.py}
#  	canti = machine.AddCircuit(type='Cantilever', name= 'cantilever', NumberOfModesV=0, NumberOfModesL=2 ,pushed=True)	
#  	canti.InputKL(10,10)
# \endcode
#

#Get Kl
	def InputKL(self, *args):
		for i in args:
			self.Kl.append(i)
		print "found " + str (len(args)) + " lateral K factors"		
		self.KlCheck = True	

		if len(args) != self.NumberOfModesL:
			raise NameError("ERROR: Number of K factors entered does not equal the number of Lateral modes entered")
#####################################################################
## Assign F (funmental eigenfrequency) to the lateral modes
#
# @param *args is list for any number of modes, although one must note that the number of frequencies entered must be equal to the NumberOfModesL parameter.
#
# \b Example:
# \code{.py}
#  	canti = machine.AddCircuit(type='Cantilever', name= 'cantilever', NumberOfModesV=0, NumberOfModesL=2 ,pushed=True)	
#  	canti.InputFV(10,10)
# \endcode
#

#Get Fl
	def InputFL(self, *args):
		for i in args:
			self.Fl.append(i)
		print "found " + str (len(args)) + " lateral K factors"		
		self.FlCheck = True	

		if len(args) != self.NumberOfModesL:
			raise NameError("ERROR: Number of frequencies entered does not equal the number of Lateral modes entered")

#####################################################################






#####################################################################
## Assign the starting position of the tip
#
# @param x y and z is the coordnates of the starting position
#
# \b Example:
# \code{.py}
#  	canti = machine.AddCircuit(type='Cantilever', name= 'cantilever', NumberOfModesV=2, NumberOfModesL=0 ,pushed=True)	
#  	canti.StartingPos(0,0,2)
# \endcode
#
#Get Starting pos
	def StartingPos(self, x, y ,z):
		self.startingx  = x
		self.startingy  = y
		self.startingz  = z
		print "starting position found as " + str (self.startingx) + "," + str(self.startingy) + "," + str(self.startingz)
		self.startposcheck = True

#####################################################################
## Assign the mass of the cantilever in the vertical modes
#
# @param *args is list for any number of modes, although one must note that the number of masses entered must be equal to the NumberOfModesV parameter.
# If no mass is entered a mass will be calculated using the spring constant and fundemntal frequncy.
#
# \b Example:
# \code{.py}
#  	canti = machine.AddCircuit(type='Cantilever', name= 'cantilever', NumberOfModesV=2, NumberOfModesL=0 ,pushed=True)	
#  	canti.MassV(1,1)
# \endcode
#
#Get MassV

	def MassV(self, *args):
		for i in args:
			self.Mv.append(i)
		self.MassvCheck = True
		if len(args) != self.NumberOfModesV:
			raise NameError("ERROR: Number of masses entered does not equal the number of vertical modes entered")


#####################################################################
## Assign the mass of the cantilever in the lateral modes
#
# @param *args is list for any number of modes, although one must note that the number of masses entered must be equal to the NumberOfModesL parameter.
# If no mass is entered a mass will be calculated using the spring constant and fundemntal frequncy.
#
# \b Example:
# \code{.py}
#  	canti = machine.AddCircuit(type='Cantilever', name= 'cantilever', NumberOfModesV=0, NumberOfModesL=2 ,pushed=True)	
#  	canti.MassL(1,1)
# \endcode
#
#Get Massl
	def MassL(self, *args):
		for i in args:
			self.Ml.append(i)
		self.MasslCheck = True
		if len(args) != self.NumberOfModesL:
			raise NameError("ERROR: Number of masses entered does not equal the number of Lateral modes entered")


#####################################################################


	
	def Initialize (self):
		pass


	def Update (self):

#####################################################################
#vertical modes
		check = self.I['Record'].value 
		if self.machine.time == 0:
			print " "
			for i in range(0 , self.NumberOfModesV):
				self.Wv.append( 2 * math.pi * self.Fv[i]  )
				self.gammav.append( 0.5 * self.Wv[i] / self.Qv[i] )
				if self.MassvCheck == False:
					print "WARNING: No mass given will calculate from omega and k for vertical mode " + str(i+1) + "!"
					self.Mv.append (  self.Kv[i]/ (self.Wv[i] * self.Wv[i])  )

				self.xv.append (self.startingx)
				self.yv.append (self.startingy)
				self.zv.append (self.startingz)

				self.av.append (0)
				self.vv.append (0)

				if self.QvCheck == False:
					raise NameError("ERROR: Missing Q input for the vertical modes")
				if self.KvCheck == False:
					raise NameError("ERROR: Missing K input for the vertical modes")
				if self.FvCheck == False:
					raise NameError("ERROR: Missing F input for the vertical modes")

		self.ztip= 0
		for i in range(0 , self.NumberOfModesV):
			#verlet eqn
			# z + (velocity - friction*velocity) + 0.5 * a * dt^2
			self.zv[i] = self.zv[i] + self.vv[i] * self.machine.dt * ( 1 - self.gammav[i]* self.machine.dt) + 0.5* self.av[i] *self.machine.dt  * self.machine.dt
			# half step velocity update
			#v = velocity - velocity*friction
			self.vv[i] = self.vv[i] * ( 1 - self.gammav[i] * self.machine.dt) + 0.5* self.av[i] *self.machine.dt

			self.ztip = self.ztip + self.zv[i]

			#self.O["z" + str(i)] = self.z[i]

		if check == True:
			self.O["zPos"].value = self.ztip

		self.velocityv = 0.5*(self.ztip - self.ztipo)/self.machine.dt
		self.ztipo = self.ztip


		if check == True:
			#output x + holder pos 
			self.O["xABSv"].value = self.holderx + self.startingx
			#output y + holder pos
			self.O["yABSv"].value = self.holdery + self.startingy + self.ytip
			#output z + holder pos 
			self.O["zABSv"].value = self.holderz + self.startingz + self.ztip


		self.force = self.I["ForceV"].value
		self.totalforce  = (self.force + self.I["exciterz"].value )

		for i in range(0 , self.NumberOfModesV):
			#change in acceleration
			# force / mass                  - z * w ^2 
			self.av[i] = self.totalforce / self.Mv[i] - self.zv[i] * self.Wv[i] * self.Wv[i]
			#self.a = self.a * self.machine.dt


			#update the half velocity
			self.vv[i] = self.vv[i] * ( 1 - self.gammav[i]* self.machine.dt) + 0.5* self.av[i] *self.machine.dt
		
			if check == True:
				self.O["vV"+str(i+1)].value = self.vv[i]
#####################################################################


#####################################################################
#lateral modes
		if self.machine.time == 0:
			print " "
			for i in range(0 , self.NumberOfModesL):
				self.Wl.append( 2 * math.pi * self.Fl[i]  )
				self.gammal.append( 0.5 * self.Wl[i] / self.Ql[i] )
				if self.MasslCheck == False:
					print "WARNING: No mass given will caulcate mass from omega and k for lateral mode " +str(i+1)+ "!"
					self.Ml.append (  self.Kl[i]/ (self.Wl[i] * self.Wl[i])  )

				self.xl.append (self.startingx)
				self.yl.append (self.startingy)
				self.zl.append (self.startingz)

				self.al.append (0)
				self.vl.append (0)

				if self.QlCheck == False:
					raise NameError("ERROR: Missing Q input for the lateral modes")
				if self.KlCheck == False:
					raise NameError("ERROR: Missing K input for the lateral modes")
				if self.FlCheck == False:
					raise NameError("ERROR: Missing F input for the lateral modes")
		if self.machine.time > 0:
			holderx = self.I["position"].value[0]
			holdery = self.I["position"].value[1]
			holderz = self.I["position"].value[2]

		self.ytip= 0
		for i in range(0 , self.NumberOfModesL):
			#verlet eqn
			# z + (velocity - friction*velocity) + 0.5 * a * dt^2
			self.yl[i] = self.yl[i] + self.vl[i] * self.machine.dt * ( 1 - self.gammal[i]* self.machine.dt) + 0.5* self.al[i] *self.machine.dt  * self.machine.dt
			# half step velocity update
			#v = velocity - velocity*friction
			self.vl[i] = self.vl[i] * ( 1 - self.gammal[i] * self.machine.dt) + 0.5* self.al[i] *self.machine.dt

			self.ytip = self.ytip + self.yl[i]

			#self.O["z" + str(i)] = self.z[i]
		if check == True:
			self.O["yPos"].value = self.ytip

		self.velocityl = 0.5*(self.ztip - self.ztipo)/self.machine.dt
		self.ztipo = self.ztip


		if check == True:
			#output x + holder pos 
			self.O["xABSl"].value = self.holderx + self.startingx
			#output y + holder pos
			self.O["yABSl"].value = self.holdery + self.startingy + self.ytip
			#output z + holder pos 
			self.O["zABSl"].value = self.holderz + self.startingz + self.ztip


		self.force = self.I["ForceL"].value
		self.totalforce  = (self.force + self.I["excitery"].value )

		for i in range(0 , self.NumberOfModesL):
			#change in acceleration
			# force / mass                  - z * w ^2 
			self.al[i] = self.totalforce / self.Ml[i] - self.yl[i] * self.Wl[i] * self.Wl[i]
			#self.a = self.a * self.machine.dt


			#update the half velocity
			self.vl[i] = self.vl[i] * ( 1 - self.gammal[i]* self.machine.dt) + 0.5* self.al[i] *self.machine.dt
		
			if check == True:
				self.O["vL"+str(i+1)].value = self.vl[i]
#####################################################################
		
