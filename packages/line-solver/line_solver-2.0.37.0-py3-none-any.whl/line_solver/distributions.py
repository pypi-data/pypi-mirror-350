import sys

import jpype
import jpype.imports

from line_solver import jlineMatrixFromArray, jlineMatrixToArray

"""
Defines classes that wrap around distribution-related functionality provided by JLINE.
"""

# Utility class to represnet named parameters for distributions
class NamedParam:
    def __init__(self, *args):
        if len(args) == 1:
            self.obj = args[0]
        else:
            self.name = args[0]
            self.value = args[1]

    def getName(self):
        return self.name

    def getValue(self):
        return self.value

# Base class for all distributions
class Distribution:
    def __init__(self):
        pass

    def evalCDF(self, x):
        return self.obj.evalCDF(x)

    def evalLST(self, x):
        return self.obj.evalLST(x)

    def getName(self):
        return self.obj.getName()

    def getParam(self, id):
        nparam = NamedParam(self.obj.getParam(id))
        return nparam

    def getMean(self):
        return self.obj.getMean()

    def getRate(self):
        return self.obj.getRate()

    def getSCV(self):
        return self.obj.getSCV()

    def getVar(self):
        return self.obj.getVar()

    def getSkew(self):
        return self.obj.getSkew()

    def getSupport(self):
        return self.obj.getSupport()

    def isContinuous(self):
        return self.obj.isContinuous()

    def isDisabled(self):
        return self.obj.isDisabled()

    def isDiscrete(self):
        return self.obj.isDiscrete()

    def isImmediate(self):
        return self.obj.isImmediate()

    def sample(self, *args):
        if len(args) == 1:
            n = args[0]
            return jlineMatrixToArray(self.obj.isImmediate())
        else:
            n = args[0]
            seed = args[1]

# Subclass for continuous distributions
class ContinuousDistribution(Distribution):
    def __init__(self):
        super().__init__()

# Subclass for discrete distributions
class DiscreteDistribution(Distribution):
    def __init__(self):
        super().__init__()

# Subclass for Markovian distributions
class MarkovianDistribution(Distribution):
    def __init__(self):
        super().__init__()

    def getD0(self):
        return self.obj.getD0()

    def getD1(self):
        return self.obj.getD1()

    def getMu(self):
        return self.obj.getMu()

    def getNumberOfPhases(self):
        return self.obj.getNumberOfPhases()

    def getPH(self):
        return self.obj.getPH()

    def getPhi(self):
        return self.obj.getPhi()

    def getRepres(self):
        return self.obj.getRepres()


class APH(MarkovianDistribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            self.obj = args[0]
        else:
            alpha = args[0]
            subgen = args[1]
            self.obj = jpype.JPackage('jline').lang.processes.APH(jlineMatrixFromArray(alpha),
                                                                      jlineMatrixFromArray(subgen))

class Bernoulli(DiscreteDistribution):
    def __init__(self, *args):
        super().__init__()
        prob = args[0]
        self.obj = jpype.JPackage('jline').lang.processes.Bernoulli(prob)

class Binomial(DiscreteDistribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            self.obj = args[0]
        else:
            prob = args[0]
            n = args[1]
            self.obj = jpype.JPackage('jline').lang.processes.Binomial(prob, n)

class Coxian(MarkovianDistribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            self.obj = args[0]
        else:
            mu = args[0]
            phi = args[1]
            if phi[len(phi)-1] != 1.0:
                print("Invalid Coxian exit probabilities. The last element must be 1.0.", file=sys.stderr)
            elif max(phi) > 1.0 or min(phi) < 0.0:
                print("Invalid Coxian exit probabilities. Some values are not in [0,1].", file=sys.stderr)
            else:
                self.obj = jpype.JPackage('jline').lang.processes.Coxian(jlineMatrixFromArray(mu), jlineMatrixFromArray(phi))

    def fitMeanAndSCV(mean, scv):
        return Cox2(jpype.JPackage('jline').lang.processes.Cox2.fitMeanAndSCV(mean, scv))

class Cox2(MarkovianDistribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            self.obj = args[0]
        else:
            mu1 = args[0]
            mu2 = args[1]
            phi1 = args[2]
            self.obj = jpype.JPackage('jline').lang.processes.Cox2(mu1, mu2, phi1)

    def fitMeanAndSCV(mean, scv):
        return Cox2(jpype.JPackage('jline').lang.processes.Cox2.fitMeanAndSCV(mean, scv))


class Det(Distribution):
    def __init__(self, value):
        super().__init__()
        self.obj = jpype.JPackage('jline').lang.processes.Det(value)


class Disabled(Distribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            self.obj = jpype.JPackage('jline').lang.processes.Disabled()
        else:
            self.obj = args[0]

    @staticmethod
    def getInstance():
        return Disabled(jpype.JPackage('jline').lang.processes.Disabled.getInstance())

class DiscreteSampler(DiscreteDistribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            if isinstance(args[0], DiscreteDistribution):
                self.obj = args[0]
            else:
                p = args[0]
                self.obj = jpype.JPackage('jline').lang.processes.DiscreteSampler(p)
        else:
            p = args[0]
            x = args[1]
            self.obj = jpype.JPackage('jline').lang.processes.DiscreteSampler(p, x)

class DiscreteUniform(DiscreteDistribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            self.obj = args[0]
        else:
            minVal = args[0]  # min
            maxVal = args[1]  # max
            self.obj = Uniform.JPackage('jline').lang.processes.DiscreteUniform(minVal, maxVal)

class Exp(MarkovianDistribution):
    def __init__(self, rate):
        super().__init__()
        self.obj = jpype.JPackage('jline').lang.processes.Exp(rate)

    def fitMean(mean):
        return Erlang(jpype.JPackage('jline').lang.processes.Exp.fitMean(mean))


class Erlang(MarkovianDistribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            self.obj = args[0]
        else:
            rate = args[0]
            nphases = args[1]
            self.obj = jpype.JPackage('jline').lang.processes.Erlang(rate, nphases)

    def fitMeanAndSCV(mean, scv):
        return Erlang(jpype.JPackage('jline').lang.processes.Erlang.fitMeanAndSCV(mean, scv))

    def fitMeanAndOrder(mean, order):
        return Erlang(jpype.JPackage('jline').lang.processes.Erlang.fitMeanAndOrder(mean, order))


class Gamma(ContinuousDistribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            self.obj = args[0]
        else:
            shape = args[0]
            scale = args[1]
            self.obj = jpype.JPackage('jline').lang.processes.Gamma(shape, scale)

    def fitMeanAndSCV(mean, scv):
        return Gamma(jpype.JPackage('jline').lang.processes.Gamma.fitMeanAndSCV(mean, scv))


class Geometric(DiscreteDistribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            if isinstance(args[0], jpype.JPackage('jline').lang.processes.DiscreteDistribution):
                self.obj = args[0]
            else:
                prob = args[0]
                self.obj = jpype.JPackage('jline').lang.processes.Geometric(prob)


class HyperExp(MarkovianDistribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            self.obj = args[0]
        else:
            p = args[0]
            lambda1 = args[1]
            lambda2 = args[2]
            self.obj = jpype.JPackage('jline').lang.processes.HyperExp(p, lambda1, lambda2)

    def fitMeanAndSCV(mean, scv):
        return HyperExp(jpype.JPackage('jline').lang.processes.HyperExp.fitMeanAndSCV(mean, scv))

    def fitMeanAndSCVBalanced(mean, scv):
        return HyperExp(jpype.JPackage('jline').lang.processes.HyperExp.fitMeanAndSCVBalanced(mean, scv))


class Immediate(Distribution):
    def __init__(self):
        super().__init__()
        self.obj = jpype.JPackage('jline').lang.processes.Immediate()


class Lognormal(ContinuousDistribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            self.obj = args[0]
        else:
            mu = args[0]
            sigma = args[1]
            self.obj = jpype.JPackage('jline').lang.processes.Lognormal(mu, sigma)

    def fitMeanAndSCV(mean, scv):
        return Lognormal(jpype.JPackage('jline').lang.processes.Lognormal.fitMeanAndSCV(mean, scv))


class MAP(MarkovianDistribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            self.obj = args[0]
        else:
            D0 = args[0]
            D1 = args[1]
            self.obj = jpype.JPackage('jline').lang.processes.MAP(jlineMatrixFromArray(D0), jlineMatrixFromArray(D1))

    def toPH(self):
        self.obj.toPH()


class PH(MarkovianDistribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            self.obj = args[0]
        else:
            # Takes a probability vector
            alpha = args[0]
            # Takes a subgenerator matrix
            subgen = args[1]
            # Generates a phase-type distribution
            self.obj = jpype.JPackage('jline').lang.processes.PH(jlineMatrixFromArray(alpha),
                                                                     jlineMatrixFromArray(subgen))


class Pareto(ContinuousDistribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            self.obj = args[0]
        else:
            shape = args[0]
            scale = args[1]
            self.obj = jpype.JPackage('jline').lang.processes.Pareto(shape, scale)

    def fitMeanAndSCV(mean, scv):
        return Pareto(jpype.JPackage('jline').lang.processes.Pareto.fitMeanAndSCV(mean, scv))


class Poisson(DiscreteDistribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            self.obj = args[0]
        else:
            rate = args[0]
            self.obj = jpype.JPackage('jline').lang.processes.Geometric(rate)


class Replayer(Distribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            if isinstance(args[0], Distribution):
                self.obj = args[0]
            else:
                filename = args[0]
                self.obj = jpype.JPackage('jline').lang.processes.Replayer(filename)

    def fitAPH(self):
        return APH(self.obj.fitAPH())


class Uniform(ContinuousDistribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            self.obj = args[0]
        else:
            minVal = args[0]  # min
            maxVal = args[1]  # max
            self.obj = Uniform.JPackage('jline').lang.processes.Uniform(minVal, maxVal)


class Weibull(ContinuousDistribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            self.obj = args[0]
        else:
            shape = args[0]
            scale = args[1]
            self.obj = jpype.JPackage('jline').lang.processes.Weibull(shape, scale)

    def fitMeanAndSCV(mean, scv):
        return Weibull(jpype.JPackage('jline').lang.processes.Weibull.fitMeanAndSCV(mean, scv))


class Zipf(DiscreteDistribution):
    def __init__(self, *args):
        super().__init__()
        if len(args) == 1:
            self.obj = args[0]
        else:
            s = args[0]
            n = args[1]
            self.obj = jpype.JPackage('jline').lang.processes.Zipf(s, n)

