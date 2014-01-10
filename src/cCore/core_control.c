/**********************************************************
Control circuits definitions.
*********************************************************/

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef CORECONTROL
#include "core_control.h"
#endif


/*
 * TODO: add description of params
 * TODO: KI and KP should be input channels!
 * */
int Add_PIC(int owner, double kp, double ki ) {

        circuit c = NewCircuit();
        c.nI = 2;
        c.nO = 1;
        
        c.plen = 6;
        c.params = (double*)calloc(c.plen,sizeof(double));

        double delta = 0;
        double integral = 0;
        double oldint = 0;
        
        c.params[0] = kp;
        c.params[1] = ki;
        c.params[2] = 0;
        
        c.params[3] = integral;
        c.params[4] = oldint;
        c.params[5] = delta;



        c.updatef = PIC;
        
        int index = AddToCircuits(c,owner);
        printf("added PI circuit\n");
        return index;
}


void PIC( circuit *c ) {

        double delta = GlobalBuffers[c->inputs[1]] - GlobalBuffers[c->inputs[0]];

        
        // integral = integral + 0.5 * (oldint + ki * dekta) * dt
        c->params[3] = c->params[3] + ( 0.5*(c->params[4] + c->params[1] *delta)*dt);
        // output = delta * kp + integral
        GlobalBuffers[c->outputs[0]] = delta * c->params[0] + c->params[3];
        // oldint = ki * delta
        c->params[4] = c->params[1] * delta;

}


//TODO: add PID controller

