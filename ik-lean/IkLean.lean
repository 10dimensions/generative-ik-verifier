import IkLean.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2
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

def x : ℝ := l1 * cos(theta1) + l2 * cos(theta1 + theta2)

def y : ℝ := l1 * sin(theta1) + l2 * sin(theta1 + theta2)

/-! ==================== JACOBIAN ==================== -/

def J : Matrix (Fin 2) (Fin 2) ℝ :=
![-l1 * sin(theta1) - l2 * sin(theta1 + theta2), -l2 * sin(theta1 + theta2);
      l1 * cos(theta1) + l2 * cos(theta1 + theta2), l2 * cos(theta1 + theta2)]

/-! ==================== VELOCITIES ==================== -/

def x_dot : ℝ := (-l1 * sin(theta1) - l2 * sin(theta1 + theta2)) * dtheta1 + (-l2 * sin(theta1 + theta2)) * dtheta2

def y_dot : ℝ := (l1 * cos(theta1) + l2 * cos(theta1 + theta2)) * dtheta1 + (l2 * cos(theta1 + theta2)) * dtheta2

/-! ==================== DYNAMICS ==================== -/

def M : Matrix (Fin 2) (Fin 2) ℝ :=
![I1 + I2 + m1 * lc1^2 + m2 * (l1^2 + lc2^2 + 2 * l1 * lc2 * cos(theta2)), I2 + m2 * (lc2^2 + l1 * lc2 * cos(theta2));
      I2 + m2 * (lc2^2 + l1 * lc2 * cos(theta2)), I2 + m2 * lc2^2]

def C : Matrix (Fin 2) (Fin 1) ℝ :=
![-m2 * l1 * lc2 * sin(theta2) * dtheta2, -m2 * l1 * lc2 * sin(theta2) * (dtheta1 + dtheta2);
      m2 * l1 * lc2 * sin(theta2) * dtheta1, 0]

def G : Matrix (Fin 2) (Fin 1) ℝ :=
![-(m1 * lc1 + m2 * l1) * g * sin(theta1) - m2 * lc2 * g * sin(theta1 + theta2);
      -m2 * lc2 * g * sin(theta1 + theta2)]

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
