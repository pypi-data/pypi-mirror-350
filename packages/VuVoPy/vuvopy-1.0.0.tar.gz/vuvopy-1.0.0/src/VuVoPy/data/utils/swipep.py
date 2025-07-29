import numpy as np
import math as m
import sympy as sym 
from scipy.signal import spectrogram
from scipy.interpolate import CubicSpline

def swipep(x,fs,plim,hop_size,dlog2p,dERBs,sTHR):
    """
     Perform the SWIPE' (Sawtooth Waveform Inspired Pitch Estimator) algorithm 
     for pitch estimation in a given audio signal.
     Parameters:
     -----------
     x : ndarray
         Input audio signal (1D array).
     fs : float
         Sampling frequency of the audio signal (in Hz).
     plim : tuple
         Pitch range as a tuple (min_pitch, max_pitch) in Hz.
     hop_size : float
         Hop size for analysis (in samples).
     dlog2p : float
         Step size for pitch candidates in log2 scale.
     dERBs : float
         Step size for Equivalent Rectangular Bandwidth (ERB) spaced frequencies.
     sTHR : float
         Threshold for pitch strength to consider a valid pitch.
     Returns:
     --------
     p : ndarray
         Estimated pitch values (in Hz) for each time frame.
     t : ndarray
         Time vector corresponding to the pitch estimates (in seconds).
     s : ndarray
         Pitch strength values for each time frame.
     Notes:
     ------
     - The function uses a multi-resolution analysis approach to estimate pitch.
     - It computes pitch candidates, their strengths, and refines the pitch 
       estimates using parabolic interpolation.
     - The algorithm is robust to noise and works well for a wide range of 
       pitch frequencies.
    """
    
    dt = hop_size / fs  # Time step for analysis (seconds)
    t =np.arange( 0, len(x)/fs, dt)# time vektor
    dc = 4 #Hop size 
    K = 2 #Parameter for size window

    #Define pitch candidates
    log2pc = np.arange(np.log2(plim[0]), np.log2(plim[1]), dlog2p).reshape(-1, 1) 
    pc = 2 ** log2pc
    S = np.zeros((len(pc),len(t))) # Pitch candidate strenght matrix

    # Determine P2 - WSs
    divFS = [fs / x for x in plim] #variable so I can divide by list
    logWs = [round(m.log2(4 * K * df)) for df in divFS]
    #ws_arg =  np.arange(logWs[0], logWs[1], -1)
    ws = 2**  np.arange(logWs[0], logWs[1], -1)
    pO = 4 * K * fs / ws

    # Determine window sizes used by each pitch candidate
    d =  1 + log2pc - m.log2(4*K*fs/ws[0])
    # Create ERBs spaced frequencies (in Hertz)
    fERBs = erbs2hz(np.arange(hz2erbs(pc[0]/4), hz2erbs(fs/2),dERBs))[:,np.newaxis]

    for i in range(len(ws)):
        dn = round(dc * fs / pO[i]) #Hop size in samples
        # Zero pad signal
        xzp = np.concatenate([np.zeros((ws[i]//2,)), x.flatten(), np.zeros((dn + ws[i]//2,))])
        # Compute spectrum
        w = np.hanning(ws[i]) # Hanning window
        o = max(0, round(ws[i] - dn))
        f, ti, X = spectrogram(xzp, fs=fs, window=w, nperseg=ws[i], noverlap=o, mode='complex') 
        # Interpolate at eqidistant ERBs steps
        # Perform interpolation
        # TO DO: ferb je hodnota musim posilat poradi prvku v liste 
        interp_func = CubicSpline(f, np.abs(X), extrapolate=False)
        # Calculate the interpolated magnitudes
        M = np.maximum(0, interp_func(fERBs) )  # Ensure non-negative values
        M = np.squeeze(M)# 

        L = [np.sqrt(ms) for ms in M]# Loudness
        # Select candidates that use this window size 
        # Loop over window 
        # Select candidates that use this window size
        if i == len(ws) - 1:
             j = np.where(d - i > -1)[0]
             k = np.where(d[j] - i < 0)[0]
        elif i == 0:
             j = np.where(d - i < 1)[0]
             k = np.where(d[j] - i > 0)[0]
        else:
             j = np.where(np.abs(d - i) < 1)[0]
             k = np.arange(len(j))   

        Si = pitchStrengthAllCandidates(fERBs, L, pc[j])
         # Pitch strength for selected candidates
        # Interpolate at desired times
        if Si.shape[1] > 1:
           Si = np.nan_to_num(Si, nan=0.0, posinf=0.0, neginf=0.0)
           interp_func = CubicSpline(ti, Si.T, extrapolate = False)
           #Si = [interp_func(i) for i in t]
           Si = interp_func(t) 
        else:
           Si = np.full((len(Si), len(t)), np.nan)
        # Calculate lambda and mu for weighting
        lambda_ = d[j[k]] - i
        mu = np.ones(j.shape).T
        mu[k] = 1 - np.abs(lambda_.T)
        # Update pitch strength matrix
        S[j, :] += np.outer(mu, np.ones(Si.T.shape[1])) * Si.T
        #S[j, :] += (mu * Si.T).T
    # Initialize pitch and strength ys with NaN
    p = np.full((S.shape[1], 1), np.nan)
    s = np.full((S.shape[1], 1), np.nan)

    # Loop over each time frame
    for j in range(S.shape[1]):
        # Find the maximum strength and its index
        s[j], i = np.max(S[:, j]), np.argmax(S[:, j])
    
        # Skip if the strength is below the threshold
        if s[j] < sTHR:
            continue
        # Handle boundary cases
        if i == 0 or i == len(pc) - 1:
            p[j] = pc[0]
        else:
             # Use neighboring points for interpolation
            I = np.arange(i-1, i+2)  # Indices for 3-point interpolation
            tc = 1.0 / pc[I]  # Convert pitch candidates to periods
            ntc = (tc / tc[1] - 1) * 2 * np.pi  # Normalize periods
            # Perform parabolic interpolation using polyfit
            c = np.polyfit(np.squeeze(ntc), S[I, j], 2)
            # Generate fine-tuned frequency candidates for interpolation
            ftc = 1.0 / 2.0**np.arange(np.log2(pc[I[0]]), np.log2(pc[I[2]]) + 1/12/64, 1/12/64)
            nftc = (ftc / tc[1] - 1) * 2 * np.pi  # Normalize fine-tuned candidates Use the interpolated polynomial to find the fine-tuned maximum
            s[j], k = np.max(np.polyval(c, nftc)), np.argmax(np.polyval(c, nftc))
            # Convert the fine-tuned result back to pitch
            p[j] = 2 ** (np.log2(pc[I[0]]) + (k - 1) / (12 * 64))
    return p, t, s

def pitchStrengthAllCandidates(f,L,pc):

    """
    Calculate the pitch strength for all candidates.

    Parameters:
    f  -- Frequency y
    L  -- Loudness y
    pc -- Pitch candidates

    Returns:
    S  -- Pitch salience matrix
    """
    with np.errstate(divide= 'ignore', invalid = 'ignore'):
        L =  np.array(L)
        L = L / np.sqrt(np.sum(L ** 2, axis = 0, keepdims = True))
    #Create pitch salience matrix
    S = np.zeros((len(pc), L.shape[1]))
    for j in range(len(pc)):
        S[j,:] = pitchStrengthOneCandidate(f, L, pc[j])
    return S

def  pitchStrengthOneCandidate(f,L,pc):
    """
    Calculate the pitch strength for one pitch candidate.

    Parameters:
    f  -- Frequency y
    L  -- Loudness y
    pc -- Pitch candidate

    Returns:
    S  -- Pitch strength for this candidate
    """
    n = int(np.fix(f[-1]/pc - 0.75)) # Number of harmonics
    k = np.zeros(f.shape) # Kernel
    q = f / pc #Normalize frequency  w.r.t candidate

    for i in [1] + list(sym.primerange(n)):
        a = np.abs(q-i)
        p = a < 0.25 #Peaks weights
        k[p] = np.cos(2*np.pi * q[p]) /2

    k = k * np.sqrt(1. /f) # Aplly envelope
    k = k / np.linalg.norm(k[k > 0]) # K+-normalize kernel

    S = np.dot(k.T, L)

    return S

def hz2erbs(hz):
    """Convert frequency in Hz to ERBs."""
    return 21.4* np.log10(1+ hz / 229)

def erbs2hz(erbs):
    """Convert ERBs to frequency in Hz."""
    return (10** (erbs / 21.4)-1) * 229
