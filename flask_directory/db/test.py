class Polynomial:
    def init(self, coef):
        self.coef = coef
 
    def call(self, x):
        return sum([self.coef[i] * x ** i for i in range(len(self.coefficients))])
 
    def add(self, p):
        a = self.coef
        b = p.coef
        if len(a) < len(b):
            a += [0] * (len(b) - len(a))
        else:
            b += [0] * (len(a) - len(b))
        return Polynomial([a[i] + b[i] for i in range(len(a))])