# PhD-Simulations
## Vorpal Data Analyzer

This repository contains the example of simulations carried out during my PhD. My thesis entitled _Numerical Simulations on high-intensity laser-plasma interaction_.I was working on laser plasma acclerators theory and simulations. I was using software VORPAL Version 5.2 (now called VSIM) by Tech-X Corportations, specifically designed to carry out laser plasma accleration simulation.

The algorithm of the simulation was based on Particle-in-cell(PIC) method. The input file to modify the parameters and functions to be used while simulations was saved as an extension _.pre_. This pre file is processed by Vorpal to calculate all the values derived from pre file in an .in file that is fetched to Vorpal simulation software. 

Depending on the number of processors used, dimensionality of the problem to be simulated (1D, 2D or 3D) and values of the defined parameters in .pre file, total processing time of simulation varied from few minutes to 1 month. The number and size of the output files generated depend on the parameters defined in the simulation. The output contained the particles' position-momentum, electric/magnetic field and charge density values. 

_For a single simulation, the number of output files of the hdf5 format generated varied from 20-200 and size of single output .h5 file was about ~3-10 GB. There was no way, but to run and store simulations on large scale clusters and supercomputers_. These output files are then processed by Vorpal Data Analyzer which extract the data from .h5 files and manipulate it to get the final results. 

####The program Vorpal Data Analyzer was designed to be used for all kind of simulations run on Vorpal Version 5.2 or higher using python 2.6. The code was developed by my colleague Shushil Kumar Sawant and me.#### 

For further reading, check out my publications in international journal

1. Simulation of laser-driven plasma beat-wave propagation in collisional weakly relativistic plasmas
https://iopscience.iop.org/article/10.1209/0295-5075/116/35001/meta

2. Electron energy optimization by plasma density ramp in laser wakefield acceleration in bubble regime
https://www.cambridge.org/core/journals/laser-and-particle-beams/article/electron-energy-optimization-by-plasma-density-ramp-in-laser-wakefield-acceleration-in-bubble-regime/520B316345107D57375A793603EEF110

3. Evolution of laser pulse shape in a parabolic plasma channel
https://iopscience.iop.org/article/10.1088/1054-660X/27/1/015401/meta
