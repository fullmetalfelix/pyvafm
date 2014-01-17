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

    c.iplen = 3;
    c.iparams = (int*)calloc(c.iplen,sizeof(int));
    c.iparams[0] = dump;
    c.iparams[1] = 0; //step counter
    c.iparams[2] = 0; //number of channels to print

    c.vplen = 1;
    c.vpparams = (void**)malloc(sizeof(FILE*));//one element
    c.vpparams[0] = (void*)fopen(filename, "w");

    c.updatef = output;

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

    circuits[outer].iparams[2]++;
    circuits[outer].iplen++;
    circuits[outer].iparams = (int*)realloc(circuits[outer].iparams,
            circuits[outer].iplen*sizeof(int));

    circuits[outer].iparams[circuits[outer].iplen-1] = feedid;
    
    return 0;
}

void output_dump( int index ) {
    
    //circuits[index].updatef(&(circuits[index]));
    output_printout( &(circuits[index]) );
}

void output_printout( circuit *c ) {
    
    for(int i=3; i < c->iplen; i++){
        
        //printf("%lf ",GlobalSignals[c->iparams[i]]);
        fprintf((c->vpparams[0]), "%15.8lf ", GlobalSignals[c->iparams[i]]);
        
    }
    //printf("\n");
    fprintf((c->vpparams[0]), "\n");
}

int output_close(int outer) {
  
  fclose(circuits[outer].vpparams[0]);
  
  return 0;
}

void output( circuit *c ) {

    if(c->iparams[0] <= 0) {
        //printf("asd!\n");
        if(GlobalSignals[c->inputs[0]] > 0) {
            output_printout(c); //do the print out
        }
        
        return;
    }
    
    c->iparams[1]++;
    
    if(c->iparams[1] >= c->iparams[0]) {
        
        output_printout(c); //do the print out
        c->iparams[1] = 0;
    
    }

}


