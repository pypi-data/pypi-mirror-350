import numpy as np
import matplotlib.pyplot as plt
from VuVoPy.data.containers.prepocessing import Preprocessed as pp
from VuVoPy.data.containers.sample import VoiceSample as vs
from VuVoPy.data.containers.segmentation import Segmented as sg
from VuVoPy.data.utils.vuvs_detection import Vuvs as vuvs

class VoicedSample(vs):
    """
    VoicedSample is a class that processes and analyzes preprocessed audio data to extract voiced samples 
    and remove silence from the waveform. It also provides functionality to stretch labels to match the 
    signal length.
    Attributes:
        x (numpy.ndarray): The original waveform extracted from the preprocessed data.
        x_preem (numpy.ndarray): The pre-emphasized version of the waveform.
        x_norm (numpy.ndarray): The normalized version of the waveform.
        fs (int): The sampling rate of the audio signal.
        vuvs (object): An object containing voiced/unvoiced labels for the audio signal.
        voiced_sample (numpy.ndarray): The waveform containing only voiced segments.
        silence_removed_sample (numpy.ndarray): The waveform with silence removed.
    Methods:
        get_waveform():
            Returns the silence-removed waveform as a NumPy array.
        label_stretch():
            Stretches the voiced/unvoiced labels to match the length of the audio signal.
        get_voiced_sample():
            Extracts and returns the voiced segments of the waveform based on the stretched labels.
        get_silence_remove_sample():
            Removes silence from the waveform based on the stretched labels and returns the resulting waveform.
        get_sampling_rate():
            Returns the sampling rate of the audio signal.
    """
    def __init__(self, preprocessed, vuvs, fs) :
        self.x = preprocessed.get_waveform()
        self.x_preem = preprocessed.get_preemphasis()
        self.x_norm = preprocessed.get_normalization()
        self.fs = preprocessed.get_sampling_rate()
        self.vuvs = vuvs

        self.voiced_sample = self.get_voiced_sample()
        self.silence_removed_sample = self.get_silence_remove_sample()

    def get_waveform(self):
        """
        Return the silence removed waveform as a NumPy array.
        """
        return self.voiced_sample

    def label_stretch(self):
        """
        Stretches or compresses a sequence of labels to match the length of a target array.
        This function takes a sequence of labels and adjusts their lengths proportionally 
        to match the length of the target array `self.x`. It ensures that the relative 
        proportions of the original label segments are preserved while fixing any rounding 
        errors to exactly match the target length.
        Returns:
            np.ndarray: A stretched or compressed array of labels with the same length as `self.x`.
        """

        labels = self.vuvs.get_vuvs()
        arr = np.asarray(labels)
        target_len = len(self.x)
        # Find segments where values stay the same
        segments = []
        start_idx = 0
        for i in range(1, len(arr)):
           if arr[i] != arr[i - 1]:
              segments.append(arr[start_idx:i])
              start_idx = i
        segments.append(arr[start_idx:])  # Add last segment
        original_lens = np.array([len(seg) for seg in segments])

        # Determine how many samples per segment
        total_original = np.sum(original_lens)
    
        # Calculate how much to stretch each segment
        stretched_lens = np.round((original_lens / total_original) * target_len).astype(int)

        # Fix rounding errors to exactly match target_len
        diff = target_len - np.sum(stretched_lens)
        while diff != 0:
            for i in range(len(stretched_lens)):
               if diff == 0:
                  break
            stretched_lens[i] += 1 if diff > 0 else -1
            diff = target_len - np.sum(stretched_lens)

        # Build the stretched array
        stretched = np.concatenate([np.full(l, seg[0]) for seg, l in zip(segments, stretched_lens)])
        return stretched
    
    def get_voiced_sample(self):
        """
        Extracts and returns the voiced portion of the audio sample.
        This method uses the label information to identify the voiced segments
        in the audio sample. It assumes that the labels are generated such that
        a label value of 2 corresponds to voiced segments.
        Returns:
            numpy.ndarray: A subset of the audio sample containing only the 
            voiced segments.
        """
        
        sample = self.x
        labels = self.label_stretch()
        voiced_sample = sample[labels == 2]
        return voiced_sample

    def get_silence_remove_sample(self):
        """
        Removes segments of silence from the audio sample based on the provided labels.
        This method identifies silent regions in the audio sample `self.x` using the 
        labels generated by the `label_stretch` method. Silent regions are defined as 
        consecutive frames labeled as 0, with a duration greater than or equal to 50 ms. 
        These regions are then removed from the audio sample.
        Returns:
            numpy.ndarray: A modified version of the audio sample `self.x` with silent 
            regions removed.
        """
        
        sample = self.x
        labels = self.label_stretch()
        
        i = 0
        min_frames = int(np.ceil(50 / 1000 * self.fs))
        silence_idx = []

        while i < len(labels):
            if labels[i] == 0:
                start = i
                while i < len(labels) and labels[i] == 0:
                    i += 1
                silence_len = i - start
                if silence_len >= min_frames:
                    silence_idx.append((start, i))
            else:
                i += 1
            mask = np.ones(len(self.x), dtype=bool)
            for start, end in silence_idx:
                mask[start:end] = False
        
        return self.x[mask]
    def get_sampling_rate(self):
        """
        Return the sampling rate.
        """
        return self.fs
    