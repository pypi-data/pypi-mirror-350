import numpy as np
from scipy.linalg import solve, inv

def prob_pca(X, num_components=None, num_iter=32):
    """
    Probabilistic PCA (PPCA) using Variational Inference.

    Parameters
    ----------
    X : (num_samples, num_dimensions) ndarray
        Data matrix.
    num_components : int, optional
        Number of PCA components.
    num_iter : int, default=32
        Number of iterations for fitting the model.

    Returns
    ----------
    W : (num_dimensions, num_components) ndarray
        Estimated projection matrix.
    mu : (num_components, num_samples) ndarray
        Estimated latent variables.
    b : (num_dimensions, 1) ndarray
        Estimated bias.

    Reference
    ----------
    Tipping, Michael E. "Probabilistic visualisation of high-dimensional binary data." 
    Advances in neural information processing systems (1999): 592-598.
    """
    num_samples, num_dimensions = X.shape
    num_components = num_components or min(num_samples, num_dimensions)

    N, D, K = num_samples, num_dimensions, num_components
    I = np.eye(K)
    W = np.random.randn(D, K)
    mu = np.random.randn(K, N)
    b = np.random.randn(D, 1)    
    C = np.repeat(I[:, :, np.newaxis], N, axis=2)
    xi = np.ones((N, D))  # Variational parameters

    # Functions
    sig = lambda x: 1/(1 + np.exp(-x))
    lam = lambda x: (0.5 - sig(x)) / (2*x)

    # Fit model
    for _ in range(num_iter):
        # Step 1: Update latent variable expectations
        for n in range(N):
            x_n = X[n, :][:, None]
            lam_n = lam(xi[n, :])[:, None]
            C[:, :, n] = inv(I - 2 * W.T @ (lam_n * W))
            mu[:, n] = (C[:, :, n] @ (W.T @ (x_n - 0.5 + 2 * lam_n * b)))[:, 0]

        # Step 2: Update variational parameters
        for n in range(N):
            z = mu[:, n][:, None]
            E_zz = C[:, :, n] + z @ z.T
            xixi = np.sum(W * (W @ E_zz), axis=1, keepdims=True) + 2 * b * (W @ z) + b**2
            xi[n, :] = np.sqrt(np.abs(xixi[:, 0]))

        # Step 3: Update model parameters
        E_zhzh = np.zeros((K + 1, K + 1, N))
        for n in range(N):
            z = mu[:, n][:, None]
            E_zhzh[:-1, :-1, n] = C[:, :, n] + z @ z.T
            E_zhzh[:-1, -1, n] = z[:, 0]
            E_zhzh[-1, :-1, n] = z[:, 0]
            E_zhzh[-1, -1, n] = 1
        E_zh = np.append(mu, np.ones((1, N)), axis=0)

        for i in range(D):
            lam_i = lam(xi[:, i])[None][None]
            H = np.sum(2 * lam_i * E_zhzh, axis=2)
            g = E_zh @ (X[:, i] - 0.5)
            wh_i = -solve(H, g[:, None])[:, 0]
            W[i, :] = wh_i[:K]
            b[i] = wh_i[K]

    return W, mu, b

