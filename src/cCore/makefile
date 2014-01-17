CC	= gcc
CFLAGS	= -c -w -std=c99 -fpic -O3
LFLAGS	= -w -lm -shared -fpic -O3 -o vafmcore.so


#CIRCUITS = core_container.o core_signals.o core_output.o core_maths.o core_logic.o  core_filters.o core_scanner.o

all: scanner container siggen outputs maths logics filters comparison control sigproc main.o 
	$(CC) $(LFLAGS) *.o
	rm *.o
	cp vafmcore.so ../.
	cp vafmcore.so ../../examples/.
main.o:
	$(CC) $(CFLAGS) main.c
outputs:
	$(CC) $(CFLAGS) core_output.c
maths: 
	$(CC) $(CFLAGS) core_maths.c
logics: 
	$(CC) $(CFLAGS) core_logic.c
comparison:
	$(CC) $(CFLAGS) core_comparison.c
siggen: 
	$(CC) $(CFLAGS) core_signals.c
filters: 
	$(CC) $(CFLAGS) core_filters.c
control:
	$(CC) $(CFLAGS) core_control.c
sigproc:
	$(CC) $(CFLAGS) core_signalprocessing.c
container: 
	$(CC) $(CFLAGS) core_container.c

scanner:
	$(CC) $(CFLAGS) core_scanner.c

clean:
	rm -rf *.o vafmcore.so
