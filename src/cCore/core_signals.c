/**********************************************************
Signal generators circuits definitions.
 *********************************************************/
#include <math.h>


#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef CORESIGNALS
#include "core_signals.h"
#endif

//deprecated
void INIT_SIGNALS(int* counter) {
  
  int i = *counter;
  
  pynames[i] = "waver"; ufunctions[i] = waver; i++;  
  
  
  *counter = i;

}

int Add_waver(int owner) {
    
    circuit c = NewCircuit();
    
    c.nI = 4;
    c.nO = 2;
    
    
    c.plen = 1;
    c.params = (double*) calloc(c.plen,sizeof(double));
    
    c.updatef = waver;

    
    //*** ALLOCATE IN LIST *********************
    int index = AddToCircuits(c,owner);
    
    printf("cCore: added waver %d\n",index);
    
    return index;
}

void waver( circuit *c ) {

    /*
    in[0]: freq
    in[1]: amp
    in[2]: phi
    in[3]: offset
    params[0]: phase
    out[0]: sin
    out[1]: cos
    */
    //printf("waving...\n");

    c->params[0] += dt*GlobalSignals[c->inputs[0]];
    //c->params[0] -= floor(c->params[0]);
    c->params[0] -= (int)(c->params[0]); //this is slightly faster than floor and itz the same for positive numbers!
    //printf("waving2...\n");


    double phase = 2*PI*(c->params[0]) + GlobalSignals[c->inputs[2]];
    GlobalBuffers[c->outputs[0]] = GlobalSignals[c->inputs[1]]*sin(phase)+GlobalSignals[c->inputs[3]];
    GlobalBuffers[c->outputs[1]] = GlobalSignals[c->inputs[1]]*cos(phase)+GlobalSignals[c->inputs[3]];
    
}

