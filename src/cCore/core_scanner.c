/**********************************************************
Arithmetic circuits definitions.
 *********************************************************/
#include <math.h>
#include <stdio.h>
#include <stdlib.h> 

#ifndef CIRCUIT
#include "circuit.h"
#endif

#ifndef CORESCANNER
#include "core_scanner.h"
#endif

double CurrentX=0;
double CurrentY=0;
double CurrentZ=0;
int Record = 1;

void Place(double x, double y, double z)
{
    CurrentX = x;
    CurrentY = y;
    CurrentZ = z;
    printf("Tip placed at %f, %f, %f \n", x ,y ,z);
}

void Idle( double T)
{
    int i;
    for (i = 0; i<floor(T/dt); i++)
    {
    Update(1);
    }
}


void Move(double x, double y, double z, double v)
{
    double oldx = CurrentX;
    double oldy = CurrentY;
    double oldz = CurrentZ;

    double stepx = x/v*dt;
    double stepy= y/v*dt;
    double stepz= z/v*dt;

    int i;
    for (i = 0; i<floor(v/dt); i++)
    {
    CurrentX = CurrentX + stepx;
    CurrentY = CurrentY + stepy;
    CurrentZ = CurrentZ + stepz;

    Update(1);
    }

    if ( (CurrentX-oldx) != x || (CurrentY-oldy) != y || (CurrentZ-oldz) != z)
    {
        CurrentX = oldx+x;
        CurrentY = oldy+y;
        CurrentZ = oldz+z;
        Update(1);
    }
    printf("Tip adjusted by %f %f %f \n", CurrentX, CurrentY, CurrentZ);

}

void MoveTo(double x, double y, double z, double v)
{
    double oldx = CurrentX;
    double oldy = CurrentY;
    double oldz = CurrentZ;

    double stepx = (x-CurrentX)/v*dt;
    double stepy= (y-CurrentY)/v*dt;
    double stepz= (z-CurrentZ)/v*dt;

    int i;
    for (i = 0; i<floor(v/dt); i++)
    {
    CurrentX = CurrentX + stepx;
    CurrentY = CurrentY + stepy;
    CurrentZ = CurrentZ + stepz;

    Update(1);
    }
    //if the positon is not a integral number of steps then use one cycle to adjust it 
    if ( (CurrentX) != x || (CurrentY) != y || (CurrentZ) != z)
    {
        CurrentX = x;
        CurrentY = y;
        CurrentZ = z;
        Update(1);
    }
    printf("Moved To %f %f %f \n", CurrentX, CurrentY, CurrentZ);
}

void Scan(double x, double y, double z, double v, int points)
{
    int counter = 0;
    double oldx = CurrentX;
    double oldy = CurrentY;
    double oldz = CurrentZ;

    double stepx = (x-CurrentX)/v*dt;
    double stepy= (y-CurrentY)/v*dt;
    double stepz= (z-CurrentZ)/v*dt;

    int i;
    for (i = 0; i<floor(v/dt); i++)
    {
    Record = 0;

    CurrentX = CurrentX + stepx;
    CurrentY = CurrentY + stepy;
    CurrentZ = CurrentZ + stepz;
    counter ++;
    if (counter == points)
        {
            Record = 1;
            counter = 0;
        }
 
    Update(1);

    }

    Record = 1;
    //if the positon is not a integral number of steps then use one cycle to adjust it 
    if ( (CurrentX) != x || (CurrentY) != y || (CurrentZ) != z)
    {
        CurrentX = x;
        CurrentY = y;
        CurrentZ = z;
        Update(1);
    }
    printf("Scanned To %f %f %f \n", CurrentX, CurrentY, CurrentZ);

}


int Scanner( int owner)
{
    circuit c = NewCircuit();
    c.nI = 0;
    c.nO = 4;

    c.updatef = UpdateScanner;
  
    int index = AddToCircuits(c,owner);
    printf("cCore: Scanner Initialised\n");
    return index;
}

void UpdateScanner( circuit *c )
{
    GlobalBuffers[c->outputs[0]] = CurrentX;
    GlobalBuffers[c->outputs[1]] = CurrentY;
    GlobalBuffers[c->outputs[2]] = CurrentZ;
    GlobalBuffers[c->outputs[3]] = Record;
}

