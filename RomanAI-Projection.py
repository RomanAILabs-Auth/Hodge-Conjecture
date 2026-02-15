#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
romanai_projection.py
RomanAILabs - Drop-in module for α′ = α − Σ_i [q_i * Z_i] with q_i = <α, Z_i> / ||Z_i||
Includes GENESIS PRIME-style audit function
Copyright Daniel Harding - RomanAILabs
"""

import hashlib
import numpy as np
import time

# -----------------------------
# UTILITY FUNCTIONS
# -----------------------------
def alpha_hash(alpha):
    """Return SHA256 hash of vector alpha"""
    h = hashlib.sha256()
    h.update(alpha.tobytes())
    return h.hexdigest()

def norm(v):
    """Euclidean norm of a vector"""
    return np.linalg.norm(v)

def inner(a, b):
    """Dot product of two vectors"""
    return np.dot(a, b)

def compute_qi(alpha, Zi):
    """Compute q_i = <alpha, Zi> / ||Zi||"""
    return inner(alpha, Zi) / norm(Zi)

def compute_projection(alpha, Z_list):
    """Compute Σ_i q_i * Z_i"""
    projection = np.zeros_like(alpha)
    for Zi in Z_list:
        qi = compute_qi(alpha, Zi)
        projection += qi * Zi
    return projection

# -----------------------------
# AUDIT FUNCTION
# -----------------------------
def romanai_audit(alpha, Z_cycles, damping=0.05, threshold=1e-3, max_iter=200, verbose=True):
    """
    GENESIS PRIME-style audit for α′ = α − Σ_i [q_i * Z_i]
    Returns: final_alpha, residual, certainty %
    """
    alpha = np.array(alpha, dtype=float)
    Z_cycles = [np.array(Zi, dtype=float) for Zi in Z_cycles]
    
    initial_norm = norm(alpha)
    residual = initial_norm
    iteration = 0
    
    if verbose:
        print("🚀 ROMAN AI: AUTO-CONVERGING GENESIS PRIME AUDIT MODULE")
        print(f"[*] Initial Alpha Hash: {alpha_hash(alpha)}")
        print(f"[*] Initial Residual Norm: {initial_norm:.6f}\n")
    
    while residual > threshold and iteration < max_iter:
        projection = compute_projection(alpha, Z_cycles)
        delta = damping * projection
        alpha -= delta
        residual = norm(delta)
        iteration += 1
        if verbose:
            print(f"   Iter {iteration:03d} | Residual Norm: {residual:.6f} | Status: Applying Projection")
            time.sleep(0.01)
    
    certainty = min(100.0, (1 - residual / initial_norm) * 100)
    final_norm = norm(alpha)
    
    if verbose:
        print("\n" + "-"*60)
        print(f"[*] Final Alpha Hash: {alpha_hash(alpha)}")
        print(f"[*] Initial Norm: {initial_norm:.6f}, Final Norm: {final_norm:.6f}")
        print(f"[*] Residual after {iteration} iterations: {residual:.6f}")
        print(f"[*] CERTAINTY of stabilization: {certainty:.2f}%")
        if residual < threshold:
            print("✅ AUDIT PASSED: Projection stabilized within tolerance.")
        else:
            print("❌ AUDIT FAILED: Projection residual still significant (increase iterations).")
    
    return alpha, residual, certainty

# -----------------------------
# QUICK TEST FUNCTION
# -----------------------------
def test_module():
    """Quick internal test for drop-in module"""
    DIM = 4
    NUM_CYCLES = 5
    alpha = np.random.rand(DIM)
    Z_cycles = [np.random.rand(DIM) for _ in range(NUM_CYCLES)]
    
    romanai_audit(alpha, Z_cycles)

# Run test if module executed directly
if __name__ == "__main__":
    test_module()

