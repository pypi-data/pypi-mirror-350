from enum_tools import Enum
import jpype
import jpype.imports
from line_solver.distributions import *

"""
Defines Python enums (sets of related constants) that map directly to corresponding Java constants in JLINE.
Provides a convenient way to access pre-defined values from the JLINE library.
"""

# Defines the different types of activity precedence relationships in layered models
class ActivityPrecedenceType(Enum):
    # __repr__ method defines how an instance of the enum class is represented
    def __repr__(self):
        return str(self.value)
    PRE_SEQ = jpype.JPackage('jline').lang.constant.ActivityPrecedenceType.PRE_SEQ
    PRE_AND = jpype.JPackage('jline').lang.constant.ActivityPrecedenceType.PRE_AND
    PRE_OR = jpype.JPackage('jline').lang.constant.ActivityPrecedenceType.PRE_OR
    POST_SEQ = jpype.JPackage('jline').lang.constant.ActivityPrecedenceType.POST_SEQ
    POST_AND = jpype.JPackage('jline').lang.constant.ActivityPrecedenceType.POST_AND
    POST_OR = jpype.JPackage('jline').lang.constant.ActivityPrecedenceType.POST_OR
    POST_LOOP = jpype.JPackage('jline').lang.constant.ActivityPrecedenceType.POST_LOOP
    POST_CACHE = jpype.JPackage('jline').lang.constant.ActivityPrecedenceType.POST_CACHE

# Defines the different types of calls in a model
class CallType(Enum):
    def __repr__(self):
        return str(self.value)
    SYNC = jpype.JPackage('jline').lang.constant.CallType.SYNC
    ASYNC = jpype.JPackage('jline').lang.constant.CallType.ASYNC
    FWD = jpype.JPackage('jline').lang.constant.CallType.FWD

# Defines the different strategies for handling dropped requests
class DropStrategy(Enum):
    def __repr__(self):
        return str(self.value)
    WaitingQueue = jpype.JPackage('jline').lang.constant.DropStrategy.WaitingQueue
    Drop = jpype.JPackage('jline').lang.constant.DropStrategy.Drop
    BlockingAfterService = jpype.JPackage('jline').lang.constant.DropStrategy.BlockingAfterService

# Defines the different types of events in a model
class EventType(Enum):
    def __repr__(self):
        return str(self.value)
    INIT = jpype.JPackage('jline').lang.constant.EventType.INIT
    LOCAL = jpype.JPackage('jline').lang.constant.EventType.LOCAL
    ARV = jpype.JPackage('jline').lang.constant.EventType.ARV
    DEP = jpype.JPackage('jline').lang.constant.EventType.DEP
    PHASE = jpype.JPackage('jline').lang.constant.EventType.PHASE
    READ = jpype.JPackage('jline').lang.constant.EventType.READ
    STAGE = jpype.JPackage('jline').lang.constant.EventType.STAGE

# Defines the different types of job classes in a queueing network
class JobClassType(Enum):
    def __repr__(self):
        return str(self.value)
    OPEN = jpype.JPackage('jline').lang.constant.JobClassType.OPEN
    CLOSED = jpype.JPackage('jline').lang.constant.JobClassType.CLOSED
    DISABLED = jpype.JPackage('jline').lang.constant.JobClassType.DISABLED

# Defines the different strategies to join tasks in a model
class JoinStrategy(Enum):
    def __repr__(self):
        return str(self.value)
    STD = jpype.JPackage('jline').lang.constant.JoinStrategy.STD
    PARTIAL = jpype.JPackage('jline').lang.constant.JoinStrategy.PARTIAL
    Quorum = jpype.JPackage('jline').lang.constant.JoinStrategy.Quorum
    Guard = jpype.JPackage('jline').lang.constant.JoinStrategy.Guard

# Defines the different metrics that can be measured in a model
class MetricType(Enum):
    def __repr__(self):
        return str(self.value)
    ResidT = jpype.JPackage('jline').lang.constant.MetricType.ResidT
    RespT = jpype.JPackage('jline').lang.constant.MetricType.RespT
    DropRate = jpype.JPackage('jline').lang.constant.MetricType.DropRate
    QLen = jpype.JPackage('jline').lang.constant.MetricType.QLen
    QueueT = jpype.JPackage('jline').lang.constant.MetricType.QueueT
    FCRWeight = jpype.JPackage('jline').lang.constant.MetricType.FCRWeight
    FCRMemOcc = jpype.JPackage('jline').lang.constant.MetricType.FCRMemOcc
    FJQLen = jpype.JPackage('jline').lang.constant.MetricType.FJQLen
    FJRespT = jpype.JPackage('jline').lang.constant.MetricType.FJRespT
    RespTSink = jpype.JPackage('jline').lang.constant.MetricType.RespTSink
    SysDropR = jpype.JPackage('jline').lang.constant.MetricType.SysDropR
    SysQLen = jpype.JPackage('jline').lang.constant.MetricType.SysQLen
    SysPower = jpype.JPackage('jline').lang.constant.MetricType.SysPower
    SysRespT = jpype.JPackage('jline').lang.constant.MetricType.SysRespT
    SysTput = jpype.JPackage('jline').lang.constant.MetricType.SysTput
    Tput = jpype.JPackage('jline').lang.constant.MetricType.Tput
    ArvR = jpype.JPackage('jline').lang.constant.MetricType.ArvR
    TputSink = jpype.JPackage('jline').lang.constant.MetricType.TputSink
    Util = jpype.JPackage('jline').lang.constant.MetricType.Util
    TranQLen = jpype.JPackage('jline').lang.constant.MetricType.TranQLen
    TranUtil = jpype.JPackage('jline').lang.constant.MetricType.TranUtil
    TranTput = jpype.JPackage('jline').lang.constant.MetricType.TranTput
    TranRespT = jpype.JPackage('jline').lang.constant.MetricType.TranRespT

# Defines the different types of nodes in a model
class NodeType(Enum):
    def __repr__(self):
        return str(self.value)
    Transition = jpype.JPackage('jline').lang.constant.NodeType.Transition
    Place = jpype.JPackage('jline').lang.constant.NodeType.Place
    Fork = jpype.JPackage('jline').lang.constant.NodeType.Fork
    Router = jpype.JPackage('jline').lang.constant.NodeType.Router
    Cache = jpype.JPackage('jline').lang.constant.NodeType.Cache
    Logger = jpype.JPackage('jline').lang.constant.NodeType.Logger
    ClassSwitch = jpype.JPackage('jline').lang.constant.NodeType.ClassSwitch
    Delay = jpype.JPackage('jline').lang.constant.NodeType.Delay
    Source = jpype.JPackage('jline').lang.constant.NodeType.Source
    Sink = jpype.JPackage('jline').lang.constant.NodeType.Sink
    Join = jpype.JPackage('jline').lang.constant.NodeType.Join
    Queue = jpype.JPackage('jline').lang.constant.NodeType.Queue

    # Helper method that maps strings to Python NodeType enums
    # Modified name fromJLINE to fromString for clarity
    @staticmethod
    def fromJLine(obj):
        match str(obj):
            case 'Transition':
                return NodeType.Transition
            case 'Place':
                return NodeType.Place
            case 'Fork':
                return NodeType.Fork
            case 'Router':
                return NodeType.Router
            case 'Cache':
                return NodeType.Cache
            case 'Logger':
                return NodeType.Logger
            case 'ClassSwitch':
                return NodeType.ClassSwitch
            case 'Delay':
                return NodeType.Delay
            case 'Source':
                return NodeType.Source
            case 'Sink':
                return NodeType.Sink
            case 'Join':
                return NodeType.Join
            case 'Queue':
                return NodeType.Queue

# Defines the different types of processes in a model
class ProcessType(Enum):
    def __repr__(self):
        return str(self.value)

    EXP = jpype.JPackage('jline').lang.constant.ProcessType.EXP
    ERLANG = jpype.JPackage('jline').lang.constant.ProcessType.ERLANG
    DISABLED = jpype.JPackage('jline').lang.constant.ProcessType.DISABLED
    IMMEDIATE = jpype.JPackage('jline').lang.constant.ProcessType.IMMEDIATE
    HYPEREXP = jpype.JPackage('jline').lang.constant.ProcessType.HYPEREXP
    APH = jpype.JPackage('jline').lang.constant.ProcessType.APH
    COXIAN = jpype.JPackage('jline').lang.constant.ProcessType.COXIAN
    PH = jpype.JPackage('jline').lang.constant.ProcessType.PH
    MAP = jpype.JPackage('jline').lang.constant.ProcessType.MAP
    UNIFORM = jpype.JPackage('jline').lang.constant.ProcessType.UNIFORM
    DET = jpype.JPackage('jline').lang.constant.ProcessType.DET
    GAMMA = jpype.JPackage('jline').lang.constant.ProcessType.GAMMA
    PARETO = jpype.JPackage('jline').lang.constant.ProcessType.PARETO
    WEIBULL = jpype.JPackage('jline').lang.constant.ProcessType.WEIBULL
    LOGNORMAL = jpype.JPackage('jline').lang.constant.ProcessType.LOGNORMAL
    MMPP2 = jpype.JPackage('jline').lang.constant.ProcessType.MMPP2
    REPLAYER = jpype.JPackage('jline').lang.constant.ProcessType.REPLAYER
    TRACE = jpype.JPackage('jline').lang.constant.ProcessType.TRACE
    COX2 = jpype.JPackage('jline').lang.constant.ProcessType.COX2
    BINOMIAL = jpype.JPackage('jline').lang.constant.ProcessType.BINOMIAL
    POISSON = jpype.JPackage('jline').lang.constant.ProcessType.POISSON

    # Added a helper method (similar to NodeType) to map strings to Python ProcessType enums
    # Mapping follows: String -> Python ProcessType -> Java ProcessType
    @staticmethod
    def fromString(obj):
        match str(obj):
            case "Exp":
                return ProcessType.EXP
            case "Erlang":
                return ProcessType.ERLANG
            case "HyperExp":
                return ProcessType.HYPEREXP
            case "PH":
                return ProcessType.PH
            case "APH":
                return ProcessType.APH
            case "MAP":
                return ProcessType.MAP
            case "Uniform":
                return ProcessType.UNIFORM
            case "Det":
                return ProcessType.DET
            case "Coxian":
                return ProcessType.COXIAN
            case "Gamma":
                return ProcessType.GAMMA
            case "Pareto":
                return ProcessType.PARETO
            case "MMPP2":
                return ProcessType.MMPP2
            case "Replayer":
                return ProcessType.REPLAYER
            case "Trace":
                return ProcessType.TRACE
            case "Immediate":
                return ProcessType.IMMEDIATE
            case "Disabled":
                return ProcessType.DISABLED
            case "Cox2":
                return ProcessType.COX2
            case "Weibull":
                return ProcessType.WEIBULL
            case "Lognormal":
                return ProcessType.LOGNORMAL
            case "Poisson":
                return ProcessType.POISSON
            case "Binomial":
                return ProcessType.BINOMIAL
            case _:
                raise ValueError(f"Unsupported ProcessType: {obj}")

    # Added a helper method that maps process types to corresponding distribution classes
    def toDistribution(process_type, *args):
        match process_type:
            case ProcessType.EXP:
                return Exp
            case ProcessType.DET:
                return Det
            case ProcessType.ERLANG:
                return Erlang
            case ProcessType.HYPEREXP:
                return HyperExp
            case ProcessType.UNIFORM:
                return Uniform
            case ProcessType.IMMEDIATE:
                return Immediate
            case ProcessType.DISABLED:
                return Disabled
            # Add other cases as needed
            case _:
                raise ValueError(f"Unsupported ProcessType: {process_type}")

# Defines the different types of replacement strategies in a model
class ReplacementStrategy(Enum):
    def __repr__(self):
        return str(self.value)
    RR = jpype.JPackage('jline').lang.constant.ReplacementStrategy.RR
    FIFO = jpype.JPackage('jline').lang.constant.ReplacementStrategy.FIFO
    SFIFO = jpype.JPackage('jline').lang.constant.ReplacementStrategy.SFIFO
    LRU = jpype.JPackage('jline').lang.constant.ReplacementStrategy.LRU

# Defines the different types of routing strategies in a model
class RoutingStrategy(Enum):
    def __repr__(self):
        return str(self.value)
    RAND = jpype.JPackage('jline').lang.constant.RoutingStrategy.RAND
    PROB = jpype.JPackage('jline').lang.constant.RoutingStrategy.PROB
    RROBIN = jpype.JPackage('jline').lang.constant.RoutingStrategy.RROBIN
    WRROBIN = jpype.JPackage('jline').lang.constant.RoutingStrategy.WRROBIN
    JSQ = jpype.JPackage('jline').lang.constant.RoutingStrategy.JSQ
    DISABLED = jpype.JPackage('jline').lang.constant.RoutingStrategy.DISABLED
    FIRING = jpype.JPackage('jline').lang.constant.RoutingStrategy.FIRING
    KCHOICES = jpype.JPackage('jline').lang.constant.RoutingStrategy.KCHOICES

# Defines the different scheduling strategies for servers
class SchedStrategy(Enum):
    def __repr__(self):
        return str(self.value) # string representation

    INF = jpype.JPackage('jline').lang.constant.SchedStrategy.INF
    FCFS = jpype.JPackage('jline').lang.constant.SchedStrategy.FCFS
    LCFS = jpype.JPackage('jline').lang.constant.SchedStrategy.LCFS
    LCFSPR = jpype.JPackage('jline').lang.constant.SchedStrategy.LCFSPR
    SIRO = jpype.JPackage('jline').lang.constant.SchedStrategy.SIRO
    SJF = jpype.JPackage('jline').lang.constant.SchedStrategy.SJF
    LJF = jpype.JPackage('jline').lang.constant.SchedStrategy.LJF
    PS = jpype.JPackage('jline').lang.constant.SchedStrategy.PS
    DPS = jpype.JPackage('jline').lang.constant.SchedStrategy.DPS
    GPS = jpype.JPackage('jline').lang.constant.SchedStrategy.GPS
    SEPT = jpype.JPackage('jline').lang.constant.SchedStrategy.SEPT
    LEPT = jpype.JPackage('jline').lang.constant.SchedStrategy.LEPT
    HOL = jpype.JPackage('jline').lang.constant.SchedStrategy.HOL
    FORK = jpype.JPackage('jline').lang.constant.SchedStrategy.FORK
    EXT = jpype.JPackage('jline').lang.constant.SchedStrategy.EXT
    REF = jpype.JPackage('jline').lang.constant.SchedStrategy.REF

    # Added a helper method to map strings to Python SchedStrategy enums
    @staticmethod
    def fromString(obj):
        match str(obj):
            case 'INF':
                return SchedStrategy.INF
            case 'FCFS':
                return SchedStrategy.FCFS
            case 'LCFS':
                return SchedStrategy.LCFS
            case 'LCFSPR':
                return SchedStrategy.LCFSPR
            case 'SIRO':
                return SchedStrategy.SIRO
            case 'SJF':
                return SchedStrategy.SJF
            case 'LJF':
                return SchedStrategy.LJF
            case 'PS':
                return SchedStrategy.PS
            case 'DPS':
                return SchedStrategy.DPS
            case 'GPS':
                return SchedStrategy.GPS
            case 'SEPT':
                return SchedStrategy.SEPT
            case 'LEPT':
                return SchedStrategy.LEPT
            case 'HOL':
                return SchedStrategy.HOL
            case 'FORK':
                return SchedStrategy.FORK
            case 'EXT':
                return SchedStrategy.EXT
            case 'REF':
                return SchedStrategy.REF
            case _:
                raise ValueError(f"Unsupported SchedStrategy: {obj}")

    # Added a wrapper for the fromLINEString method
    # convert string to SchedStrategy Java obj
    @staticmethod
    def fromLINEString(sched: str):
        return jpype.JPackage('jline').lang.constant.SchedStrategy.fromLINEString(sched.lower())

    # Added a wrapper for the toID method
    # convert from SchedStrategy obj to ID (converted to int)
    @staticmethod
    def toID(sched):
        return int(jpype.JPackage('jline').lang.constant.SchedStrategy.toID(sched))

# Defines the different types of scheduling strategies
class SchedStrategyType(Enum):
    def __repr__(self):
        return str(self.value)
    PR = jpype.JPackage('jline').lang.constant.SchedStrategyType.PR
    PNR = jpype.JPackage('jline').lang.constant.SchedStrategyType.PNR
    NP = jpype.JPackage('jline').lang.constant.SchedStrategyType.NP
    NPPrio = jpype.JPackage('jline').lang.constant.SchedStrategyType.NPPrio

# Defines the different types of service strategies
class ServiceStrategy(Enum):
    def __repr__(self):
        return str(self.value)
    LI = jpype.JPackage('jline').lang.constant.ServiceStrategy.LI
    LD = jpype.JPackage('jline').lang.constant.ServiceStrategy.LD
    CD = jpype.JPackage('jline').lang.constant.ServiceStrategy.CD
    SD = jpype.JPackage('jline').lang.constant.ServiceStrategy.SD

# Defines the different types of solvers available in JLINE
class SolverType(Enum):
    def __repr__(self):
        return str(self.value)
    CTMC = jpype.JPackage('jline').lang.constant.SolverType.CTMC
    ENV = jpype.JPackage('jline').lang.constant.SolverType.ENV
    FLUID = jpype.JPackage('jline').lang.constant.SolverType.FLUID
    JMT = jpype.JPackage('jline').lang.constant.SolverType.JMT
    LN = jpype.JPackage('jline').lang.constant.SolverType.LN
    LQNS = jpype.JPackage('jline').lang.constant.SolverType.LQNS
    MAM = jpype.JPackage('jline').lang.constant.SolverType.MAM
    MVA = jpype.JPackage('jline').lang.constant.SolverType.MVA
    NC = jpype.JPackage('jline').lang.constant.SolverType.NC
    SSA = jpype.JPackage('jline').lang.constant.SolverType.SSA

# Defines timing strategies for events
class TimingStrategy(Enum):
    def __repr__(self):
        return str(self.value)
    TIMED = jpype.JPackage('jline').lang.constant.TimingStrategy.TIMED
    IMMEDIATE = jpype.JPackage('jline').lang.constant.TimingStrategy.IMMEDIATE

# Defines verbosity levels for logging and debugging
class VerboseLevel(Enum):
    def __repr__(self):
        return str(self.value)
    SILENT = jpype.JPackage('jline').lang.constant.VerboseLevel.SILENT
    STD = jpype.JPackage('jline').lang.constant.VerboseLevel.STD
    DEBUG = jpype.JPackage('jline').lang.constant.VerboseLevel.DEBUG

# Provides access to global constants in JLINE library
class GlobalConstants:
    def __repr__(self):
        return str(self.value)

    Zero = jpype.JPackage('jline').lang.constant.GlobalConstants.Zero
    CoarseTol = jpype.JPackage('jline').lang.constant.GlobalConstants.CoarseTol
    FineTol = jpype.JPackage('jline').lang.constant.GlobalConstants.FineTol
    Immediate = jpype.JPackage('jline').lang.constant.GlobalConstants.Immediate
    Version = jpype.JPackage('jline').lang.constant.GlobalConstants.Version
    Verbose = jpype.JPackage('jline').lang.constant.GlobalConstants.Verbose
    DummyMode = jpype.JPackage('jline').lang.constant.GlobalConstants.DummyMode

    # Retrieves the verbosity level from the JLINE library
    @staticmethod
    def getVerbose():
        GC = jpype.JPackage('jline').lang.constant.GlobalConstants.getInstance()
        verbose = GC.getVerbose()
        if verbose == jpype.JPackage('jline').lang.constant.VerboseLevel.STD:
            return VerboseLevel.STD
        elif verbose == jpype.JPackage('jline').lang.constant.VerboseLevel.DEBUG:
            return VerboseLevel.DEBUG
        elif verbose == jpype.JPackage('jline').lang.constant.VerboseLevel.SILENT:
            return VerboseLevel.SILENT

    # Sets the verbosity level
    def setVerbose(verbosity):
        if verbosity == VerboseLevel.STD:
            GC = jpype.JPackage('jline').lang.constant.GlobalConstants.getInstance()
            GC.setVerbose(jpype.JPackage('jline').lang.constant.VerboseLevel.STD)
        elif verbosity == VerboseLevel.DEBUG:
            GC = jpype.JPackage('jline').lang.constant.GlobalConstants.getInstance()
            GC.setVerbose(jpype.JPackage('jline').lang.constant.VerboseLevel.DEBUG)
        elif verbosity ==  VerboseLevel.SILENT:
            GC = jpype.JPackage('jline').lang.constant.GlobalConstants.getInstance()
            GC.setVerbose(jpype.JPackage('jline').lang.constant.VerboseLevel.SILENT)
