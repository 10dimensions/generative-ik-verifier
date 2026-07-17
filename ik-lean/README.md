# 2-Link Robotic Arm Mathematical Model

This project generates a complete symbolic mathematical model for a **2-link planar robotic arm (2R manipulator)** and converts it into Lean 4 code for formal verification.

## Overview

The workflow consists of three main steps:

1. **Generate JSON Model**  
   A detailed system prompt is used to create a symbolic mathematical model (forward kinematics, Jacobian, velocities, and full dynamics) expressed as Python/SymPy compatible strings in JSON format.

2. **JSON Model**  
   The model includes:
   - Forward kinematics (`x`, `y`)
   - Jacobian matrix
   - End-effector velocities
   - Dynamic model: Inertia matrix `M`, Coriolis/centrifugal `C`, Gravity `G`, and torque `τ`

3. **Python Parser → Lean 4**  
   A Python script reads the JSON file and automatically translates the mathematical expressions into a valid **Lean 4** file (`TwoLinkArm.lean`) using Mathlib.

## Files

- `two_link_model.json` — Symbolic model (SymPy expressions)
- `generate_lean.py` — Parser that converts JSON → Lean 4 code
- `TwoLinkArm.lean` — Generated Lean 4 formalization

## Purpose

The Lean 4 code allows formal verification of the robotic arm model, including:
- Correctness of kinematics and dynamics equations
- Symmetry of the inertia matrix `M`
- Future proofs (positive definiteness, energy conservation, etc.)

## Workflow Summary

1. AI generates accurate mathematical model in JSON format.
2. Python parser translates expressions from SymPy syntax to Lean syntax.
3. Lean 4 file is produced for formal verification in theorem prover.

## How to Use

1. Run the Python script with the JSON model:
   ```bash
   python generate_lean.py