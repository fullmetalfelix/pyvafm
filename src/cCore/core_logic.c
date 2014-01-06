/**********************************************************
Logical circuits definitions.
 *********************************************************/

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef CORELOGIC
#include "core_logic.h"
#endif


int LogicStart, LogicEnd;

void INIT_LOGIC(int* counter) {

    int i = *counter;
    LogicStart = i;

    pynames[i] = "opAND"; ufunctions[i] = opAND; i++;
    pynames[i] = "opOR"; ufunctions[i] = opOR; i++;

    LogicEnd = i-1;
    *counter = i;

}


int Add_Logic(char* type, int ni) {
    
    circuit c = NewCircuit();

    c.nI = ni;
    c.nO = 1;

    int template = GetCircuitIndex(type);
    if(template < LogicStart || template > LogicEnd) {
        printf("cERROR! type [%s] is not a logic circuit!\n",type);
        errorflag++;
    }
    
    c.updatef = ufunctions[template];
    
    int index = AddToCircuits(c);
    
    printf("Added logic [%s].\n",type);
    return index;
    
}


void opAND( circuit *c ) {

  double result = 1;
  for(int i=0; i < c->nI; i++){
    if(GlobalSignals[c->inputs[i]] <= 0) {
      result = 0;
      break;
    }
  }
  GlobalBuffers[c->outputs[0]] = result;
}

void opOR( circuit *c ) {

  double result = 0;
  for(int i=0; i < c->nI; i++){
    if(GlobalSignals[c->inputs[i]] > 0) {
      result = 1;
      break;
    }
  }
  GlobalBuffers[c->outputs[0]] = result;
}
