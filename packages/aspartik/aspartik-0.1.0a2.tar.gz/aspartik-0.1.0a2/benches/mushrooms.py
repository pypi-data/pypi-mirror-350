from aspartik.b3 import MCMC, Tree, Parameter, Likelihood
from aspartik.b3.loggers import TreeLogger, PrintLogger, ValueLogger
from aspartik.b3.operators import (
    ParamScale,
    EpochScale,
    TreeScale,
    RootScale,
    NarrowExchange,
    WideExchange,
    NodeSlide,
    WilsonBalding,
)
from aspartik.b3.priors import Distribution, Yule
from aspartik.b3.substitutions import HKY
from aspartik.stats.distributions import Gamma, Uniform
from aspartik.rng import RNG
from aspartik.io.fasta import FASTADNAReader

path = "data/512.fasta"
sequences = []
names = []
for record in FASTADNAReader(path):
    sequences.append(record.sequence)
    names.append(record.description)

rng = RNG(4)
tree = Tree(names, rng)

birth_rate_y = Parameter.Real(1.0)

params = [
    birth_rate_y,
]

priors = [
    # Yule(tree, birth_rate_y),
    Distribution(birth_rate_y, Gamma(0.001, 1 / 1000.0)),
]

operators = [
    ParamScale(birth_rate_y, 0.1, Uniform(0, 1), rng, weight=3),
    EpochScale(tree, 0.9, Uniform(0, 1), rng, weight=4.0),
    TreeScale(tree, 0.9, Uniform(0, 1), rng, weight=2.0),
    RootScale(tree, 0.9, Uniform(0, 1), rng, weight=3.0),
    NodeSlide(tree, Uniform(0, 1), rng, weight=45.0),
    NarrowExchange(tree, rng, weight=15.0),
    WideExchange(tree, rng, weight=3.0),
    WilsonBalding(tree, rng, weight=3.0),
]

model = HKY((0.25, 0.25, 0.25, 0.25), Parameter.Real(2.0))
likelihood = Likelihood(
    sequences=sequences,
    substitution=model,
    tree=tree,
    calculator="thread",
)

loggers = [
    TreeLogger(tree=tree, path="b3.trees", every=1_000),
    PrintLogger(every=1_000),
    ValueLogger(
        {"birth_rate_y": birth_rate_y},
        path="b3.log",
        every=1_000,
    ),
]

mcmc = MCMC(
    burnin=0,
    length=19_000,
    trees=[tree],
    params=params,
    priors=priors,
    operators=operators,
    likelihoods=[likelihood],
    loggers=loggers,
    rng=rng,
)

mcmc.run()
