from vafmbase import Circuit
from vafmcircuits import Machine
import math

import vafmcircuits_Filters
import vafmcircuits_math
import vafmcircuits_control
import vafmcircuits_signal_processing

## \package customs_pll
# Contain the assembly functions for composite PLL circuits.


## \brief Analog PLL composite circuit.
# Assembly function for analog PLL composite circuit.
# The Phase-Frequency Detector (PFD) multiplies the signals, and the result
# is passed to a series of lowpass Sallen-Key filters. The mount of filters
# and their cutoff frequencies are taken from the input parameter \a filters.
# 
# \note For this to work, the output \a sin should be connected to \a signal2 in the parent circuit (as shown in example). 
# Also, both signals should be normalised (amplitude = 1) and their offset should be removed.
#
#
# \htmlonly <div class="image"><a href="apll.png"><image src="apll.png" alt="aPLL schema" /></a> \endhtmlonly
#
# \b Initialisation \b parameters:
# - filters = list of cutoff frequencies for PFD lowpass filters
# - Kp = proportional constant of the charge pump
# - Ki = integral constant of the charge pump
# - gain = gain on the charge pump output
# - pushed = True|False  push the output buffer immediately if True
#
# \b Input \b channels:
# - \a signal1 = incoming signal
# - \a signal2 = reference signal
# - \a f0 = fundamental frequency
#
# \b Output \b channels:
# - \a sin = sine wave of the internal VCO
# - \a cos = cosine wave of the internal VCO
# - \a df = frequency shift from \a f0
#
# 
# \b Example:
# \code{.py}
#machine = Machine(name='machine', dt=1.0e-8, pushed=True);
#
#machine.AddCircuit(type="Machine",name='pll', assembly=aPLL, filters=[1000,500],
#	gain=600.0, f0=1.0e5, Kp=0.4, Ki=500)
#
#machine.Connect("pll.sin","pll.signal2")
# \endcode
#
def aPLL(compo,**keys):
	
	# I/O
  	compo.AddInput("signal1")
  	compo.AddInput("signal2")
  	compo.AddInput("f0")
  	
  	compo.AddOutput("sin")
  	compo.AddOutput("cos")
  	compo.AddOutput("df")
  	compo.AddOutput("dbg")
  	
  	
  	filters = keys['filters']
  	print "prefilters cutoffs: ",filters
  	
  	compo.AddCircuit(type='opMul',name='pfd', pushed=True)
  	for i in range(len(filters)):
		f = filters[i]
		compo.AddCircuit(type='ActiveLowPass',name='lp'+str(i+1),fcut=f, pushed=True)
	    
  	compo.AddCircuit(type='PI',name='pump', Kp=keys['Kp'],Ki=keys['Ki'], set=0, pushed=True)
	compo.AddCircuit(type='gain',name='dfgain', gain=keys['gain'], pushed=True)
  	compo.AddCircuit(type='opAdd',name='fsum', pushed=True)
  	compo.AddCircuit(type='waver',name='vco', amp=1, pushed=True)
  	

  	
  	#connections
  	compo.Connect("global.signal1","pfd.in1")
  	compo.Connect("global.signal2","pfd.in2")
  	
  	compo.Connect("pfd.out","lp1.signal")
	for i in range(1,len(filters)):
		compo.Connect("lp"+str(i)+".out","lp"+str(i+1)+".signal")
  	
  	compo.Connect("lp"+str(len(filters))+".out","pump.signal")
  	compo.Connect("pump.out","dfgain.signal")
  	compo.Connect("dfgain.out","fsum.in1","global.df")
  	compo.Connect("global.f0", "fsum.in2")
	compo.Connect("fsum.out",   "vco.freq")
	compo.Connect("vco.sin",   "global.sin")
	compo.Connect("vco.cos",   "global.cos")
	compo.Connect("pfd.out",   "global.dbg")
	
	#debug
	#out1 = compo.AddCircuit(type='output',name='output',file='pll.log', dump=1000)
	#out1.Register('global.time',"lp"+str(len(filters))+".out",'pump.out',"global.df")

	print "analog PLL assembled!"
