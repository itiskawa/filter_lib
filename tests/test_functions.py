import functions as f

from matplotlib import pyplot as plt
import numpy as np



def sine_test():
    x = np.linspace(-np.pi, np.pi, 401)
    sine = np.sin(x)
    
    print(sine.shape)
    noise = np.random.normal(0, .02, 401)

    noisy_sine = noise + sine
    plt.plot(x, sine, color='blue', label='original')
    plt.plot(x, noisy_sine, color='r', label='noisy')
    #plt.show()


    corrected = f.fourier_filter(noisy_sine, 400)
    plt.plot(x[:corrected.shape[0]], corrected, color='yellow', label='corrected')
    plt.legend()
    plt.show()
    plt.close()


sine_test()