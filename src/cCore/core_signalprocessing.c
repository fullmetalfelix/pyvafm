/**********************************************************
Comparison circuits definitions.
*********************************************************/

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef CORESIGNALPROCESSING
#include "core_signalprocessing.h"
#endif



int Add_Gain(int owner, double gain) {

        circuit c = NewCircuit();
        c.nI = 1;
        c.nO = 1;
        
        c.plen = 1;
        c.params = (double*)calloc(c.plen,sizeof(double));
        
        c.params[0] = gain;
        
        c.updatef = Gain;
        
        int index = AddToCircuits(c, owner);
        printf("added Gain circuit\n");
        return index;
}
void Gain( circuit *c ) {

        GlobalBuffers[c->outputs[0]] = GlobalBuffers[c->inputs[0]]* c->params[0];
}


int Add_minmax(int owner, double checktime) {

        circuit c = NewCircuit();
        c.nI = 1;
        c.nO = 4;
        
        c.plen = 2;
        c.params = (double*)calloc(c.plen,sizeof(double));
        
        
        c.iplen = 2;
        c.iparams = (int*)calloc(c.iplen,sizeof(int));
        
        c.iparams[0] = (int)(floor(checktime/dt)); //checktime in steps
        c.iparams[1] = 0; //step counter
        
        c.updatef = minmax;
        
        int index = AddToCircuits(c, owner);
        printf("added minmax circuit %i\n",c.iparams[0]);
        return index;
}
void minmax( circuit *c ) {

    double signal = GlobalSignals[c->inputs[0]];
    
    if (signal > c->params[0])
        c->params[0] = signal; //max
    if (signal < c->params[1])
        c->params[1] = signal; //min
    
    c->iparams[1]++;
	
	//if the counter is equal to the amount of time steps then then output the values
    if (c->iparams[1] >= c->iparams[0]) {

        GlobalBuffers[c->outputs[0]] = c->params[0];
        GlobalBuffers[c->outputs[1]] = c->params[1];

        GlobalBuffers[c->outputs[2]] = (c->params[0] - c->params[1])*0.5;
        GlobalBuffers[c->outputs[3]] = (c->params[0] + c->params[1])*0.5;

        //reset min and max for the next calculation
        c->params[1] = signal;
        c->params[0] = signal;

        c->iparams[1] = 0;
    }
    
}


