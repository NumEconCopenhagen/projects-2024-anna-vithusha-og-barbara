from types import SimpleNamespace
import numpy as np

class ExchangeEconomyClass:

    def __init__(self):

        par = self.par = SimpleNamespace()

        # a. preferences
        par.alpha = 1/3
        par.beta = 2/3

        # b. endowments
        par.w1A = 0.8
        par.w2A = 0.3

    def utility_A(self,x1A,x2A):
        par = self.par

        return x1A**par.alpha*x2A**(1-par.alpha)

    def utility_B(self,x1B,x2B):
        par = self.par

        return x1B**par.beta*x2B**(1-par.beta)

    def demand_A(self,p1):
        par = self.par

        x1A = par.alpha*(p1*par.w1A + par.w2A)/p1
        x2A = (1-par.alpha)*(p1*par.w1A + par.w2A)

        return x1A, x2A

    def demand_B(self,p1):
        par = self.par

        x1B = par.beta*(p1*(1-par.w1A) + (1-par.w2A))/p1
        x2B = (1-par.beta)*(p1*(1-par.w1A) + (1-par.w2A))

        return x1B, x2B

    def check_market_clearing(self,p1):

        par = self.par

        x1A,x2A = self.demand_A(p1)
        x1B,x2B = self.demand_B(p1)

        eps1 = x1A-par.w1A + x1B-(1-par.w1A)
        eps2 = x2A-par.w2A + x2B-(1-par.w2A)

        return eps1,eps2
    
    def solve_discrete(self):

        par = self.par

        x1A = np.linspace(0, 1, 75)
        x2A = np.linspace(0, 1, 75)

        x1a_vec =[]
        x2a_vec =[]

        for x1a in x1A:
            for x2a in x2A:

                x1b = 1 - x1a
                x2b = 1 - x2a

                if self.utility_A(x1a, x2a) >= self.utility_A(par.w1A, par.w2A) and self.utility_B(x1b, x2b) >= self.utility_B(1-par.w1A, 1-par.w2A):
                    x1a_vec.append(x1a)
                    x2a_vec.append(x2a)

        return x1a_vec, x2a_vec

                    



