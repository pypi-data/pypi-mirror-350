__version__ = "0.0.1"
__copyright__ = "Copyright 2025"
__license__ = "GPL-3.0"
__developer__ = "Jianfeng Sun"
__maintainer__ = "Jianfeng Sun"
__email__ = "jianfeng.sunmt@gmail.com"


import numpy as np
from functools import wraps
from tresor.util.Console import Console


class Number:

    def __init__(
            self,
            *args,
            **kwargs,
    ):
        self.args = args
        self.kwargs = kwargs
        self.console = Console()

    def __call__(self, deal):
        if self.kwargs['type'] == 'binomial':
            distrib = self.binomial
        if self.kwargs['type'] == 'uniform':
            distrib = self.binomial
        else:
            pass
        @wraps(deal)
        def switch(ph, *args, **kwargs):
            if 'verbose' in kwargs['params'].keys():
                self.console.verbose = kwargs['params']['verbose']
            else:
                self.console.verbose = True
            self.console.print('======>numbering...')
            # print(kwargs)
            res = deal(ph, **kwargs)
            res['spl_num'] = distrib(
                n=len(res['data']),
                p=res['ampl_rate'],
            )
            # print(res)
            return res
        return switch

    def binomial(self, n, p, use_seed=True, seed=1):
        if use_seed:
            state = np.random.RandomState(seed)
            return state.binomial(
                n,
                p,
            )
        else:
            return np.random.binomial(
                n,
                p,
            )

    def nbinomial(self, n, p, use_seed=True, seed=1):
        """

        Parameters
        ----------
        n
            the number of success to be expected, better, n = the total number of trails * p
        p
            the prob of success
        use_seed
        seed

        Returns
        -------

        """
        if use_seed:
            state = np.random.RandomState(seed)
            return state.negative_binomial(
                n,
                p,
            )
        else:
            return np.random.negative_binomial(
                n,
                p,
            )

    def uniform(self, low, high, num, use_seed=True, seed=1):
        if use_seed:
            state = np.random.RandomState(seed)
            return state.randint(
                low=low,
                high=high,
                size=num
            )
        else:
            return np.random.randint(
                low=low,
                high=high,
                size=num
            )

    # def choice(self, high, num, replace=False):
    #     from numpy.random import default_rng
    #     rng = default_rng()
    #     return rng.choice(high, size=num, replace=replace)

    def choice(self, high, num, use_seed=True, seed=1, replace=False):
        if use_seed:
            state = np.random.RandomState(seed)
            return state.choice(high, int(num), replace=replace)
        else:
            return np.random.choice(high, int(num), replace=replace)