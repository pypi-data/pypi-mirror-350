# Copyright (c) 2024 The KUTE contributors

import numpy as np
from scipy.signal import correlate
from scipy.integrate import cumulative_trapezoid
from typing import Optional, Dict, List, Tuple


class GreenKuboIntegral():
    """
    Class to calculate and manage correlation functions, their integrals and transport properties derived from them.

    Args:
        t (np.ndarray): One dimensional array of shape (N). The timesteps in
            which the current is measured.
        
        J1 (np.ndarray): Two dimensional array of shape (M, N). Each row is an
            independent measurement of N points of the first component of the
            current.
        
        J2 (np.ndarray): Two dimensional array of shape (M, N). Each row is an
            independent measurement of N points of the second component of the
            current.
        
        J3 (np.ndarray): Two dimensional array of shape (M, N). Each row is an
            independent measurement of N points of the third component of the
            current.
    """

    def __init__(self, t: np.ndarray, J1: np.ndarray, J2: np.ndarray, J3: np.ndarray):
        self.time = t
        self.J1 = J1
        self.J2 = J2
        self.J3 = J3
        # self.caf: Dict[str, Optional[np.ndarray]] = {
        #     "11": None, "22": None,"33": None, "12": None,"13": None,
        #     "23": None}
        self.caf: Dict[str, np.ndarray] = {}
        # self.cumulative_integral: Dict[str, Optional[np.ndarray]] = {
        #     "11": None, "22": None, "33": None, "12": None, "13": None,
        #     "23": None}
        self.cumulative_integral: Dict[str, np.ndarray] = {}
        # self.running_average: Dict[str, Optional[np.ndarray]] = {
        #     "11": None, "22": None, "33": None, "12": None, "13": None,
        #     "23": None}
        self.running_average: Dict[str, np.ndarray] = {}
        self.dt: float = t[1] - t[0]
        self._calculated_caf = False
        self._calculated_integral = False
        self._calculated_running_average = False

        
    def set_time_to_zero(self):
        """
        Shifts the time origin so that self.time[0] = 0
        """
        self.time -= self.time[0] * np.ones(len(self.time))


    @staticmethod
    def get_correlation_function(j1: np.ndarray, j2: np.ndarray) -> np.ndarray:
        """
        Method for quickly calculating a correlation function and its uncertainty.

        Args:
            j1 (np.ndarray): Two dimensional array of shape (M, N). It represents M measurings of a signal consisting of
            N points.
            j2 (np.ndarray): Two dimensional array of shape (M, N). It represents M measurings of a signal consisting of
            N points.

        Returns:
            np.ndarray: Two dimensional array of shape (N-1, 2). The first
            column contains the correlation <j1(t0) * j2(t0+t)>, averaged over
            all time origins t0 and all samples M The second column contains the
            uncertainty of the correlation function.
        
        Raises:
            ValueError: If the two entries don't have the same shape
        """

        if j1.shape != j2.shape:
            raise ValueError("Correlation cannot be calculated between entries with different sizes")

        try:
            M, N = j1.shape
        except:
            j1 = j1[np.newaxis, :]
            j2 = j2[np.newaxis, :]
            M, N = j1.shape


        caf = np.zeros(N-1)
        caf2 =np.zeros(N-1)
        contributions = np.array([N-k for k in range(N-1)])

        for A in range(M):

            caf += correlate(j1[A, :], j2[A, :])[N-1:-1]
            caf2 += correlate(j1[A, :]**2, j2[A, :]**2)[N-1:-1]

        caf /= M * contributions
        caf2 /= M * contributions

        unc_caf = np.sqrt(caf2 - caf**2) / np.sqrt(M*contributions - 1)

        return np.array([caf, unc_caf]).T
    
    def _calculate_correlation(self):    
        """
        Calculates all independent autocorrelation functions, C_11, C_22, C_33,
        C_12, C_13 and C_23, as well as their uncertainties. They are stored in
        self.caf under different keys.
        """ 
        
        if not self._calculated_caf:

            self.caf["11"] = self.get_correlation_function(self.J1, self.J1)
            self.caf["22"] = self.get_correlation_function(self.J2, self.J2)
            self.caf["33"] = self.get_correlation_function(self.J3, self.J3)
            self.caf["12"] = self.get_correlation_function(self.J1, self.J2)
            self.caf["13"] = self.get_correlation_function(self.J1, self.J3)
            self.caf["23"] = self.get_correlation_function(self.J2, self.J3)

            self._calculated_caf = True
        

    def _calculate_integral(self):
        """
        Calculates the cumulative integral of the various autocorrelation
        functions and their uncertainties. They get stored in
        self.cumulative_integral under different keys.
        """
        
        if not self._calculated_caf:
            raise RuntimeError("The correlation functions have not been calculated yet")

        if not self._calculated_integral:

            for key in list(self.caf.keys()):
                caf = self.caf[key][:, 0]
                unc_caf = self.caf[key][:, 1]
                cumul = cumulative_trapezoid(caf, self.time[:-1], initial = 0)
                
                unc_trapzs = np.zeros(len(caf))
                unc_trapzs[1:] = (self.dt/2)*np.sqrt(np.array([ unc_caf[i]**2 + unc_caf[i-1]**2 for i in range(1, len(cumul)) ]))
                unc_cumul = np.sqrt(np.cumsum(unc_trapzs**2))
                self.cumulative_integral[key] = np.array([cumul, unc_cumul]).T
            
            self._calculated_integral = True

           

    
    def _calculate_running_average(self):
        """
            Calculates the running average for all time steps, given by the
            weighted average of the cumulative integral from a given timestep to
            the last one, and for all tensor components. This has N-1 values,
            with N the length of the cumulative integral. The values and their
            uncertainties are stored in self.running_average under different
            keys.
        """

        if not self._calculated_running_average:
            if not self._calculated_caf or not self._calculated_integral:
                raise RuntimeError("The correlation functions have not been calculated yet")

            for key in list(self.caf.keys()):

                ## The values of the cumulative integral and the corresponding weights are stored in arrays
                ## The arrays are flipped so that they structure is [ cumul(N), cumul(N-1), ..., cumul(0) ]

                flipped_cumul = np.flip(self.cumulative_integral[key][1:, 0])
                flipped_weights = np.flip(self.cumulative_integral[key][1:, 1]) ** (-2)
                contributions = np.flip(np.arange(len(flipped_cumul)-1) + 2)

                ## From the flipped arrays, the weighted average for each choice of beggining of averaging can be calculated as follows
                ## The last point is not calculated, because it corresponds to an average of a single point

                running_average = np.flip(np.cumsum(flipped_cumul * flipped_weights) / np.cumsum(flipped_weights))[:-1]
                running_average2 = np.flip(np.cumsum(flipped_cumul**2 * flipped_weights) / np.cumsum(flipped_weights))[:-1]

                uncertainty = np.sqrt((running_average2 - running_average**2)/contributions)

                shape = (len(running_average), 2)
                self.running_average[key] = np.zeros(shape)
                self.running_average[key][:, 0] = running_average
                self.running_average[key][:, 1] = uncertainty
            
            self._calculated_running_average = True
        


    def analyze(self):
        """
            Performs the analysis for the system. This consists of calculating
            correlations, running integrals and running averages.
        """

        self._calculate_correlation()
        self._calculate_integral()
        self._calculate_running_average()

    
    def get_running_average(self, keys:list)-> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculates the running average integral and its uncertainty, averaging
        over the given components of the transport tensor
        Args:
            keys (list): A selection of keys ("11", "22", "33", "12", "13", "23") to average over. Supports a single component (keys=["11"] for example), but note that this will return data already present in self.caf.

        Returns:
            time (np.ndarray): Times corresponding to the values
            average (np.ndarray): Isotropic running average
            uncertainty (np.ndarray): Uncertainty of the running average
        """

        self.analyze()
        NKEYS = len(keys)
        L = len(self.running_average[keys[0]][:, 0])

        ## If only one key is provided, the returned values are the ones already calculated and stored for that component

        if NKEYS == 1:

            return self.time[:L], self.running_average[keys[0]][:, 0], self.running_average[keys[0]][:, 1]

        values = np.zeros((NKEYS, L))
        weights = np.zeros((NKEYS, L))

        for j, key in enumerate(keys):

            values[j, :] = self.running_average[key][:, 0]
            weights[j, :] = self.running_average[key][:, 1] ** (-2)

        average = np.sum(values*weights, axis=0) / np.sum(weights, axis=0)
        variance2 = np.sum(weights * (values - average[np.newaxis, :])**2, axis=0) / np.sum(weights, axis=0)
        uncertainty = np.sqrt((1./(NKEYS-1)) * variance2)

        return self.time[:L], average, uncertainty


    def get_isotropic_running_average(self)-> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculates the running average integral and its uncertainty, averaging
        over the isotropic components of the transport tensor

        Returns:
            time (np.ndarray): Times corresponding to the values
            average (np.ndarray): Isotropic running average
            uncertainty (np.ndarray): Uncertainty of the running average
        """
        
        return self.get_running_average(["11", "22", "33"])
        

    def get_anisotropic_running_average(self)-> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculates the running average integral and its uncertainty, averaging
        over the anisotropic components of the transport tensor

        Returns:
            time (np.ndarray): Times corresponding to the values
            average (np.ndarray): Isotropic running average
            uncertainty (np.ndarray): Uncertainty of the running average
        """

        return self.get_running_average(["12", "13", "23"])


    def get_average_correlation_function(self, keys):
        """
        Calculates the running correlation function and its uncertainty, averaging
        over the given components of the transport tensor
        Args:
            keys (list): A selection of keys ("11", "22", "33", "12", "13", "23") to average over. Supports a single component (keys=["11"] for example), but note that this will return data already present in self.caf.

        Returns:
            time (np.ndarray): Times corresponding to the values
            average (np.ndarray): Average correlation function
            uncertainty (np.ndarray): Uncertainty of the correlation function
        """
        self.analyze()
        NKEYS = len(keys)
        L = len(self.caf[keys[0]][:, 0])

        ## When only one key is provided, the results is already stored in self.caf

        if NKEYS == 1:
            return self.time[:L], self.caf[keys[0]][:, 0], self.caf[keys[0]][:, 0]

        values = np.zeros((NKEYS, L))
        weights = np.zeros((NKEYS, L))

        for j, key in enumerate(keys):

            values[j, :] = self.caf[key][:, 0]
            weights[j, :] = self.caf[key][:, 1] ** (-2)

        average = np.sum(values*weights, axis=0) / np.sum(weights, axis=0)
        variance2 = np.sum(weights * (values - average[np.newaxis, :])**2, axis=0) / np.sum(weights, axis=0)
        uncertainty = np.sqrt((1./(NKEYS-1)) * variance2)

        return self.time[:L], average, uncertainty
    

    def get_isotropic_correlation_function(self):
        """
        Calculates the average correlation function and its uncertainty, averaging
        over the isotropic components

        Returns:
            time (np.ndarray): Times corresponding to the values
            average (np.ndarray): Isotropic correlation function
            uncertainty (np.ndarray): Uncertainty of the correlation function
        """
        return self.get_average_correlation_function(["11", "22", "33"])
    
    def get_anisotropic_correlation_function(self):
        """
        Calculates the average correlation function and its uncertainty, averaging
        over the anisotropic components

        Returns:
            time (np.ndarray): Times corresponding to the values
            average (np.ndarray): Isotropic correlation function
            uncertainty (np.ndarray): Uncertainty of the correlation function
        """
        return self.get_average_correlation_function(["12", "13", "23"])


class IntegralEnsemble():
    """
    Class to manage a collection of replicas when calculating transport
    properties

    Args:
        green_kubo_integrals (list): A list of instances of the
            GreenKuboIntegral class, with the values of the current for each
            replica
        factors (np.ndarray,optional): Multiplying factors for the average
            integral of each replica. Can be used for changing units, or to
            implement a factor that changes among
            replicas (1/V for example). The default is no weights are applied.
    Raises
    ------
    ValueError 
        If the GreenKuboIntegral objects have non matching times
    ValueError
        If the length of factors does not match the number of replicas
    """

    def __init__(self, green_kubo_integrals: List[GreenKuboIntegral], 
                 factors: Optional[np.ndarray]=None):
        self.gk_integrals = green_kubo_integrals
        self.N_REPLICAS = len(green_kubo_integrals)
        self.time = green_kubo_integrals[0].time
        self.LENGTH = len(self.time) - 3

        for integral in green_kubo_integrals:
            if np.all(self.time != integral.time):
                raise ValueError("Integrals with non matching times were given")
            
        if factors is None:
            self.FACTORS = np.ones(self.N_REPLICAS)
        else:
            if len(factors) != self.N_REPLICAS:
                raise ValueError("Length of the prefactors does not match the number of replicas")
            else:
                self.FACTORS = factors


    def get_average_over_components(self, keys: list) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculates the running average of one or more components of the transport tensor across all replicas

        Args:
            key (list): A list of strings (11, 22, 33, 12, 13 or 23). The components to be 
                        averaged over. Supports a single component (keys=["11"], for example)

        Returns:
            time (np.ndarray): Times corresponding to the values
            average (np.ndarray): Isotropic running average
            uncertainty (np.ndarray): Uncertainty of the running average
        """

        replica_values = np.zeros((self.N_REPLICAS, self.LENGTH))
        replica_weights = np.zeros((self.N_REPLICAS, self.LENGTH))

        for i, (integral, FACTOR) in enumerate(zip(self.gk_integrals, self.FACTORS)):
            
            integral.analyze()
            _, val, uval = integral.get_running_average(keys)
            replica_values[i, :] = FACTOR * val
            replica_weights[i, :] = FACTOR * uval

        average = np.sum(replica_values*replica_weights, axis=0) / np.sum(replica_weights, axis=0)
        variance2 = np.sum(replica_weights * (replica_values - average[np.newaxis, :])**2, axis=0) / np.sum(replica_weights, axis=0)
        uncertainty = np.sqrt(variance2 / (self.N_REPLICAS - 1))

        return self.time[:self.LENGTH], average, uncertainty
    

    def get_isotropic_average(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculates the isotropic average of the transport tensor across all replicas

        Returns:
            time (np.ndarray): Times corresponding to the values
            average (np.ndarray): Isotropic running average
            uncertainty (np.ndarray): Uncertainty of the running average
        """

        return self.get_average_over_components(["11", "22", "33"])
    

    def get_anisotropic_average(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculates the anisotropic average of the transport tensor across all replicas

        Returns:
            time (np.ndarray): Times corresponding to the values
            average (np.ndarray): Isotropic running average
            uncertainty (np.ndarray): Uncertainty of the running average
        """

        return self.get_average_over_components(["12", "13", "23"])




