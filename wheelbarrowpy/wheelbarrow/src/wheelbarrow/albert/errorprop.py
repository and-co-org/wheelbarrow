import math

from mpmath import mp, mpf # pip install mpmath

mp.dps = 4

class ErroredValue(object):
    def __init__(self, value, delta=0, percent_err=None, abs_err=None):
        if isinstance(value, list): # compute mean and std from list
            from statistics import stdev
            values = list(value)     # optm: stream
            self.value = mpf(sum(values) / len(values))
            self.delta = mpf(stdev(values))
        else:   # given mean and std
            self.value = mpf(value)

            if type(percent_err) in [float, int, str]:
                print('percent err!')
                self.delta = mpf(value) * percent_err * 0.01
            elif type(abs_err) in [float, int, str]:
                print('abs err! std-ify')
                self.delta = (mpf(abs_err)/6)**0.5
            else:
                self.delta = mpf(delta)

    def __add__(self, o):
        if type(o) != ErroredValue:
            o = ErroredValue(o)
        return ErroredValue((self.value+o.value), (((self.delta**2) + (o.delta**2))**0.5))

    def __radd__(self, o):
        return ErroredValue((o+self.value), (((self.delta**2) + 0)**0.5))

    def __radd__(self, o):
        return ErroredValue((o+self.value), (((self.delta**2) + 0)**0.5))

    def __sub__(self, o):
        if o is self: return ErroredValue(0)
        if type(o) != ErroredValue:
            o = ErroredValue(o)
        return ErroredValue((self.value-o.value), (((self.delta**2) + (o.delta**2))**0.5))

    def __rsub__(self, o):
        return ErroredValue((o-self.value), (((self.delta**2) + 0)**0.5))

    def __rsub__(self, o):
        return ErroredValue((o-self.value), (((self.delta**2) + 0)**0.5))

    def __mul__(self, o):
        if type(o) != ErroredValue:
            o = ErroredValue(o)
        return ErroredValue((self.value*o.value), (self.value*o.value)*(((self.delta/self.value)**2 + (o.delta/o.value)**2)**0.5))

    def __rmul__(self, o):
        return ErroredValue((o*self.value), (o*self.value)*(((self.delta/self.value)**2 + 0)**0.5))
      
    def __truediv__(self, o):
        if self is o: return ErroredValue(1)
        if type(o) != ErroredValue:
            o = ErroredValue(o)
        return ErroredValue((self.value/o.value), (self.value/o.value)*(((self.delta/self.value)**2 + (o.delta/o.value)**2)**0.5))

    def __rtruediv__(self,o):
        return ErroredValue(o) / self

    # https://physics.stackexchange.com/questions/411879/how-to-calculate-the-percentage-error-of-ex-if-percentage-error-in-measuring
    def __rpow__(self, a):
        return ErroredValue(a**(self.value), (0.5**self.value)*math.log(a, math.e)*self.delta)

    def __pow__(self, p):
        return ErroredValue(self.value**p, abs(self.value**p) * (self.delta / abs(self.value)))

    def __str__(self):
        return f'{self.value} ± {self.delta} ({float(self.delta/self.value * 100):.2f}%)'

    def __repr__(self):
        return f'<ErroredValue {self.value}±{self.delta} at {hex(id(self))}>'

    @property
    def percentDelta(self):
        return self.delta/self.value

    @staticmethod
    def ln(a):
        return ErroredValue(math.log(a.value, math.e), ((a.delta)/a.value))

