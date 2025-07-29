import numpy as np
import matplotlib.pyplot as plt
from VuVoPy.data.containers.prepocessing import Preprocessed as pp
from VuVoPy.data.containers.sample import VoiceSample as vs
from VuVoPy.data.containers.segmentation import Segmented as sg
from VuVoPy.data.utils.vuvs_gmm import vuvs_gmm
 
class Vuvs:
    """
    The Vuvs class is designed to analyze voiced, unvoiced, and silence segments in an audio signal. 
    It uses Gaussian Mixture Models (GMM) to compute these segments and provides methods to retrieve 
    various statistics about silence durations and counts.
    Attributes:
        segment (array-like): The original audio segment.
        segment_preem (array-like): The pre-emphasized audio segment.
        segment_norm (array-like): The normalized audio segment.
        fs (int): The sampling rate of the audio signal.
        winlen (int): The length of the analysis window in samples. Default is 512.
        winover (int): The overlap between consecutive windows in samples. Default is 496.
        wintype (str): The type of window to apply (e.g., 'hann'). Default is 'hann'.
        smoothing_window (int): The size of the smoothing window for post-processing. Default is 5.
        vuvs (array-like): The computed voiced/unvoiced/silence segments.
    Methods:
        calculate_vuvs():
            Compute the voiced/unvoiced/silence segments using a GMM-based approach.
        get_vuvs():
            Retrieve the computed voiced/unvoiced/silence segments.
        get_sampling_rate():
            Retrieve the sampling rate of the audio signal.
        get_total_silence_duration(min_silence_duration_ms=50):
            Calculate the total duration (in seconds) of silences longer than a specified threshold.
        get_silence_count(min_silence_duration_ms=50):
            Count the number of silent segments longer than a specified threshold.
        get_silence_durations(min_silence_duration_ms=50):
            Retrieve a list of durations (in seconds) for all silences longer than a specified threshold.
    """
    
    def __init__(self, segment, fs, winlen = 512, winover = 496, wintype = 'hann', smoothing_window=5):
        self.segment = segment.get_segment()
        self.segment_preem = segment.get_preem_segment()
        self.segment_norm = segment.get_norm_segment()
        self.fs = fs
        self.winlen = winlen
        self.winover = winover
        self.wintype = wintype
        self.smoothing_window = smoothing_window

        # Compute vuvs vuvs upon initialization
        self.vuvs = self.calculate_vuvs()
        
    def calculate_vuvs(self):
        """
        Calculate the voiced/unvoiced segments (VUVS) of an audio signal.
        This method uses a Gaussian Mixture Model (GMM) to determine the voiced 
        and unvoiced segments of the audio signal based on the provided parameters.
        Returns:
            list: A list of VUVs detected in the audio signal.
        Notes:
            - The method relies on the `vuvs_gmm` function, which performs the 
              actual VUV detection.
            - The detection process uses the attributes `segment`, `fs`, 
              `winover`, and `smoothing_window` of the class instance.
        """
        
        return vuvs_gmm(self.segment, self.fs, self.winover, self.smoothing_window)

    def get_vuvs(self):
        """Return computed voiced/unvoiced/scilence segments."""
        return self.vuvs

    def get_sampling_rate(self):
        """Return the sampling rate."""
        return self.fs
    
    def get_total_silence_duration(self, min_silence_duration_ms=50):
        """Return total duration (in seconds) of silences longer than the threshold."""
        labels = self.vuvs
        hop_duration = (self.winlen - self.winover) / self.fs
        min_frames = int(np.ceil(min_silence_duration_ms / 1000 / hop_duration))

        total_duration = 0.0
        i = 0
        while i < len(labels):
            if labels[i] == 0:
                start = i
                while i < len(labels) and labels[i] == 0:
                    i += 1
                silence_len = i - start
                if silence_len >= min_frames:
                    total_duration += silence_len * hop_duration
            else:
                i += 1
        return total_duration

    def get_silence_count(self, min_silence_duration_ms=50):
        """Return number of silent segments longer than the threshold."""
        labels = self.vuvs
        hop_duration = (self.winlen - self.winover) / self.fs
        min_frames = int(np.ceil(min_silence_duration_ms / 1000 / hop_duration))

        silence_count = 0
        i = 0
        while i < len(labels):
            if labels[i] == 0:
                start = i
                while i < len(labels) and labels[i] == 0:
                    i += 1
                silence_len = i - start
                if silence_len >= min_frames:
                    silence_count += 1
            else:
                i += 1
        return silence_count

    def get_silence_durations(self, min_silence_duration_ms=50):
        """Return list of durations (in seconds) for all silences longer than the threshold."""
        labels = self.vuvs
        hop_duration = (self.winlen - self.winover) / self.fs
        min_frames = int(np.ceil(min_silence_duration_ms / 1000 / hop_duration))

        durations = []
        i = 0
        while i < len(labels):
            if labels[i] == 0:
                start = i
                while i < len(labels) and labels[i] == 0:
                    i += 1
                silence_len = i - start
                if silence_len >= min_frames:
                    durations.append(silence_len * hop_duration)
            else:
                i += 1
        return durations

    
