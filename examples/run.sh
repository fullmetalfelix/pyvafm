#!/bin/bash
cd ..
cd src/cCore
make
cd ../..
cd examples
python $0
gnuplot plot.plt