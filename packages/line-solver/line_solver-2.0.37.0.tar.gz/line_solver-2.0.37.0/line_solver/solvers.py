import os

import jpype
import jpype.imports
import numpy as np
import pandas as pd
from jpype import JArray

from line_solver import VerboseLevel, jlineMatrixToArray, GlobalConstants, jlineMatrixFromArray, \
    jlineMapMatrixToArray
from native.solvers.fluid.solver_fluid_analyzer import solver_fluid_analyzer


# from my_implementations.fluid.solver_fluid import *

# Base class for all solvers
# Used to configure the solver options
class Solver:
    def __init__(self, options, args):
        self.solveropt = options
        if len(args) >= 1:
            ctr = 0
            for ctr in range(len(args)):
                match args[ctr]:
                    case 'cutoff':
                        self.solveropt.obj.cutoff(args[ctr + 1])
                    case 'method':
                        self.solveropt.obj.method(args[ctr + 1]) # to set the method in the Solver object instantiation, one should specify in the args (... "method", "matrix")
                    case 'exact':
                        self.solveropt.obj.method('exact')
                        ctr -= 1
                    case 'keep':
                        self.solveropt.obj.keep(args[ctr + 1])
                    case 'seed':
                        self.solveropt.obj.seed(args[ctr + 1])
                    case 'samples':
                        self.solveropt.obj.samples(args[ctr + 1])
                    case 'timespan':
                        # NOTE: added timespan to the solver options
                        self.solveropt.obj.timespan = JArray(jpype.JDouble)(args[ctr + 1])
                    case 'verbose':
                        if isinstance(args[ctr + 1], bool):
                            if args[ctr + 1]:
                                self.solveropt.obj.verbose(jpype.JPackage('jline').lang.constant.VerboseLevel.STD)
                            else:
                                self.solveropt.obj.verbose(jpype.JPackage('jline').lang.constant.VerboseLevel.SILENT)
                        else:
                            match (args[ctr + 1]):
                                case VerboseLevel.SILENT:
                                    self.solveropt.obj.verbose(
                                        jpype.JPackage('jline').lang.constant.VerboseLevel.SILENT)
                                case VerboseLevel.STD:
                                    self.solveropt.obj.verbose(jpype.JPackage('jline').lang.constant.VerboseLevel.STD)
                                case VerboseLevel.DEBUG:
                                    self.solveropt.obj.verbose(jpype.JPackage('jline').lang.constant.VerboseLevel.DEBUG)
                ctr += 2

    def getName(self):
        return self.obj.getName()

# Specialized subclass of Solver used to solve ensemble models
class EnsembleSolver(Solver):
    def __init__(self, options, args):
        super().__init__(options, args)
        pass

    def getNumberOfModels(self):
        return self.obj.getNumberOfModels()

    def printEnsembleAvgTables(self):
        self.obj.printEnsembleAvgTables()


# Specialized subclass of Solver used to solve network models
# Provides methods to get performance metrics from the solver
class NetworkSolver(Solver):
    def __init__(self, options, args):
        super().__init__(options, args)
        pass

    # Retrieves average performance metrics for each node
    def getAvgNodeTable(self):
        table = self.obj.getAvgNodeTable()

        # convert to NumPy

        QLen = np.array(list(table.getQLen()))
        Util = np.array(list(table.getUtil()))
        RespT = np.array(list(table.getRespT()))
        ResidT = np.array(list(table.getResidT()))
        ArvR = np.array(list(table.getArvR()))
        Tput = np.array(list(table.getTput()))

        cols = ['QLen', 'Util', 'RespT', 'ResidT', 'ArvR', 'Tput']
        nodes = list(table.getNodeNames())
        nodenames = []
        for i in range(len(nodes)):
            nodenames.append(str(nodes[i]))
        jobclasses = list(table.getClassNames())

        classnames = []
        for i in range(len(jobclasses)):
            classnames.append(str(jobclasses[i]))
        AvgTable = pd.DataFrame(np.concatenate([[QLen, Util, RespT, ResidT, ArvR, Tput]]).T, columns=cols)
        tokeep = ~(AvgTable <= 0.0).all(axis=1)
        AvgTable.insert(0, "JobClass", classnames)
        AvgTable.insert(0, "Node", nodenames)
        AvgTable = AvgTable.loc[tokeep]  # eliminate zero rows
        if not (
                GlobalConstants.getVerbose() == VerboseLevel.SILENT) and not self.solveropt.obj.verbose == VerboseLevel.SILENT:  # and not is_interactive():
            print(AvgTable)

        return AvgTable

    # Retrieves average performance metrics for each chain
    def getAvgChainTable(self):
        table = self.obj.getAvgChainTable()
        # convert to NumPy

        QLen = np.array(list(table.getQLen()))
        Util = np.array(list(table.getUtil()))
        RespT = np.array(list(table.getRespT()))
        ResidT = np.array(list(table.getResidT()))
        ArvR = np.array(list(table.getArvR()))
        Tput = np.array(list(table.getTput()))

        cols = ['QLen', 'Util', 'RespT', 'ResidT', 'ArvR', 'Tput']
        stations = list(table.getStationNames())
        statnames = []
        for i in range(len(stations)):
            statnames.append(str(stations[i]))
        jobchains = list(table.getChainNames())
        chainnames = []
        for i in range(len(jobchains)):
            chainnames.append(str(jobchains[i]))
        AvgChainTable = pd.DataFrame(np.concatenate([[QLen, Util, RespT, ResidT, ArvR, Tput]]).T, columns=cols)
        tokeep = ~(AvgChainTable <= 0.0).all(axis=1)
        AvgChainTable.insert(0, "Chain", chainnames)
        AvgChainTable.insert(0, "Station", statnames)
        AvgChainTable = AvgChainTable.loc[tokeep]  # eliminate zero rows
        if not (
                GlobalConstants.getVerbose() == VerboseLevel.SILENT) and not self.solveropt.obj.verbose == VerboseLevel.SILENT:  # and not is_interactive():
            print(AvgChainTable)

        return AvgChainTable

    # Retrieves average performance metrics for each node-chain combination
    def getAvgNodeChainTable(self):
        table = self.obj.getAvgNodeChainTable()
        # convert to NumPy

        QLen = np.array(list(table.getQLen()))
        Util = np.array(list(table.getUtil()))
        RespT = np.array(list(table.getRespT()))
        ResidT = np.array(list(table.getResidT()))
        ArvR = np.array(list(table.getArvR()))
        Tput = np.array(list(table.getTput()))

        cols = ['QLen', 'Util', 'RespT', 'ResidT', 'ArvR', 'Tput']
        nodes = list(table.getNodeNames())
        nodenames = []
        for i in range(len(nodes)):
            nodenames.append(str(nodes[i]))
        jobchains = list(table.getChainNames())
        chainnames = []
        for i in range(len(jobchains)):
            chainnames.append(str(jobchains[i]))
        AvgChainTable = pd.DataFrame(np.concatenate([[QLen, Util, RespT, ResidT, ArvR, Tput]]).T, columns=cols)
        tokeep = ~(AvgChainTable <= 0.0).all(axis=1)
        AvgChainTable.insert(0, "Chain", chainnames)
        AvgChainTable.insert(0, "Node", nodenames)
        AvgChainTable = AvgChainTable.loc[tokeep]  # eliminate zero rows
        if not (
                GlobalConstants.getVerbose() == VerboseLevel.SILENT) and not self.solveropt.obj.verbose == VerboseLevel.SILENT:  # and not is_interactive():
            print(AvgChainTable)

        return AvgChainTable

    # Retrieves average performance metrics for all stations and job classes
    def getAvgTable(self):
        table = self.obj.getAvgTable()

        # convert to NumPy

        QLen = np.array(list(table.getQLen()))
        Util = np.array(list(table.getUtil()))
        RespT = np.array(list(table.getRespT()))
        ResidT = np.array(list(table.getResidT()))
        ArvR = np.array(list(table.getArvR()))
        Tput = np.array(list(table.getTput()))

        cols = ['QLen', 'Util', 'RespT', 'ResidT', 'ArvR', 'Tput']

        stations = list(table.getStationNames())
        statnames = []
        for i in range(len(stations)):
            statnames.append(str(stations[i]))
        jobclasses = list(table.getClassNames())
        classnames = []
        for i in range(len(jobclasses)):
            classnames.append(str(jobclasses[i]))
        AvgTable = pd.DataFrame(np.concatenate([[QLen, Util, RespT, ResidT, ArvR, Tput]]).T, columns=cols)
        tokeep = ~(AvgTable <= 0.0).all(axis=1)
        AvgTable.insert(0, "JobClass", classnames)
        AvgTable.insert(0, "Station", statnames)
        AvgTable = AvgTable.loc[tokeep]  # eliminate zero rows
        if not (
                GlobalConstants.getVerbose() == VerboseLevel.SILENT) and not self.solveropt.obj.verbose == VerboseLevel.SILENT:  # and not is_interactive():
            print(AvgTable)

        return AvgTable

    # Retrieves average performance metrics for the whole system
    def getAvgSysTable(self):
        table = self.obj.getAvgSysTable()

        # convert to NumPy
        SysRespT = np.array(list(table.getSysRespT()))
        SysTput = np.array(list(table.getSysTput()))

        cols = ['SysRespT', 'SysTput']
        jobchains = list(table.getChainNames())
        chains = []
        for i in range(len(jobchains)):
            chains.append(str(jobchains[i]))
        jobinchains = list(table.getInChainNames())
        inchains = []
        for i in range(len(jobinchains)):
            inchains.append(str(jobinchains[i]))
        AvgSysTable = pd.DataFrame(np.concatenate([[SysRespT, SysTput]]).T, columns=cols)
        tokeep = ~(AvgSysTable <= 0.0).all(axis=1)
        AvgSysTable.insert(0, "JobClasses", inchains)
        AvgSysTable.insert(0, "Chain", chains)
        AvgSysTable = AvgSysTable.loc[tokeep]  # eliminate zero rows
        if not (
                GlobalConstants.getVerbose() == VerboseLevel.SILENT) and not self.solveropt.obj.verbose == VerboseLevel.SILENT:
            print(AvgSysTable)
        return AvgSysTable

    """
    Below are methods for retrieving specific performance metrics
    """
    # Retrieves average throughput
    def getAvgTput(self):
        Tput = jlineMatrixToArray(self.obj.getAvgTput())
        if not (
                GlobalConstants.getVerbose() == VerboseLevel.SILENT) and not self.solveropt.obj.verbose == VerboseLevel.SILENT:
            print(Tput)
        return Tput

    # Retrieves average residence time
    def getAvgResidT(self):
        ResidT = jlineMatrixToArray(self.obj.getAvgResidT())
        if not (
                GlobalConstants.getVerbose() == VerboseLevel.SILENT) and not self.solveropt.obj.verbose == VerboseLevel.SILENT:
            print(ResidT)
        return ResidT

    # Retrieves average arrival rate
    def getAvgArvR(self):
        ArvR = jlineMatrixToArray(self.obj.getAvgArvR())
        if not (
                GlobalConstants.getVerbose() == VerboseLevel.SILENT) and not self.solveropt.obj.verbose == VerboseLevel.SILENT:
            print(ArvR)
        return ArvR

    # Retrieves average utilization
    def getAvgUtil(self):
        Util = jlineMatrixToArray(self.obj.getAvgUtil())
        if not (
                GlobalConstants.getVerbose() == VerboseLevel.SILENT) and not self.solveropt.obj.verbose == VerboseLevel.SILENT:
            print(Util)
        return Util

    # Retrieves average queue length
    def getAvgQLen(self):
        QLen = jlineMatrixToArray(self.obj.getAvgQLen())
        if not (
                GlobalConstants.getVerbose() == VerboseLevel.SILENT) and not self.solveropt.obj.verbose == VerboseLevel.SILENT:
            print(QLen)
        return QLen

    # Retrieves average response time
    def getAvgRespT(self):
        RespT = jlineMatrixToArray(self.obj.getAvgRespT())
        if not (
                GlobalConstants.getVerbose() == VerboseLevel.SILENT) and not self.solveropt.obj.verbose == VerboseLevel.SILENT:
            print(RespT)
        return RespT

    # Retrieves average system throughput
    def getAvgSysTput(self):
        SysTput = jlineMatrixToArray(self.obj.getAvgSysTput())
        if not (
                GlobalConstants.getVerbose() == VerboseLevel.SILENT) and not self.solveropt.obj.verbose == VerboseLevel.SILENT:
            print(SysTput)
        return SysTput

    # Retrieves average system response time
    def getAvgSysRespT(self):
        SysRespT = jlineMatrixToArray(self.obj.getAvgSysRespT())
        if not (
                GlobalConstants.getVerbose() == VerboseLevel.SILENT) and not self.solveropt.obj.verbose == VerboseLevel.SILENT:
            print(SysRespT)
        return SysRespT

    # Retrieves the CDF of the response time (only returned by SolverFluid)
    def getCdfRespT(self):
        try:
            table = self.obj.getCdfRespT()
            distribC = self.obj.fluidResult.distribC
            CdfRespT = []
            for i in range(distribC.length):
                for c in range(distribC[i].length):
                    F = jlineMatrixToArray(distribC[i][c])
                    CdfRespT.append(F)
            return np.asarray(CdfRespT)
        except:
            return [[]]

# Specialized subclass of NetworkSolver that uses the CTMC method
class SolverCTMC(NetworkSolver):
    def __init__(self, *args):
        options = SolverOptions(jpype.JPackage('jline').lang.constant.SolverType.CTMC)
        super().__init__(options, args)
        model = args[0] # model is the first argument
        self.obj = jpype.JPackage('jline').solvers.ctmc.SolverCTMC(model.obj, self.solveropt.obj)

    def getStateSpace(self):
        StateSpace = self.obj.getStateSpace()
        return jlineMatrixToArray(StateSpace.stateSpace), jlineMapMatrixToArray(StateSpace.localStateSpace.toMap())

    def getGenerator(self):
        generatorResult = self.obj.getGenerator()
        return jlineMatrixToArray(generatorResult.infGen), jlineMapMatrixToArray(generatorResult.eventFilt.toMap())#, jlineMapMatrixToArray(generatorResult.ev)

    @staticmethod
    def printInfGen(infGen, stateSpace):
        jpype.JPackage('jline').solvers.ctmc.SolverCTMC.printInfGen(jlineMatrixFromArray(infGen), jlineMatrixFromArray(stateSpace))

# Specialized subclass of EnsembleSolver
class SolverEnv(EnsembleSolver):
    def __init__(self, *args):
        options = SolverOptions(jpype.JPackage('jline').lang.constant.SolverType.ENV) # default SolverEnv options?
        super().__init__(options, [])
        model = args[0] # model is the first argument
        solvers = jpype.JPackage('jline').solvers.NetworkSolver[len(args[1])] # second argument is the list of solvers
        for i in range(len(solvers)):
            solvers[i] = args[1][i].obj
        self.obj = jpype.JPackage('jline').solvers.env.SolverEnv(model.obj, solvers, self.solveropt.obj)

    def getEnsembleAvg(self):
        return self.obj.getEnsembleAvg()

    def printAvgTable(self):
        # calls getAvg() which calls getEnsembleAvg() which calls iterate()
        # fetches results and prints them in table format
        self.obj.printAvgTable()

    def runAnalyzer(self):
        # calls iterate()
        self.obj.runAnalyzer()

    def getName(self):
        return self.obj.getName()


# Specialized subclass of NetworkSolver that uses the Fluid method
class SolverFluid(NetworkSolver):
    def __init__(self, *args):
        options = SolverOptions(jpype.JPackage('jline').lang.constant.SolverType.FLUID) # default options object
        super().__init__(options, args)
        self.model = args[0] # model is the first argument
        self.obj = jpype.JPackage('jline').solvers.fluid.SolverFluid(self.model.obj, self.solveropt.obj)
    # NOTE: missing wrappers for SolverFluid methods
    # the result field contains steady-state metrics, transient metrics and the response time distribution (CDF)

    def run_fluid_analyzer(self, options):
        # check if all solver options have been defined
        required_keys = ['method', 'init_sol', 'iter_max', 'verbose', 'tol', 'iter_tol', 'stiff', 'timespan']
        missing = [key for key in required_keys if key not in options]
        if missing:
            raise ValueError(f"Missing required solver options: {missing}")
        else:
            sn = self.model.getStruct()
            QN, UN, RN, TN, CN, XN, t, QNt, UNt, TNt, xvec_iter, iter = solver_fluid_analyzer(sn, options)

            results = {
                'QN': QN,
                'UN': UN,
                'RN': RN,
                'TN': TN,
                'CN': CN,
                'XN': XN,
                't': t,
                'QNt': QNt,
                'UNt': UNt,
                'TNt': TNt,
                'xvec_iter': xvec_iter,
                'iter': iter
            }
            return results

    # Returns transient performance metrics as a dictionary of numpy time-series arrays
    def getTranAvg(self):

        result = self.obj.result

        M = result.QNt.length # number of stations
        K = result.QNt[0].length # number of classes

        def extract(metrics):
            return [[jlineMatrixToArray(metrics[i][k]) for k in range(K)] for i in range(M)]

        return {
            'QNt': extract(result.QNt),
            'UNt': extract(result.UNt),
            'TNt': extract(result.TNt),
        }


# Specialized subclass of NetworkSolver that uses the JMT method
class SolverJMT(NetworkSolver):
    def __init__(self, *args):
        options = SolverOptions(jpype.JPackage('jline').lang.constant.SolverType.JMT)
        super().__init__(options, args)
        model = args[0] # model is the first argument
        self.jmtPath = jpype.JPackage('java').lang.String(os.path.dirname(os.path.abspath(__file__)) + "/JMT.jar")
        self.obj = jpype.JPackage('jline').solvers.jmt.SolverJMT(model.obj, self.solveropt.obj, self.jmtPath)

    def jsimwView(self):
        self.obj.jsimwView(self.jmtPath)

    def jsimgView(self):
        self.obj.jsimgView(self.jmtPath)

# Specialized subclass of NetworkSolver that uses the MAM method (Matrix Analytic Method)
class SolverMAM(NetworkSolver):
    def __init__(self, *args):
        options = SolverOptions(jpype.JPackage('jline').lang.constant.SolverType.MAM)
        super().__init__(options, args)
        model = args[0] # model is the first argument
        self.obj = jpype.JPackage('jline').solvers.mam.SolverMAM(model.obj, self.solveropt.obj)
    # NOTE: missing wrappers for SolverMAM methods

# Specialized subclass of NetworkSolver that uses the MVA method
class SolverMVA(NetworkSolver):
    def __init__(self, *args):
        options = SolverOptions(jpype.JPackage('jline').lang.constant.SolverType.MVA)
        super().__init__(options, args)
        model = args[0] #
        self.obj = jpype.JPackage('jline').solvers.mva.SolverMVA(model.obj, self.solveropt.obj)
    # NOTE: missing wrappers for SolverMVA methods

# Specialized subclass of Solver that uses the LQNS method
class SolverLQNS(Solver):
    def __init__(self, *args):
        options = SolverOptions(jpype.JPackage('jline').lang.constant.SolverType.LQNS)
        super().__init__(options, args)
        model = args[0]
        self.obj = jpype.JPackage('jline').solvers.lqns.SolverLQNS(model.obj, self.solveropt.obj)

    def getAvgTable(self):
        table = self.obj.getAvgTable()
        # convert to NumPy

        QLen = np.array(list(table.getQLen()))
        Util = np.array(list(table.getUtil()))
        RespT = np.array(list(table.getRespT()))
        ResidT = np.array(list(table.getResidT()))
        ArvR = np.array(list(table.getArvR()))
        Tput = np.array(list(table.getTput()))

        cols = ['QLen', 'Util', 'RespT', 'ResidT', 'ArvR', 'Tput']
        nodenames = list(table.getNodeNames())
        mynodenames = []
        for i in range(len(nodenames)):
            mynodenames.append(str(nodenames[i]))
        nodetypes = list(table.getNodeTypes())
        mynodetypes = []
        for i in range(len(nodetypes)):
            mynodetypes.append(str(nodetypes[i]))
        AvgTable = pd.DataFrame(np.concatenate([[QLen, Util, RespT, ResidT, ArvR, Tput]]).T, columns=cols)
        tokeep = ~(AvgTable <= 0.0).all(axis=1)
        AvgTable.insert(0, "NodeType", mynodetypes)
        AvgTable.insert(0, "Node", mynodenames)
        AvgTable = AvgTable.loc[tokeep]  # eliminate zero rows
        if not (
                GlobalConstants.getVerbose() == VerboseLevel.SILENT) and not self.solveropt.obj.verbose == VerboseLevel.SILENT:  # and not is_interactive():
            print(AvgTable)

        return AvgTable

# Specialized subclass of EnsembleSolver for solving ensembles of Layered Networks
class SolverLN(EnsembleSolver):
    def __init__(self, *args):
        options = SolverOptions(jpype.JPackage('jline').lang.constant.SolverType.LN)
        super().__init__(options, args)
        model = args[0]
        self.obj = jpype.JPackage('jline').solvers.ln.SolverLN(model.obj, self.solveropt.obj)


    def getAvgTable(self):
        table = self.obj.getAvgTable()
        # convert to NumPy

        QLen = np.array(list(table.getQLen()))
        Util = np.array(list(table.getUtil()))
        RespT = np.array(list(table.getRespT()))
        ResidT = np.array(list(table.getResidT()))
        ArvR = np.array(list(table.getArvR()))
        Tput = np.array(list(table.getTput()))

        cols = ['QLen', 'Util', 'RespT', 'ResidT', 'ArvR', 'Tput']
        nodenames = list(table.getNodeNames())
        mynodenames = []
        for i in range(len(nodenames)):
            mynodenames.append(str(nodenames[i]))
        nodetypes = list(table.getNodeTypes())
        mynodetypes = []
        for i in range(len(nodetypes)):
            mynodetypes.append(str(nodetypes[i]))
        AvgTable = pd.DataFrame(np.concatenate([[QLen, Util, RespT, ResidT, ArvR, Tput]]).T, columns=cols)
        tokeep = ~(AvgTable <= 0.0).all(axis=1)
        AvgTable.insert(0, "NodeType", mynodetypes)
        AvgTable.insert(0, "Node", mynodenames)
        AvgTable = AvgTable.loc[tokeep]  # eliminate zero rows
        if not (
                GlobalConstants.getVerbose() == VerboseLevel.SILENT) and not self.solveropt.obj.verbose == VerboseLevel.SILENT:  # and not is_interactive():
            print(AvgTable)

        return AvgTable

# Specialized subckass of NetworkSolver that uses the NC method
class SolverNC(NetworkSolver):
    def __init__(self, *args):
        options = SolverOptions(jpype.JPackage('jline').lang.constant.SolverType.NC)
        super().__init__(options, args)
        model = args[0]
        self.obj = jpype.JPackage('jline').solvers.nc.SolverNC(model.obj, self.solveropt.obj)
    # NOTE: missing wrappers for SolverNC methods

# Specialized subclass of NetworkSolver that uses the SSA method
class SolverSSA(NetworkSolver):
    def __init__(self, *args):
        options = SolverOptions(jpype.JPackage('jline').lang.constant.SolverType.SSA)
        super().__init__(options, args)
        model = args[0]
        self.obj = jpype.JPackage('jline').solvers.ssa.SolverSSA(model.obj, self.solveropt.obj)
    # NOTE: missing wrappers for SolverSSA methods

# Base class for all solver options
class SolverOptions():
    def __init__(self, solvertype):
        self.obj = jpype.JPackage('jline').solvers.SolverOptions(solvertype)

    def method(self, value):
        self.obj.method(value)

    def samples(self, value):
        self.obj.samples(value)

    def seed(self, value):
        self.obj.seed(value)

    def verbose(self, value):
        self.obj.verbose(value)

# Class for CTMC options
class CTMCOptions():
    def __init__(self):
        self.obj = jpype.JPackage('jline').solvers.CTMCOptions()

# Class for ENV options
class EnvOptions():
    def __init__(self):
        self.obj = jpype.JPackage('jline').solvers.EnvOptions()

# Class for Fluid options
class FluidOptions():
    def __init__(self):
        self.obj = jpype.JPackage('jline').solvers.FluidOptions()

# Class for JMT options
class JMTOptions():
    def __init__(self):
        self.obj = jpype.JPackage('jline').solvers.JMTOptions()

# Class for LN options
class LNOptions():
    def __init__(self):
        self.obj = jpype.JPackage('jline').solvers.LNOptions()

# Class for LQNS options
class LQNSOptions():
    def __init__(self):
        self.obj = jpype.JPackage('jline').solvers.LQNSOptions()

# Class for MAM options
class MAMOptions():
    def __init__(self):
        self.obj = jpype.JPackage('jline').solvers.MAMOptions()

# Class for MVA options
class MVAOptions():
    def __init__(self):
        self.obj = jpype.JPackage('jline').solvers.MVAOptions()

# Class for NC options
class NCOptions():
    def __init__(self):
        self.obj = jpype.JPackage('jline').solvers.NCOptions()

# Class for SSA options
class SSAOptions():
    def __init__(self):
        self.obj = jpype.JPackage('jline').solvers.SSAOptions()
