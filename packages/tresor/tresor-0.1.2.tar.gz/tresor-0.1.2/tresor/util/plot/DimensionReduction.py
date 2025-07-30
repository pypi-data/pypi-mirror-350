__version__ = "0.0.1"
__copyright__ = "Copyright 2025"
__license__ = "GPL-3.0"


import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class DimensionReduction:

    def __init__(self, ):
        pass

    def single(self, X, y, tech='TSNE', marker_size=2, cmap='tab20b', title=''):
        """https://matplotlib.org/stable/tutorials/colors/colormaps.html"""
        sns.set(font="Helvetica")
        sns.set_style("ticks")
        if tech == 'PCA':
            from sklearn.decomposition import PCA
            retech = PCA(n_components=2)
            embeddings = retech.fit_transform(np.array(X))

        elif tech == 'TSNE':
            from sklearn.manifold import TSNE
            retech = TSNE(n_components=2)
            embeddings = retech.fit_transform(np.array(X))

        elif tech == 'UMAP':
            import umap
            retech = umap.UMAP(n_components=2)
            embeddings = retech.fit_transform(np.array(X))

        else:
            embeddings = np.array(X)
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        sp = ax.scatter(
            embeddings[:, 0], embeddings[:, 1],
            c=y,
            s=marker_size,
            cmap=plt.cm.get_cmap(cmap, 10),
        )
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_xlabel(tech + ' 1', fontsize=14)
        ax.set_ylabel(tech + ' 2', fontsize=14)
        ax.set_title(title, fontsize=14)
        fig.colorbar(sp)
        fig.subplots_adjust(
            # top=0.92,
            # bottom=0.13,
            # left=0.13,
            # right=0.95,
            # hspace=0.20,
            # wspace=0.15
        )
        plt.show()