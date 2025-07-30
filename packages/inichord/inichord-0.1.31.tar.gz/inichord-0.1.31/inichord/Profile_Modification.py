# import os
# import sys
import numpy as np
# from scipy import ndimage
# from scipy import fftpack, signal

#------------------------------import for pypi lib use-------------------------
import inichord.General_Functions as gf

#------------------------------import for local dev use------------------------
# import General_Functions as gf

import scipy.io.wavfile
from scipy.signal import savgol_filter, filtfilt, butter

from importlib.resources import files
data = files('inichord').joinpath('config.txt').read_text()
if data == "True":
    import cupy as cp

# # Open a file in read-only mode
# with open('config.txt', 'r') as file:
#     line = file.read()  # Lire tout le contenu
#     if line == "True":
#         import cupy as cp


def cyclic(a, axProf):
    '''
    a : TYPE numpy array 2D or Cupy array 2D
        DESCRIPTION : les profils sont rangés en ligne ou en colonne
    axProf : Integer : décrit selon quel axe les profils s'étendent.
    Si une ligne représente un profil, alors il faut mettre axe 1
    Si une colonne représente un profil, alors il faut mettre axe 0
        
    return : un tableau où on a copié la première donnée de chaqueprofil à la fin de chaque profil,
             et donc les profils ont une dimension augmentée de 1
    '''
    if axProf == 1:
        i = 0
        n = len(a[:, 0])
        b = a[:, 0].reshape((n, -1))
        
    elif axProf == 0:
        i = 1
        n = len(a[0, :])
        b = a[0, :].reshape((-1, n))        
    else:
        print("le tableau d'entrée doit être en 2D et l'axe = 0 ou 1")
        quit()
    
    arr = np.concatenate((a, b), axis = axProf)
    return arr

def fft_profil(arr2, axProf): # Useless 
    Var_fft = np.fft.rfft(arr2, axis = axProf) #FFT

    return Var_fft 

def derivee(a, nbderiv, ax = 1, sv = False, wl = 5, po = 2):
    
    if sv:
        return savgol_filter(a, window_length = wl, polyorder = po, deriv = nbderiv, axis = ax)
    else:
        return np.diff(a, nbderiv, axis = ax)  
    

def reshapeProfilesInLine(profiles, size):
    lines = int(profiles.size / size)
    return profiles.reshape(lines, size)

def Butterworth(arr2, axProf, pass_filter, N_order, Wn_order):
    b, a = butter(N_order, Wn_order, pass_filter)
    arrHP = filtfilt(b, a, arr2, axProf)
    
    return arrHP

def downSampleProfiles(profiles, step):
    '''
        Parameters
    ----------
    profile : TYPE numpy array
        DESCRIPTION. c'est le tableau contenant les profils en ligne
    step : TYPE int
        DESCRIPTION c'est le pas de réduction (2, 3, 4...)

    Returns une matrice de profils de longueur réduite rangés en ligne
    -------
    None.

    '''
    if profiles.ndim == 1:
        try:
            profiles = profiles[::step]
            return profiles
        except:
            print("step doit être un entier et diviseur de len(profiles) ; retour des profils intacts")
            return profiles
    
    elif profiles.ndim == 2:
        try:
            profiles = profiles[:, ::step]
            return profiles
        except:
            print("step doit être un entier et diviseur de len(profiles) ; retour des profils intacts")
            return profiles 

def normMatProfiles(matrix, ax = 1):
    norm = np.linalg.norm(matrix, axis = ax, keepdims=True)
    return matrix / norm

def centeredEuclidianNorm(prof, ax = 1):
    '''
    Cette fonction prend un vecteur et retourne un vecteur normalisé centré.
    Signification : on enlève la moyenne et après on le divise par sa norme euclidienne

    Parameters
    ----------
    prof : TYPE numpy array OR cupy array
        DESCRIPTION. vecteur à normaliser-centrer
        Note : la fonction peut prendre une assemblée de profils, d'où l'argument
        ax pour spécifier la dimension le long de laquelle les différents profils sont alignés

    Returns
    -------
    prof : TYPE numpy array
        DESCRIPTION. vecteur normalisé

    '''
           
    if not gf.isCupy(prof):
        mean =np.mean(prof, axis = ax, keepdims=True)
        prof = prof - mean
        del mean
        norm = np.linalg.norm(prof, axis = ax, keepdims=True)
    else:
        mean = cp.mean(prof, axis = ax, keepdims=True)
        prof = prof - mean
        del mean
        norm = cp.linalg.norm(prof, axis = ax, keepdims=True)
   
    
    prof = prof / norm
    return prof

def centeredSTD(prof, ax = 1):
    '''
    Cette fonction prend un vecteur et retourne un vecteur centré et divisé par son écart-type.
    Signification : on enlève la moyenne et après on le divise par l'écart-type'
    Parameters
    ----------
    prof : TYPE numpy array OR cupy array
        DESCRIPTION. vecteur à normaliser-centrer
        Note : la fonction peut prendre une assemblée de profils, d'où l'argument
        ax pour spécifier la dimension le long de laquelle les différents profils sont alignés

    Returns
    -------
    prof : TYPE numpy array
        DESCRIPTION. vecteur normalisé

    '''
           
    if not gf.isCupy(prof):
        mean =np.mean(prof, axis = ax, keepdims=True)
        prof = prof - mean
        del mean
        std = np.std(prof, axis = ax, keepdims=True)
    else:
        mean = cp.mean(prof, axis = ax, keepdims=True)
        prof = prof - mean
        del mean
        std = cp.std(prof, axis = ax, keepdims=True)
   
    prof = prof / std
    return prof

def Profile_modifier(array2D, Workflow, normType, axProf):
    '''
    
    Parameters
    ----------
    array2D : TYPE numpy array 2D or Cupy array 2D
        DESCRIPTION : les profils sont rangés en ligne ou en colonne
    
    Workflow : lisdt of list. Each list containes one modification with its 
    parameters. All modifications are applied one after one.
    
    normtype : string describing the normalization applied to the profiles
        among "centered euclidian" or "euclidian_std"
    
    ax : TYPE integer
        DESCRIPTION : décrit selon quel axe les profils s'étendent.
        Si une ligne représente un profil, alors il faut mettre axe 1
        Si une colonne représente un profil, alors il faut mettre axe 0

    Returns un tableau de même type avec des profils de même dimension, 
        rangés de la même manière et normalisés en euclidien centré
    -------
    None.

    '''
    if normType == "centered euclidian":
        array2D = centeredEuclidianNorm(array2D, ax = axProf)
    elif normType == "centered_std":
        array2D = centeredSTD(array2D, ax = axProf)  
    
    for i in Workflow:
        if i[0] == 'Diff':
            if i[1] != 0:
                
                if len(i) > 2:
                    array2D = derivee(array2D, i[1], ax = axProf, sv = True, wl = i[2])
                else:
                    array2D = cyclic(array2D, axProf)
                    array2D = derivee(array2D, i[1], ax = axProf, sv = False)
                array2D = centeredEuclidianNorm(array2D, ax = axProf)
            
                
        elif i[0] == 'FFT':
            array2D = fft_profil(array2D, axProf)
            # array2D = centeredEuclidianNorm(array2D, ax = axProf)
        elif i[0] == 'Butterworth':
            array2D = Butterworth(array2D, axProf, i[1], i[2], i[3])
            array2D = centeredEuclidianNorm(array2D, ax = axProf)
            
    return array2D 


def FFT_filtering(stack, freq = 1):
    # stack = stack.asarray().astype(np.float64)
    
    freq = int(freq)
    
    h = len(stack[0])
    w = len(stack[0, 1])
    stack_reshape = np.moveaxis(stack, 0, 2)

    img_number = len(stack[:,])
    img_step = int(360/len(stack[:,]))
    stack_filtered = np.zeros((h, w, img_number))
    # stack_background = np.zeros((h, w, img_number))

    for x in range(h):
        for y in range(w):
            sig  = stack_reshape[x,y]
            sample_freq = fftpack.fftfreq(sig.size, d=img_step/360)
            sig_fft = fftpack.fft(sig)

            low_freq_fft = sig_fft.copy()
            high_freq_fft = sig_fft.copy()

            low_freq_fft[np.abs(sample_freq) <= freq] = 0
            high_freq_fft[np.abs(sample_freq) > freq] = 0

            signal_filtered = fftpack.ifft(low_freq_fft)
            # signal_background = fftpack.ifft(high_freq_fft)

            stack_filtered[x,y] = np.real(signal_filtered)
            # stack_background[x,y] = np.real(signal_background)


    stack_filtered = np.moveaxis(stack_filtered, -1, 0)
    stack_filtered = np.asarray(stack_filtered, dtype=np.float32)

    # stack_background = np.moveaxis(stack_background, -1, 0)
    # stack_background= np.asarray(stack_background, dtype=np.float32)
    
    # return stack_filtered,stack_background
    return stack_filtered

def FFT_filtering_prf_InLines(array2D, freq = 1):

    freq = int(freq)
    
    h = len(array2D)
    w = len(array2D[0])
    print('Nbr de point : ' + str(h))
    print('Nbr de profil : ' + str(w))
    # stack_reshape = np.moveaxis(array2D, 0, 2)

    img_number = len(array2D[0])
    print('img number is :' + str(img_number))
    img_step = int(360/img_number)
    print('step is :' + str(img_step))
    stack_filtered = np.zeros((h, w))
    # stack_background = np.zeros((h, w, img_number))

    for x in range(w):
        sig  = array2D[:,x]
        sample_freq = fftpack.fftfreq(sig.size, d=img_step/360)
        # print(sample_freq)
        sig_fft = fftpack.fft(sig)

        low_freq_fft = sig_fft.copy()
        high_freq_fft = sig_fft.copy()

        low_freq_fft[np.abs(sample_freq) <= freq] = 0
        high_freq_fft[np.abs(sample_freq) > freq] = 0

        signal_filtered = fftpack.ifft(low_freq_fft)
        stack_filtered[:,x] = np.real(signal_filtered)

    stack_filtered = np.asarray(stack_filtered, dtype=np.float32)

    return stack_filtered