# Take a look at: http://danfm.ca/emcee/#quickstart

import numpy as np
import emcee

def lnprob(x, mu, icov):
    diff = x-mu
    return -np.dot(diff,np.dot(icov,diff))/2.0

ndim = 10
means = np.random.rand(ndim)
cov  = 0.5-np.random.rand(ndim**2).reshape((ndim, ndim))
cov  = np.triu(cov)
cov += cov.T - np.diag(cov.diagonal())
cov  = np.dot(cov,cov)
icov = np.linalg.inv(cov)

nwalkers = 100
p0 = [np.random.rand(ndim) for i in xrange(nwalkers)]

sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=[means, icov])

pos, prob, state = sampler.run_mcmc(p0, 500)
sampler.reset()

sampler.run_mcmc(pos, 2000, rstate0=state)

print "Mean acceptance fraction:", np.mean(sampler.acceptance_fraction)

try:
    import matplotlib.pyplot as pl
except ImportError:
    print "Try installing matplotlib to generate some sweet plots..."
else:
    pl.hist(sampler.flatchain[:,0], 100)
    pl.show()
