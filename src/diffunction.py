from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import os
import csv

class Params:
    """
    """

    def __init__(self):
        """
        Params()
        Intitializes the parameter list with default values. Change parameters
        by directly accessing these class variables.
        """
        self.diffcoeffr = 2.8e28
        self.iter = 10000
        self.diffcoeffz = 2.8e28
        self.inputarray = ''
        self.inputmagnetic = 'bfield15kpc300.txt'
        self.inputsource = 'sourcefunction15kpc.txt'
        self.outputdir = 'makingplotsfortalk'
    def __call__(self):
        """
        """
        print('CREPE Input parameters:')
        print (f'Diffusion coefficient in radial direction:{self.diffcoeffr}')
        print(f'Number of iterations:{self.iter}')
        print(f'Diffusion coefficient in vertical direction:{self.diffcoeffz}')
        print(f'Input numpy array:{self.inputarray}')
        print(f'Input magnetic field distribution:{self.inputmagnetic}')
        print(f'Input magnetic field distribution:{self.inputsource}')
        print(f'Output files to be place in:{self.outputdir}')


def readfromparset(infile):

    reader = csv.reader(open(str(infile), 'rb'), delimiter=" ", skipinitialspace=True)

    params = Params()

    parset = dict()

    for row in reader:
            if len(row) != 0 and row[0] != '%':
                parset[row[0]] = row[1]
            else:
                continue

    params.diffcoeffr = float(parset['diffcoeffr'])
    params.iter = float(parset['iter'])
    params.diffcoeffz = float(parset['diffcoeffz'])
    params.inputarray = parset['inputarray']
    params.outputarray = parset['outputarray']
    params.inputmagnetic = parset['inputmagnetic']
    params.inputsource = parset['inputsource']
    params.outputdir = parset['outputdir']

    print('CREPE Input parameters:')
    print(f'Diffusion coefficient in radial direction:{params.diffcoeffr}')
    print(f'Number of iterations:{params.iter}')
    print(f'Diffusion coefficient in vertical direction:{params.diffcoeffz}')
    print(f'Input numpy array:{params.inputarray}')
    print(f'Output numpy array:{params.outputarray}')
    print(f'Input magnetic field distribution:{params.inputmagnetic}')
    print(f'Input injection distribution:{params.inputsource}')
    print(f'Output files to be placed in:{params.outputdir}')

    return params

def findinterpolpoints2low(QE):
    '''
    Explain

    Arguments
    ---------

    Output
    ----------
    '''
    lowQE = (QE[0] - 2*(QE[1] - QE[0])) #locked off
    return lowQE

def findinterpolpointslow(QE):
    '''
    Explain

    Arguments
    ---------

    Output
    ----------
    '''
    lowQE = (QE[0] - (QE[1] - QE[0])) #locked of
    return lowQE

def findinterpolpointslowenergy(QE):
    '''
    Explain

    Arguments
    ---------

    Output
    ----------
    '''
    if  QE[0]==0:
        lowQE=0
    else:
        lowQE = (QE[0]**2)/QE[1] #checked
    return lowQE

def findinterpolpointshighenergy(QE, ne, debug = False):
    '''
    Explain

    Arguments
    ---------

    Output
    ----------
    '''
    if debug is True:
        print(f'finalpoint is {QE[ne]}')
        print(f'second final point is {QE[ne-1]}')
    if  QE[ne] == 0 or QE[ne-1] == 0:
        highQE = 0
    else:
        highQE = (QE[ne]**2)/QE[ne-1] #checked
    if highQE < 0:
	#highQE=0
	return highQE
    else:
	return highQE

#function finding the nearest energy value to 1.4GHz and 151 MHz.
def find_nearest(targetarray, value, bfeldy, E):
    '''
    Function finding the nearest energy value to 1.4GHz and 151 MHz.

    Arguments
    ---------

    Output
    ----------
    '''
    n=0
    outputarray = []
    outputenergy = []
    #E = E/1.6e-12
    for makefreq in E:
        freqrange = 16*(((E))**2)*(bfeldy*1e6)#calculating frequency range E is ALREADY in Ge
        #freqrange = 16*(((E)/1e9)**2)*(bfeldy[n]*1e6)#calculating frequency range E is in Ge
        #print 'freqrange is', freqrange
        idx = (np.abs(freqrange-value)).argmin()
        outputarray = np.append(outputarray,targetarray[idx,n])
        outputenergy = np.append(outputenergy,E[idx])
        n=n+1
        #print n
    return outputarray, outputenergy
