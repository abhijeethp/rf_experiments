def config():
    return {
        "frequency": 1960 * 10**6,
        "samplerate": 31 * 10**6,
        "bandwidth": 10 * 10**6,
        "gain": 40,
        "duration_s": 30.0/1000
    }

wavelength = 299792458 / (1960 * 10**6) * 100
L_s = 26.8
L_m = 37.8