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

        # tolerence

        par.eps = 1e-8
        par.maxiter = 1000
        par.kappa = 0.1

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

                    
    def find_equilibrium(self,p1_guess,p2, w1A, w2A):
            
            par = self.par

            par.w1A = w1A
            par.w2A = w2A
            
            t = 0
            p1 = p1_guess
            
            # using a while loop as we don't know number of iterations a priori
            while True:

                # a. step 1: excess demand
                Z1 = self.check_market_clearing(p1)[0]
                
                # b: step 2: stop?
                if  np.abs(Z1) < par.eps or t >= par.maxiter:
                    print(f'{t:3d}: p1 = {p1:12.8f} -> excess demand -> {Z1:14.8f}')
                    break    
                
                # d. step 3: update p1
                p1 = p1 + par.kappa*Z1/2
                
                # e. step 4: update counter and return to step 1
                t += 1    


            # Check if solution is found 
            if np.abs(Z1) < par.eps:
                # Store equilibrium prices
                self.p1_star = p1 

                # Store equilibrium excess demand 
                self.Z1 = Z1
                self.Z2 = self.check_market_clearing(self.p1_star)[1]

                # Make sure that Walras' law is satisfied
                if not np.abs(self.Z2)<par.eps:
                    print('The market for good 2 was not cleared')
                    print(f'Z2 = {self.Z2}')

            else:
                print('Solution was not found')


    def print_solution(self):

        text = 'Solution to market equilibrium:\n'
        text += f'p1 = {self.p1_star:5.3f}\n\n\n'

        text += 'The allocations are:\n'
        text += f'(x1A, x2A) = ({self.demand_A(self.p1_star)})\n'
        text += f'(x1B, x2B) = ({self.demand_B(self.p1_star)})\n'
        print(text)

        return self.demand_A(self.p1_star)


