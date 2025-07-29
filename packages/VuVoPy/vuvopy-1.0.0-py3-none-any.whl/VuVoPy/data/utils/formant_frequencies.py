import numpy as np
import librosa as lb
import matplotlib.pyplot as plt
from VuVoPy.data.containers.prepocessing import Preprocessed     
from VuVoPy.data.containers.sample import VoiceSample
from VuVoPy.data.containers.segmentation import Segmented


class FormantFrequencies(Segmented):
    """
    FormantFrequencies is a class for extracting and managing formant frequencies from segmented voice data.
    Formants are resonant frequencies of the vocal tract, and this class provides methods to calculate and retrieve
    formant frequencies from raw, pre-emphasized, and normalized voice segments.
    Attributes:
        formants (numpy.ndarray): A 3D array containing formant frequencies for raw, pre-emphasized, and normalized
                                  voice segments. The shape is (N, 3, 3), where N is the number of segments, and the
                                  second and third dimensions correspond to the first three formants (F1, F2, F3) and
                                  the type of segment (raw, pre-emphasized, normalized), respectively.
    Methods:
        __init__(fs, formants):
            Initializes the FormantFrequencies object with a sampling rate and formant frequencies.
        from_voice_sample(segments):
            Class method to create an instance of FormantFrequencies by extracting formant frequencies from
            segmented voice data.
        get_formants():
            Returns the numpy array of formants extracted from the raw waveform.
        get_formants_preem():
            Returns the numpy array of formants extracted from the pre-emphasized waveform.
        get_formants_norm():
            Returns the numpy array of formants extracted from the normalized waveform.
        get_sampling_rate():
            Returns the sampling rate of the voice data.
    """
    def __init__(self, fs, formants):
        super().__init__(None, fs, None, None, None, None, None, None, None)
        self.formants = formants
    @classmethod
    def from_voice_sample(cls, segments):
        """
        Creates an instance of the class from a voice sample by extracting formant frequencies.
        Args:
            cls: The class itself, used to create an instance.
            segments: An object containing segmented voice data with methods to retrieve
                      raw, pre-emphasized, and normalized segments, as well as the sampling rate.
        Returns:
            An instance of the class initialized with the sampling rate and extracted formant frequencies.
        Notes:
            - The method calculates LPC coefficients for raw, pre-emphasized, and normalized segments.
            - Formant frequencies are derived from the roots of the LPC polynomial.
            - Only roots with non-negative imaginary parts are considered.
            - The method currently extracts and sorts the first three formants for each segment.
            - The bandwidths of the formants are not calculated at this stage.
        """
        seg_x = segments.get_segment() 
        seg_x_preem = segments.get_preem_segment()
        seg_x_norm = segments.get_norm_segment()
        fs = segments.get_sampling_rate() 
        
        order = int(np.fix(fs/1000 +2))

        lpc_coeff_x = lb.lpc(seg_x, order=order)
        lpc_coeff_x_prem = lb.lpc(seg_x_preem ,order=order)
        lpc_coeff_x_norm = lb.lpc(seg_x_norm, order=order)
        
        N = lpc_coeff_x.shape[0]

        formants = np.zeros((N,3,3))
        rts_x = np.zeros((N,3))
        rts_x_preem = np.zeros((N,3))
        rts_x_norm= np.zeros((N,3))
        
        for i in range(N):
            #Findiung roots of nominator of transfer function
            rts_x = np.roots(lpc_coeff_x[i,:])
            rts_x_preem = np.roots(lpc_coeff_x_prem[i,:])
            rts_x_norm = np.roots(lpc_coeff_x_norm[i,:])
            
            #Finding non-zero Im{Z} >=0
            rts_x = rts_x[(np.imag(rts_x)>0 )].copy()
            rts_x_preem = rts_x_preem[(np.imag(rts_x_preem)>0 )].copy()
            rts_x_norm = rts_x_norm[(np.imag(rts_x_norm)>0 )].copy()

            #Finding formants
            tempF_x = np.arctan2(np.imag(rts_x),np.real(rts_x))
            tempF_x_preem = np.arctan2(np.imag(rts_x_preem),np.real(rts_x_preem))
            tempF_x_norm = np.arctan2(np.imag(rts_x_norm),np.real(rts_x_norm))

            #Sorting formants
            sort_F = sorted(tempF_x)
            sort_F_preem = sorted(tempF_x_preem)
            sort_F_norm = sorted(tempF_x_norm)
            
            if sort_F == []:    
                sort_F = np.zeros(3)
                sort_F_preem = np.zeros(3)
                sort_F_norm = np.zeros(3)

            formants[i, 0, 0] = np.real(sort_F[0]) * (fs / (2 * np.pi))  # F1   
            formants[i, 1, 0] = np.real(sort_F[1]) * (fs / (2 * np.pi))
            formants[i, 2, 0] = np.real(sort_F[2]) * (fs / (2 * np.pi)) # F3
            
            
            formants[i, 0, 1] = np.real(sort_F_preem[0]) * (fs / (2 * np.pi))  # F1   
            formants[i, 1, 1] = np.real(sort_F_preem[1]) * (fs / (2 * np.pi))
            formants[i, 2, 1] = np.real(sort_F_preem[2]) * (fs / (2 * np.pi)) # F3
            
            formants[i, 0, 2] = np.real(sort_F_norm[0]) * (fs / (2 * np.pi))  # F1   
            formants[i, 1, 2] = np.real(sort_F_norm[1]) * (fs / (2 * np.pi))
            formants[i, 2, 2] = np.real(sort_F_norm[2]) * (fs / (2 * np.pi)) # F3
            formants = formants.copy()
        return cls(fs, formants)
        
    def get_formants(self):
        """Return the numpy array of formants extracted from raw waveform"""
        return self.formants[:,:,0]

    def get_formants_preem(self):
        """Return the numpy array of formants extracted from pre-emphasis waveform"""
        return self.formants[:,:,1]
    
    
    def get_formants_norm(self):
        """Return the numpy array of formants extracted from normalized waveform"""
        return self.formants[:,:,2]
    
    def get_sampling_rate(self):
        """Return the sampling rate."""
        return self.fs
