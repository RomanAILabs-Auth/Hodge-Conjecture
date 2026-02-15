#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HC-Auto-Converge-Certainty.py
RomanAILabs - Auto-Converging Audit for
α′ = α − Σ_i [q_i * Z_i] with q_i = <α, Z_i> / ||Z_i||
Includes certainty % calculation based on residual shrink
Copyright Daniel Harding - RomanAILabs
"""

import hashlib
import numpy as np
import time

# -----------------------------
# CONFIGURATION
# -----------------------------
NUM_CYCLES = 5       # number of Z_i vectors
DIM = 4              # dimension of α and Z_i
DAMPING = 0.05       # fraction of projection applied per iteration
CONVERGENCE_THRESHOLD = 1e-3
MAX_ITERATIONS = 200  # safety cap to avoid infinite loops

# Initialize alpha and Z_i vectors
alpha = np.random.rand(DIM)
Z_cycles = [np.random.rand(DIM) for _ in range(NUM_CYCLES)]

# -----------------------------
# UTILITY FUNCTIONS
# -----------------------------
def alpha_hash(alpha):
    h = hashlib.sha256()
    h.update(alpha.tobytes())
    return h.hexdigest()

def norm(v):
    return np.linalg.norm(v)

def inner(a, b):
    return np.dot(a, b)

def compute_qi(alpha, Zi):
    """Compute q_i = <α, Zi> / ||Zi||"""
    return inner(alpha, Zi) / norm(Zi)

def compute_projection(alpha, Z_list):
    """Compute full projection Σ_i q_i * Z_i"""
    projection = np.zeros_like(alpha)
    for Zi in Z_list:
        qi = compute_qi(alpha, Zi)
        projection += qi * Zi
    return projection

# -----------------------------
# AUDIT ENGINE
# -----------------------------
print("🚀 ROMAN AI: AUTO-CONVERGING GENESIS PRIME AUDIT INITIALIZED")
print("Target Formula: α′ = α − Σ_i [q_i * Z_i] with q_i = <α, Z_i> / ||Z_i||")
print("-" * 60)

print(f"[*] Initial Alpha Hash: {alpha_hash(alpha)}")
initial_norm = np.linalg.norm(alpha)
print(f"[*] Initial Residual Norm: {initial_norm:.6f}\n")

iteration = 0
residual = initial_norm
while residual > CONVERGENCE_THRESHOLD and iteration < MAX_ITERATIONS:
    projection = compute_projection(alpha, Z_cycles)
    delta = DAMPING * projection
    alpha -= delta
    residual = np.linalg.norm(delta)
    iteration += 1
    print(f"   Iter {iteration:03d} | Residual Norm: {residual:.6f} | Status: Applying Projection")
    time.sleep(0.01)  # emulate computation

# -----------------------------
# CERTAINTY CALCULATION
# -----------------------------
certainty = min(100.0, (1 - residual / initial_norm) * 100)

# -----------------------------
# AUDIT RESULT
# -----------------------------
final_norm = np.linalg.norm(alpha)
print("\n" + "-"*60)
print(f"[*] Final Alpha Hash: {alpha_hash(alpha)}")
print(f"[*] Initial Norm: {initial_norm:.6f}, Final Norm: {final_norm:.6f}")
print(f"[*] Residual after {iteration} iterations: {residual:.6f}")
print(f"[*] CERTAINTY of stabilization: {certainty:.2f}%")

if residual < CONVERGENCE_THRESHOLD:
    print("✅ AUDIT PASSED: Projection stabilized within tolerance.")
else:
    print("❌ AUDIT FAILED: Projection residual still significant (increase iterations).")

