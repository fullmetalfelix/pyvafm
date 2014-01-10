/**********************************************************
Output circuits definitions.
 *********************************************************/
#include <stdio.h>

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef COREOUTPUT
#include "core_output.h"
#endif



//int ID_output;

//deprecated
void INIT_OUTPUT(int* counter) {
  
  int i = *counter;
  pynames[i] = "output"; ufunctions[i] = output; i++;
  
  

  *counter = i;
  
}

int Add_output(int owner, char* filename, int dump) {

    circuit c = NewCircuit();

    c.nI = 1;
    c.nO = 0;

    c.iplen = 2;
    c.iparams = (int*)calloc(2,sizeof(int));
    c.iparams[0] = dump;
    c.iparams[1] = 0;

    c.vplen = 1;
    c.vpparams = (void**)malloc(sizeof(FILE*));//one element
    c.vpparams[0] = (void*)fopen(filename, "w");

    c.updatef = output;
    //c.update = ID_output;

    //*** ALLOCATE IN LIST *********************
    int index = AddToCircuits(c, owner);

    printf("Added output %i.\n",index);
    return index;
    
}

int output_register(int outer, int c, int chout) {

  circuits[outer].iparams[1]++;
  circuits[outer].iplen++;
  circuits[outer].iparams = (int*)realloc(circuits[outer].iparams,
			(2+circuits[outer].iparams[1])*sizeof(int));
  //printf("reallocating to size: %d\n",(2+circuits[outer].iparams[1]));
  

  circuits[outer].iparams[circuits[outer].iplen-1] = (c == -1)? 0:circuits[c].outputs[chout];

  return 0;
}

int output_register_feed(int outer, int feedid) {

    circuits[outer].iparams[1]++;
    circuits[outer].iplen++;
    circuits[outer].iparams = (int*)realloc(circuits[outer].iparams,
            (2+circuits[outer].iparams[1])*sizeof(int));

    circuits[outer].iparams[circuits[outer].iplen-1] = feedid;
    
    return 0;
}


int output_close(int outer) {
  
  fclose(circuits[outer].vpparams[0]);
  
  return 0;
}

void output( circuit *c ) {

  for(int i=2; i < c->iparams[1]+2; i++){
    //printf("%lf ",GlobalSignals[c->iparams[i]]);
    fprintf((c->vpparams[0]), "%15.8lf ", GlobalSignals[c->iparams[i]]);
    
  }
  //printf("\n");
  fprintf((c->vpparams[0]), "\n");
  //printf();
}


