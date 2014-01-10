# -*- coding:utf-8 -*-
## \package vafmcircuits_Interpolation
# This file contains the interpolation for the force field.
# \file vafmcircuits_Interpolation.py
# This file contains the interpolation for the force field.

import numpy
import math
from vafmbase import Circuit
import math
import vafmcircuits_Logic
from vafmcircuits import Machine
from scipy.interpolate import LinearNDInterpolator
import os
import re

## \brief Interpolation circuit.
#
# This is the circuit that caclaultes the interpolation of the force field provided. The force field must be in the following format, but plese note that the interpolation circuit is capable of taking
# any number of dimensions and components in, but for a case where there is an unequal amount of dimensions and components the unused components column must be filled with zeros. Except in the case
# of 3 dimensions and 1 component, this can be left as it is. Examples of how the force fields must be formated is shown below.: \n
# <pre> x y z Fx Fy Fz or x y z F or x y z Fx 0 0 or x y Fx 0 <pre>
#
# - \b Initialisation \b parameters:
# 	- \a Filename = Filename of the force field input file.
# 	- \a Dimensions = Number of dimensons in the force field.
# 	- \a Components = Number of components of force in the force field.
#
# - \b Input \b channels:
#         - \a coord : this is the coordiante to calcualte the interpolation.
#
# - \b Output \b channels:
#        - \a Fx: The interpolated forces where x is the component for example F1 would be first first component.
#
# \b Example:
# \code
# inter = machine.AddCircuit(type='Interpolate',name='inter', Filename = 'Force.dat', Dimensions = 3, Components = 3 ,pushed=True)
# \endcode
#

class Interpolate(Circuit):
    
    
	def __init__(self, machine, name, **keys):
		
		super(self.__class__, self).__init__( machine, name )

		self.minboundarycheck = False
		self.maxboundarycheck = False
		self.check = False
		self.Components = 1
		self.errorcheck = False

		#print self.AddInput("Filename")

		if 'Filename' in keys.keys():
			self.Filename = keys['Filename']
		else:
			raise NameError("Missing Filename input!")

		if 'Dimensions' in keys.keys():
			self.Dimensions = keys['Dimensions']
		else:
			raise NameError("Missing Dimensions input!")

		if 'Components' in keys.keys():
			self.Components = keys['Components']
		else:
			raise NameError("Missing Components input!")


		f = open(self.Filename, "r")
		for i in range(0,self.Components):
			self.AddOutput("F" + str(i+1) )

		self.AddInput("coord")

		#making a number of arrrays equal to the number of Dimensons
		self.pos = [[] for _ in range( self.Dimensions )]
		#making a number of arrrays equal to the number of Components
		self.comp = [[] for _ in range( self.Components )]

		#Check the input and read it!
		for line in f:
			
			#this is faster
			counter = len(line.split())
			
			if counter != self.Dimensions + self.Components:
				raise SyntaxError("ERROR: Incorrect number of Dimensions or Components entered!")

			#Fill Up the arrays
			
			words = line.split()
			for i in range(0,self.Dimensions):
				self.pos[i].append ( float(words[i]) )

			for i in range(0 ,self.Components):
				self.comp[i].append ( float(words[i + self.Dimensions]) )

		# I dont get this?!
		if self.Dimensions == 3 and self.Components == 1:
			self.check = True

	def Initialize (self):
		
		pass
	
	## Setting the maximum x y and z value of the force field
	#
	# @param *args will take in a coordiante and if the cantilever goes outwith this boundary a warning is printed on screen.
	#
	# \b Example:
	# \code{.py}
	# #For Dimensons = 3
	# inter = machine.AddCircuit(type='Interpolate',name='inter', Filename = 'Force.dat', Dimensons = 3, Components = 3 ,pushed=True)
	# inter.Maxboundary(10,10,10)
	# \endcode
	# 
	# \code{.py}
	# #For Dimensons = 2
	# inter = machine.AddCircuit(type='Interpolate',name='inter', Filename = 'Force.dat', Dimensons = 2, Components = 2 ,pushed=True)
	# inter.Maxboundary(10,10)
	# \endcode
	#
	# \code{.py}
	# #For Dimensons = 1
	# inter = machine.AddCircuit(type='Interpolate',name='inter', Filename = 'Force.dat', Dimensons = 1, Components = 1 ,pushed=True)
	# inter.Maxboundary(10)
	# \endcode
	#
	def Maxboundary(self, *args):
		self.max = []

		for i in range(0, len(args) ):
			self.max.append( args[i] )

		if len(self.min) != self.Dimensions:
			raise SyntaxError("ERROR! Number of dimensions in Minboundary is not equal to number in circuit Initialisation")

		self.maxboundarycheck = True


	## Setting the minimum x y and z value of the force field
	#
	# @param *args will take in a coordiante and if the cantilever goes outwith this boundary a warning is printed on screen.
	#
	# \b Example:
	# \code{.py}
	# #For Dimensons = 3
	# inter = machine.AddCircuit(type='Interpolate',name='inter', Filename = 'Force.dat', Dimensons = 3, Components = 3 ,pushed=True)
	# inter.Minboundary(0,0,0)
	# \endcode
	#                
	# \code{.py}
	# #For Dimensons = 2
	# inter = machine.AddCircuit(type='Interpolate',name='inter', Filename = 'Force.dat', Dimensons = 2, Components = 2 ,pushed=True)
	# inter.Minboundary(0,0)
	# \endcode
	#
	# \code{.py}
	# #For Dimensons = 1
	# inter = machine.AddCircuit(type='Interpolate',name='inter', Filename = 'Force.dat', Dimensons = 1, Components = 1 ,pushed=True)
	# inter.Minboundary(0)
	# \endcode
	def Minboundary(self, *args):
			self.min = []

			for i in range(0, len(args) ):
					self.min.append( args[i] )
			if len(self.min) != self.Dimensions:
					raise SyntaxError("ERROR! Number of dimensions in Minboundary is not equal to number in circuit Initialisation")
			self.minboundarycheck = True


			
	def Update (self):
			if self.maxboundarycheck == False:
					raise SyntaxError("No max boundarys for the force field added!")

			if self.minboundarycheck == False:
					raise SyntaxError("No min boundarys for the force field added!")



			if self.machine.time > 0 and self.errorcheck == False:


					for i in range(0, self.Dimensions):

							if type (self.I["coord"].value) == float:
									raise SyntaxError("ERROR: The positon for the interpolation holder was not found, maybe you forgot to connect the circuit?")


							if self.I["coord"].value[i] > self.max[i] or self.I["coord"].value[i] < self.min[i] :
									print "warning outside of force field!"
									self.errorcheck = True

			if self.machine.time > 0 and self.errorcheck == True:
					for i in range(0, self.Dimensions):
							if self.I["coord"].value[i] <= self.max[i] and self.I["coord"].value[i] >= self.min[i] :
									self.errorcheck = False


			if self.machine.time > 0 and self.check == False:
					for i in range(0 , self.Components):
							self.O["F" + str(i+1) ].value = numpy.interp(self.I["coord"].value[i], self.pos[i], self.comp[i])



			#special case of 3 dim and 1 comp
			if self.machine.time > 0 and self.check == True:
					for i in range(0 , self.Components):
							self.O[ "F" + str(i+1) ].value = self.I.__call__(self.I["coord"].value[0],self.I["coord"].value[1],self.I["coord"].value[2])



