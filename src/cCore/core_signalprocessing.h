#ifndef CORESIGNALPROCESSING
#define CORESIGNALPROCESSING

int Add_Gain(int owner, double gain) ;
void Gain( circuit *c );

int Add_minmax(int owner, double checktime);
void minmax( circuit *c );


#endif
