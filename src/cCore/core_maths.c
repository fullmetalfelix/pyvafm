/**********************************************************
Arithmetic circuits definitions.
 *********************************************************/
#include <math.h>

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef COREMATHS
#include "core_maths.h"
#endif


int MathStart, MathEnd;
void INIT_MATHS(int* counter) {

    int i = *counter; MathStart = i;
    pynames[i] = "opADD"; ufunctions[i] = opADD; i++;
    pynames[i] = "opSUB"; ufunctions[i] = opSUB; i++;
    pynames[i] = "opMUL"; ufunctions[i] = opMUL; i++;
    pynames[i] = "opDIV"; ufunctions[i] = opDIV; i++;
    pynames[i] = "opABS"; ufunctions[i] = opABS; i++;
    pynames[i] = "opPOW"; ufunctions[i] = opPOW; i++;
    pynames[i] = "opLINC"; ufunctions[i] = opPOW; i++;

    MathEnd = i-1;
    *counter = i;

}

int Add_Math(int owner, char* type, int ni) {
    
    circuit c = NewCircuit();

    c.nI = ni;
    c.nO = 1;

    //c.plen = 1;
    //c.params = (double*)calloc(c.plen,sizeof(double));

    int template = GetCircuitIndex(type);
    if(template < MathStart || template > MathEnd) {
        printf("cERROR! type [%s] is not a maths circuit!\n",type);
        errorflag++;
    }
    
    //c.update = template;
    c.updatef = ufunctions[template];
    
    int index = AddToCircuits(c,owner);
    
    //printf("Added maths [%s].\n",type);
    return index;
    
}


void opADD( circuit *c ) {
  
    double result = 0;
    for(int i=0; i < c->nI; i++){
        result += GlobalSignals[c->inputs[i]];
        
    }

    GlobalBuffers[c->outputs[0]] = result;
    
}

void opSUB( circuit *c ) {

  double result = 0;
  result = GlobalSignals[c->inputs[0]]-GlobalSignals[c->inputs[1]];
  
  GlobalBuffers[c->outputs[0]] = result;
 
}
void opMUL( circuit *c ) {
  double result = 1;
  for (int i=0; i<c->nI; i++){

  result *= GlobalSignals[c->inputs[i]];

}
  
  GlobalBuffers[c->outputs[0]] = result;
 
}
void opDIV( circuit *c ) {

  double result = 0;
  result = GlobalSignals[c->inputs[0]]/GlobalSignals[c->inputs[1]];
  
  GlobalBuffers[c->outputs[0]] = result;
 
}
inline void opABS( circuit *c ) {
  
  GlobalBuffers[c->outputs[0]] = fabs(GlobalSignals[c->inputs[0]]);
 
}

void opPOW( circuit *c ) {

  double result = pow(GlobalSignals[c->inputs[0]],GlobalSignals[c->inputs[1]]);
  
  GlobalBuffers[c->outputs[0]] = result;
 
}
void opLINC( circuit *c ) {

    double result = 0;
    
    for(int i=0; i < c->nI; i+=2) {
        result += GlobalSignals[c->inputs[i]]*GlobalSignals[c->inputs[i+1]];
    }
    
    GlobalBuffers[c->outputs[0]] = result;
 
}

/*
void opSUB( circuit *c ) {

  double result = 0;
  result = GlobalSignals[c->inputs[0]]-GlobalSignals[c->inputs[1]];
  
  GlobalBuffers[c->outputs[0]] = result;
 
}
void opMUL( circuit *c ) {

  double result = 0;
  result = GlobalSignals[c->inputs[0]]*GlobalSignals[c->inputs[1]];
  
  GlobalBuffers[c->outputs[0]] = result;
 
}
void opDIV( circuit *c ) {

  double result = 0;
  result = GlobalSignals[c->inputs[0]]/GlobalSignals[c->inputs[1]];
  
  GlobalBuffers[c->outputs[0]] = result;
 
}
inline void opABS( circuit *c ) {
  
  GlobalBuffers[c->outputs[0]] = fabs(GlobalSignals[c->inputs[0]]);
 
}

void opPOW( circuit *c ) {

  double result = pow(GlobalSignals[c->inputs[0]],GlobalSignals[c->inputs[1]]);
  
  GlobalBuffers[c->outputs[0]] = result;
 
}
void opLINC( circuit *c ) {

    double result = 0;
    
    for(int i=0; i < c->nI; i+=2) {
        result += GlobalSignals[c->inputs[i]]*GlobalSignals[c->inputs[i+1]];
    }   
    
    GlobalBuffers[c->outputs[0]] = result;
 
}
*/

