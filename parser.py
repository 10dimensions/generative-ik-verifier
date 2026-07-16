import json
import re
import sys
from pathlib import Path

def sympy_to_lean(expr: str) -> str:
    """Translate SymPy-style Python expression to Lean 4 syntax."""
    if not expr or expr.strip() == "":
        return "0"
    
    # Basic replacements
    replacements = {
        'sympy.sin': 'sin',
        'sympy.cos': 'cos',
        'sympy.Matrix': '',  # We'll handle matrices manually
        '**': '^',
        '*': ' * ',
        ' + ': ' + ',
        ' - ': ' - ',
    }
    
    lean_expr = expr.strip()
    
    # Apply replacements
    for old, new in replacements.items():
        lean_expr = lean_expr.replace(old, new)
    
    # Clean spacing
    lean_expr = re.sub(r'\s+', ' ', lean_expr)
    lean_expr = lean_expr.replace('( ', '(').replace(' )', ')')
    
    # Handle list of lists -> Matrix
    if lean_expr.startswith('[[[') or lean_expr.startswith('[['):
        # Simple 2x2 matrix case
        lean_expr = lean_expr.replace('[[', '![').replace(']]', ']')
        lean_expr = re.sub(r'],\s*\[', ';\n      ', lean_expr)
    
    return lean_expr.strip()


def generate_lean_parser(json_path: str, output_path: str = "TwoLinkArm.lean"):
    with open(json_path, 'r', encoding='utf-8') as f:
        model = json.load(f)

    # Build Lean code dynamically from JSON
    lean = """import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Calculus.Deriv.Basic

/-!
# 2-Link Planar Robotic Arm
Automatically generated from JSON mathematical model.
-/

namespace TwoLinkArm

variable (l1 l2 m1 m2 g : ℝ)
variable (θ₁ θ₂ : ℝ)
variable (θ̇₁ θ̇₂ : ℝ)
variable (θ̈₁ θ̈₂ : ℝ)
variable (I1 I2 lc1 lc2 : ℝ)

variable (h_pos : 0 < l1 ∧ 0 < l2)
variable (h_mass : 0 < m1 ∧ 0 < m2)
variable (h_inertia : 0 < I1 ∧ 0 < I2)

/-! ==================== FORWARD KINEMATICS ==================== -/

def x : ℝ := """ + sympy_to_lean(model["forward_kinematics"]["x"]) + """

def y : ℝ := """ + sympy_to_lean(model["forward_kinematics"]["y"]) + """

/-! ==================== JACOBIAN ==================== -/

def J : Matrix (Fin 2) (Fin 2) ℝ := 
""" + sympy_to_lean(model["jacobian"]["linear"]) + """

/-! ==================== VELOCITIES ==================== -/

def x_dot : ℝ := """ + sympy_to_lean(model["velocities"]["x_dot"]) + """

def y_dot : ℝ := """ + sympy_to_lean(model["velocities"]["y_dot"]) + """

/-! ==================== DYNAMICS ==================== -/

def M : Matrix (Fin 2) (Fin 2) ℝ :=
""" + sympy_to_lean(model["dynamics"]["M"]) + """

def C : Matrix (Fin 2) (Fin 1) ℝ :=
""" + sympy_to_lean(model["dynamics"]["C"]) + """

def G : Matrix (Fin 2) (Fin 1) ℝ :=
""" + sympy_to_lean(model["dynamics"]["G"]) + """

def τ : Matrix (Fin 2) (Fin 1) ℝ := 
  M *ᵥ !![θ̈₁; θ̈₂] + C *ᵥ !![θ̇₁; θ̇₂] + G

/-! ==================== VERIFICATION ==================== -/

theorem M_is_symmetric : M = Mᵀ := by
  simp [M]
  ring

#check x
#check y
#check M
#check τ
#check M_is_symmetric

end TwoLinkArm
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(lean)

    print(f"✅ Successfully generated Lean file: {output_path}")
    print("The Lean code was **parsed and translated** from your JSON model.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        json_file = "two_link_model.json"
    
    if not Path(json_file).exists():
        print(f"Error: File {json_file} not found.")
        print("Please save your JSON model first.")
    else:
        generate_lean_parser(json_file)
