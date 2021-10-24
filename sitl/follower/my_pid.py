import numpy as np
import time

def calc_lowpass(dt, cutoff_freq):
    if cutoff_freq <= 0.0:
        return 1.0
    rc = 1.0/(2*np.pi*cutoff_freq)
    return dt/(dt+rc)


def constrain(val, limit):
    if val > limit:
        return limit
    if val < -limit:
        return -limit
    return val
class PID:
    def __init__(
        self,
        kp=0.0,
        ki=0.0,
        ki_max=0.0,
        kd=0.0,
        kff=0.0,
        filt_E_hz=0.0,
        filt_D_hz=0.0
    ):
        self.kp = kp
        self.ki = ki
        self.ki_max = ki_max
        self.kd = kd
        self.kff = kff
        self.filt_E_hz = filt_E_hz
        self.filt_D_hz = filt_D_hz
        self.reset = True

    def __call__(self, measurment,  target=0.0, dt=0.0):
        self.target = target
        if self.reset == True:
            self.reset = False
            self.integrator = 0.0
            self.error = target-measurment
            self.derivative = 0.0
            if dt <= 0.0:
                self.last_time = time.monotonic()
                dt = 0.0
        else:
            if dt <= 0:
                now = time.monotonic()
                dt = self.last_time-now
                self.last_time = now
            error_last = self.error
            self.error += calc_lowpass(dt, self.filt_E_hz) * \
                (self.target-measurment-self.error)
            derivative = (self.error-error_last)/dt
            self.derivative += calc_lowpass(dt,
                                            self.filt_D_hz)*(derivative-self.derivative)
            self.integrator += self.error*dt*self.ki
            self.integrator = constrain(self.integrator, self.ki_max)
        return self.error*self.kp+self.integrator+self.derivative*self.kd+self.target*self.kff

    def __repr__(self):
        return (
            '{self.__class__.__name__}('
            'kp={self.kp!r}, ki={self.ki!r}, ki_max={self.ki_max!r}, kd={self.kd!r}, kff={self.kff!r}, '
            'error_filer_HZ={self.filt_E_hz!r}, derivative_filter_HZ={self.filt_D_hz!r}'
            ')'
        ).format(self=self)
