import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class LogisticPCA(nn.Module):
    """
    Standard Logistic PCA for binary data.
    
    Attributes:
        n_features (int): Number of input features (d).
        n_components (int): Number of principal components (k).
    """
    def __init__(self, n_features, n_components, m=5):
        super(LogisticPCA, self).__init__()
        self.n_components = n_components
        self.m = m  

        # Parameters
        self.mu = nn.Parameter(torch.zeros(n_features))  
        self.U = nn.Parameter(torch.randn(n_features, n_components) * 0.01)  

    def forward(self, X):
        theta_tilde = self.m * (2 * X - 1)
        Z = torch.matmul(theta_tilde - self.mu, self.U)
        theta_hat = self.mu + torch.matmul(Z, self.U.T)  

        P_hat = torch.sigmoid(theta_hat)
        return P_hat, theta_hat

    def fit(self, X, epochs=500, lr=0.01, verbose=True):
        optimizer = optim.Adam(self.parameters(), lr=lr)
        criterion = nn.BCELoss()

        for epoch in range(epochs):
            optimizer.zero_grad()
            P_hat, _ = self.forward(X)
            loss = criterion(P_hat, X)
            loss.backward()
            optimizer.step()

            if verbose and epoch % 50 == 0:
                print(f"Epoch {epoch}/{epochs}, Loss: {loss.item():.4f}")

    def transform(self, X):
        with torch.no_grad():
            theta_tilde = self.m * (2 * X - 1)
            Z = torch.matmul(theta_tilde - self.mu, self.U)
            return Z.numpy()

    def inverse_transform(self, X_low_dim):
        with torch.no_grad():
            theta_hat_reconstructed = self.mu + torch.matmul(X_low_dim, self.U.T)
            P_hat_reconstructed = torch.sigmoid(theta_hat_reconstructed)
            return P_hat_reconstructed.numpy()


class SparseLogisticPCA(nn.Module):
    """
    Sparse Logistic PCA with L1 regularization for binary data.
    
    Attributes:
        n_features (int): Number of input features (d).
        n_components (int): Number of principal components (k).
        lambda_L1 (float): Regularization strength for sparsity.
    """
    def __init__(self, n_features, n_components, m=5, lambda_L1=0.01):
        super(SparseLogisticPCA, self).__init__()
        self.n_components = n_components
        self.m = m  
        self.lambda_L1 = lambda_L1  

        # Parameters
        self.mu = nn.Parameter(torch.zeros(n_features))  
        self.U = nn.Parameter(torch.randn(n_features, n_components) * 0.01)  

    def forward(self, X):
        theta_tilde = self.m * (2 * X - 1)  
        Z = torch.matmul(theta_tilde - self.mu, self.U)  
        theta_hat = self.mu + torch.matmul(Z, self.U.T)  

        P_hat = torch.sigmoid(theta_hat)
        return P_hat, theta_hat

    def fit(self, X, epochs=500, lr=0.01, verbose=True):
        optimizer = optim.Adam(self.parameters(), lr=lr)
        criterion = nn.BCELoss()

        for epoch in range(epochs):
            optimizer.zero_grad()
            P_hat, _ = self.forward(X)
            loss = criterion(P_hat, X)

            # Add L1 sparsity penalty
            l1_penalty = self.lambda_L1 * torch.norm(self.U, p=1)  
            loss += l1_penalty
            
            loss.backward()
            optimizer.step()

            if verbose and epoch % 50 == 0:
                print(f"Epoch {epoch}/{epochs}, Loss: {loss.item():.4f}, L1 Penalty: {l1_penalty.item():.4f}")

    def transform(self, X):
        with torch.no_grad():
            theta_tilde = self.m * (2 * X - 1)
            Z = torch.matmul(theta_tilde - self.mu, self.U)
            return Z.numpy()

    def inverse_transform(self, X_low_dim):
        with torch.no_grad():
            theta_hat_reconstructed = self.mu + torch.matmul(X_low_dim, self.U.T)
            P_hat_reconstructed = torch.sigmoid(theta_hat_reconstructed)
            return P_hat_reconstructed.numpy()
            
            
            
class LatentSparseLogisticPCA(nn.Module):
    """
    Logistic PCA with L1 regularization on latent factors (Z) for binary data.

    Attributes:
        n_features (int): Number of input features (d).
        n_components (int): Number of principal components (k).
        lambda_L1 (float): Regularization strength on Z.
    """
    def __init__(self, n_features, n_components, m=5, lambda_L1=0.01):
        super(LatentSparseLogisticPCA, self).__init__()
        self.n_components = n_components
        self.m = m
        self.lambda_L1 = lambda_L1

        # Parameters
        self.mu = nn.Parameter(torch.zeros(n_features))
        self.U = nn.Parameter(torch.randn(n_features, n_components) * 0.01)

    def forward(self, X):
        theta_tilde = self.m * (2 * X - 1)
        Z = torch.matmul(theta_tilde - self.mu, self.U)
        theta_hat = self.mu + torch.matmul(Z, self.U.T)
        P_hat = torch.sigmoid(theta_hat)
        return P_hat, Z

    def fit(self, X, epochs=500, lr=0.01, verbose=True):
        optimizer = optim.Adam(self.parameters(), lr=lr)
        criterion = nn.BCELoss()

        for epoch in range(epochs):
            optimizer.zero_grad()
            P_hat, Z = self.forward(X)
            loss = criterion(P_hat, X)

            # L1 regularization on Z (latent scores)
            l1_penalty = self.lambda_L1 * torch.norm(Z, p=1)
            loss += l1_penalty

            loss.backward()
            optimizer.step()

            if verbose and epoch % 50 == 0:
                print(f"Epoch {epoch}/{epochs}, Loss: {loss.item():.4f}, L1(Z) Penalty: {l1_penalty.item():.4f}")

    def transform(self, X):
        with torch.no_grad():
            theta_tilde = self.m * (2 * X - 1)
            Z = torch.matmul(theta_tilde - self.mu, self.U)
            return Z.numpy()

    def inverse_transform(self, X_low_dim):
        with torch.no_grad():
            theta_hat = self.mu + torch.matmul(X_low_dim, self.U.T)
            return torch.sigmoid(theta_hat).numpy()


import torch
import torch.nn as nn
import torch.optim as optim

class LogisticPCA_SVT(nn.Module):
    """
    Logistic PCA with GDP-penalized low-rank logit structure.
    Based on: Song et al., Chemometrics and Intelligent Laboratory Systems, 2020.

    Θ = 1μᵀ + ABᵀ is the natural parameter matrix (logits), 
    P = sigmoid(Θ) is the probability matrix for Bernoulli likelihood.

    GDP penalty is applied to the singular values of Z = ABᵀ to reduce overfitting.
    """
    def __init__(self, n_samples, n_features, n_components, gamma=1.0, lambda_reg=0.1, missing_mask=None):
        super().__init__()
        self.n_samples = n_samples
        self.n_features = n_features
        self.n_components = n_components
        self.gamma = gamma
        self.lambda_reg = lambda_reg

        self.A = nn.Parameter(torch.randn(n_samples, n_components) * 0.01)  # Scores (latent rows)
        self.B = nn.Parameter(torch.randn(n_features, n_components) * 0.01)  # Loadings (latent cols)
        self.mu = nn.Parameter(torch.zeros(n_features))  # Intercept (logit of marginals)

        # Optional missing value mask
        if missing_mask is not None:
            self.register_buffer("W", missing_mask.float())
        else:
            self.W = None

    def forward(self):
        Z = torch.matmul(self.A, self.B.T)
        Theta = Z + self.mu  # Broadcasting mu
        P = torch.sigmoid(Theta)
        return P, Z

    def compute_loss(self, X):
        P, Z = self.forward()
        if self.W is not None:
            bce = nn.BCELoss(reduction='none')(P, X)
            bce = (bce * self.W).sum() / self.W.sum()
        else:
            bce = nn.BCELoss()(P, X)

        _, S, _ = torch.linalg.svd(Z, full_matrices=False)
        gdp_penalty = torch.sum(torch.log1p(S / self.gamma))
        return bce + self.lambda_reg * gdp_penalty

    def update_mu(self, X):
        with torch.no_grad():
            if self.W is not None:
                mu_update = (X * self.W).sum(dim=0) / self.W.sum(dim=0)
            else:
                mu_update = X.mean(dim=0)
            mu_update = torch.clamp(mu_update, min=1e-6, max=1 - 1e-6)
            self.mu.copy_(torch.log(mu_update / (1 - mu_update)))

    def fit(self, X, epochs=500, lr=0.01, verbose=True):
        self.update_mu(X)
        optimizer = optim.Adam(self.parameters(), lr=lr)
        for epoch in range(epochs):
            optimizer.zero_grad()
            loss = self.compute_loss(X)
            loss.backward()
            optimizer.step()
            if verbose and epoch % 50 == 0:
                print(f"Epoch {epoch}/{epochs} | Loss: {loss.item():.4f}")

    def transform(self, A_tensor=None):
        with torch.no_grad():
            A_out = self.A if A_tensor is None else A_tensor
            return A_out.detach().cpu().numpy()

    def inverse_transform(self, A_tensor=None):
        with torch.no_grad():
            A_in = self.A if A_tensor is None else A_tensor
            Theta = torch.matmul(A_in, self.B.T) + self.mu
            return torch.sigmoid(Theta).detach().cpu().numpy()

class CollinsLogisticPCA(nn.Module):
    """
    Exponential Family PCA (Collins et al., 2001) for binary data.
    
    Model: logit(P) = mu + A * B^T
    where A is n x k (scores), B is d x k (loadings), mu is d-dim intercepts
    """
    def __init__(self, n_features, n_components):
        super(CollinsLogisticPCA, self).__init__()
        self.n_features = n_features
        self.n_components = n_components
        
        # Parameters - will be initialized when fit() is called
        self.mu = None
        self.A = None  # n_samples x n_components (scores)
        self.B = None  # n_features x n_components (loadings)
        
    def _initialize_parameters(self, n_samples):
        """Initialize parameters based on data size"""
        self.mu = nn.Parameter(torch.zeros(self.n_features))
        self.A = nn.Parameter(torch.randn(n_samples, self.n_components) * 0.1)
        self.B = nn.Parameter(torch.randn(self.n_features, self.n_components) * 0.1)
        
    def forward(self):
        """Compute probabilities P = sigmoid(mu + A * B^T)"""
        theta = self.mu.unsqueeze(0) + torch.mm(self.A, self.B.T)
        return torch.sigmoid(theta), theta
        
    def fit(self, X, epochs=500, lr=0.01, verbose=True):
        """
        Fit the Collins Exponential Family PCA model
        
        Args:
            X: Binary data matrix (n_samples x n_features)
            epochs: Number of optimization epochs
            lr: Learning rate
            verbose: Print progress
        """
        X = torch.FloatTensor(X)
        n_samples = X.shape[0]
        
        # Initialize parameters
        self._initialize_parameters(n_samples)
        
        optimizer = optim.Adam(self.parameters(), lr=lr)
        
        for epoch in range(epochs):
            optimizer.zero_grad()
            
            # Forward pass
            probs, theta = self.forward()
            
            # Bernoulli negative log-likelihood
            # -LL = -sum(X * theta - log(1 + exp(theta)))
            log_lik = X * theta - torch.log(1 + torch.exp(torch.clamp(theta, -10, 10)))
            loss = -log_lik.sum()
            
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.parameters(), max_norm=1.0)
            optimizer.step()
            
            if verbose and epoch % 50 == 0:
                print(f"Epoch {epoch}/{epochs}, Loss: {loss.item():.4f}")
                
    def transform(self, X):
        """
        Transform data to latent space (get scores)
        For new data, optimizes A while keeping B, mu fixed
        """
        if not hasattr(self, 'mu') or self.mu is None:
            raise ValueError("Model must be fitted before transform")
            
        X = torch.FloatTensor(X)
        n_samples = X.shape[0]
        
        # For new data, optimize new A matrix
        A_new = nn.Parameter(torch.randn(n_samples, self.n_components) * 0.1)
        optimizer = optim.Adam([A_new], lr=0.1)
        
        # Keep B and mu fixed
        B_fixed = self.B.detach()
        mu_fixed = self.mu.detach()
        
        # Quick optimization for new scores
        for _ in range(100):
            optimizer.zero_grad()
            theta = mu_fixed.unsqueeze(0) + torch.mm(A_new, B_fixed.T)
            log_lik = X * theta - torch.log(1 + torch.exp(torch.clamp(theta, -10, 10)))
            loss = -log_lik.sum()
            loss.backward()
            optimizer.step()
            
        return A_new.detach().numpy()
    
    def inverse_transform(self, A_scores):
        """Reconstruct probabilities from latent scores"""
        if not hasattr(self, 'B') or self.B is None:
            raise ValueError("Model must be fitted before inverse_transform")
            
        A_scores = torch.FloatTensor(A_scores)
        with torch.no_grad():
            theta = self.mu.unsqueeze(0) + torch.mm(A_scores, self.B.T)
            probs = torch.sigmoid(theta)
        return probs.numpy()
        
    @property
    def components_(self):
        """Get loadings (B matrix) - similar to sklearn interface"""
        if self.B is None:
            return None
        return self.B.detach().numpy().T  # Transpose to match sklearn convention
        
    @property
    def scores_(self):
        """Get training scores (A matrix)"""
        if self.A is None:
            return None
        return self.A.detach().numpy()

