# setup functions
import numpy as np
from datetime import *
import logging

# Parameters that are set
kpc_to_cm = 3.08567758e21 # conversion factor from kpc to cm


def setup_logger(logger_name, log_file, level=logging.INFO):
    '''
    Function to set up logger.
    '''
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    l.setLevel(level)
    l.addHandler(fileHandler)
    return

class CourantConditions(object):
    '''
    Class to compute the Courant conditions.
    https://en.wikipedia.org/wiki/Courant%E2%80%93Friedrichs%E2%80%93Lewy_condition
    '''

    def __init__(self, theta, dt, delta_r_prime,
                 sigma, delta_energy_prime):
        '''
        Initialisation to find the diffusion
        '''
        self.diffusion_courant = (theta *dt) / delta_r_prime
        print(f'Diffusion Courant condition is {self.diffusion_courant}')

        self.energy_sigma_courant = (sigma * dt) / delta_energy_prime
        print(f'Sigma Courant condition is {self.energy_sigma_courant}')

    def check_diffusion_courant(self):
        error = 'Courant condition in Diffusion '
        error += 'has not passed!'
        assert np.all(self.diffusion_courant) < 1.0, error

    def check_energy_courant(self):
        error = 'Courant condition in Energy '
        error += 'has not passed!'
        assert np.all(self.energy_sigma_courant) < 1.0, error


    # add energy Courant Condition

class DefineParameters(object):
    '''
    Class to define starting parameters, import files
    and check inputs.
    '''
    def __init__(self, input_radi):
        self.final_radius = input_radi + 0.05
        self.derive_final_radius = input_radi + 0.15
        self.start_radius = 0.05
        self.delta_radius = 0.05

    def retrive_bfield(self, input_bfield_file):
        '''
        Method to retrive bfield and create a scaled bfield for modelling.

        Arguments
        -----------
        input_field_file: str
        Input magnetic field file location usually in microGauss
        but can be any unit as long as consistent


        Output
        -----------
        bfield_prime: np.array
        Normalised bfield in a numpy array

        '''
        bfield = np.loadtxt(input_bfield_file, unpack=True, usecols=[1])
        bfield_max = np.max(bfield)
        print(f'Bfeld0 is {bfield_max}')
        bfield_prime = bfield/bfield_max #normalise the magnetic field
        return bfield_prime

    def retrive_injection(self, input_injection_file):
        '''
        Method to retrive injection profile and create a scaled injection for
        modelling.

        Arguments
        -----------
        input_field_file: str
        Input injection file location

        Output
        -----------
        inputQ: np.array
        Normalised injection in a numpy array


        '''
        sourcey = np.loadtxt(input_injection_file, unpack=True, usecols=[1])

        inputQ = sourcey * 0.02
        Q0 = np.max(inputQ)/2
        inputQ = inputQ/Q0
        return inputQ

    def check_boundaries(self, injection_array):
        '''
        Method to check if the second derivative at nr is 0,
        all points in this region should be zero

        Arguments
        -----------
        injection_array: np.array
        Injection array
        '''
        error = 'Initial source boundary conditions unacceptable!'
        error += 'The final three entries in input source function need to be zero.'
        error += 'Please modify your source function.'
        assert np.all(inputQ[nr, nr-1, nr-2]) == 0, error
