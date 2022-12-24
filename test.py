import numpy as np
import matplotlib.pyplot as plt
import scipy as sci

release_time = 1
time = 5 + release_time
sr = 44100
nb_samples = time*sr
samples = np.zeros(time*sr)


x = np.linspace(0, time, nb_samples)

def ADSR(x, a, d, s, r, show_plot = False):
    '''Function to generate an ADSR enveloppe on data x'''
    if True: #x[-1] >= (a + d + r): In the future could possibly make this quicker by checking if signal is shorter then a,d,r
        attack = lambda x: x/a
        decay = lambda x: (a + d - a*s)/d - x*(1-s)/d
        sustain = lambda x: s
        pre_rel_x = x[x < (x[-1] - r)]
        pre_rel = np.piecewise(
            pre_rel_x, 
            [pre_rel_x < a, np.logical_and(a <= pre_rel_x, pre_rel_x < a+d), a+d<=pre_rel_x],
            [attack, decay, sustain]
        )

        plt.plot(pre_rel)
        plt.show()

        release = x[-1]*pre_rel[-1]/r - pre_rel[-1]/r*x[x[-1] - r <= x]

        if show_plot == True:
            plt.plot(np.concatenate((pre_rel, release)))
            plt.show()

        return np.concatenate((pre_rel, release))

    attack = x[x<a]/a
    decay = (a + d - a*s)/d - x[np.logical_and(a <= x, x < a+d)]*(1-s)/d
    sustain = s + 0*x[np.logical_and(a+d <= x, x < x[-1]-r)]
    release = x[-1]*s/r - s/r*x[x[-1] - r <= x]

    return np.concatenate((attack, decay, sustain, release))

    


adsr = ADSR(x, 4.8, 0.5, 0.5, release_time)

plt.plot(x, adsr)
plt.show()

