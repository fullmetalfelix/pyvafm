/**********************************************************
Comparison circuits definitions.
*********************************************************/

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef CORESIGNALPROCESSING
#include "core_signalprocessing.h"
#endif



int Add_Gain(int owner, char* type, double gain) {

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
