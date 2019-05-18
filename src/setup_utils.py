# setup functions
import numpy as np


class CourantConditions:
    '''
    Class to compute the Courant conditions.
    '''

    def __init__(self, theta, dt, delta_r_prime,
                 sigma, delta_energy_prime):
        '''
        '''
        self.diffusion_courant = (theta *d t) / delta_r_prime
        print(f'Diffusion Courant condition is {self.diffusion_courant}')

        self.energy_sigma_courant = (sigma * dt) / delta_energy_prime
        print(f'Sigma Courant condition is {self.energy_sigma_courant}')

    def check_courant(self):
        error = 'Courant condition in diffusion '
        error += 'has not passed!'
        assert np.all(diffusioncourant) < 1.0, error

    # add energy Courant Condition
