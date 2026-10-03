# Physics Misconceptions Dataset Schema

**Specification Version**: `1.0.0`  
**Primary Owner**: Member 2 (Physics Dataset & Intervention Content)  
**File Location**: `data/physics_misconceptions.csv` (gitignored, kept locally)

---

## 1. Schema Definition

The training and validation dataset must be a comma-separated values (CSV) file containing the following fields:

| Field Name | Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `question_id` | String | Yes | Unique identifier for the question prompt | `"Q_NEWTON_01"` |
| `topic` | String | Yes | Physics sub-domain | `"Newtonian Mechanics"`, `"Kinematics"` |
| `question` | String | Yes | The conceptual physics question presented to the student | `"A hockey puck slides on ice after being hit. What keeps it moving?"` |
| `correct_answer` | String | Yes | The canonical scientifically correct explanation | `"No force is required; it continues due to inertia."` |
| `student_answer` | String | Yes | Natural language response written by the student | `"The forward force from the stick stays inside the puck."` |
| `misconception_label` | String | Yes | Standardized categorical identifier for the misconception | `"impetus_force_persistence"` |
| `misconception_explanation` | String | No | Pedagogical explanation of why this answer is incorrect | `"Confuses velocity with requiring a continuous force."` |
| `difficulty_level` | String | No | Target student level (`"introductory"`, `"intermediate"`, `"advanced"`) | `"introductory"` |

---

## 2. Standard Misconception Taxonomy (Examples)

Member 2 is responsible for expanding and maintaining this taxonomy:

1. `impetus_force_persistence`
   - **Belief**: Motion implies an internal or carried force; an object stops when its "impetus" runs out.
   - **Physics Principle**: Newton's First Law (Inertia).
2. `heavier_objects_fall_faster`
   - **Belief**: Heavier masses always accelerate faster under gravity in a vacuum.
   - **Physics Principle**: Gravitational acceleration independence of mass ($g = G M / r^2$).
3. `acceleration_zero_at_top`
   - **Belief**: When an object thrown upward reaches velocity zero at its peak, its acceleration is also zero.
   - **Physics Principle**: Gravity acts continuously ($a = -9.8\text{ m/s}^2$).
4. `action_reaction_same_object`
   - **Belief**: Newton's third law force pairs cancel each other out on the same object.
   - **Physics Principle**: Action-reaction forces act on two distinct objects.
5. `no_misconception_detected`
   - **Belief**: The student's answer demonstrates conceptual correctness.

---

## 3. Data Integrity & Validation Rules

- **No Nulls in Core Fields**: `question`, `student_answer`, and `misconception_label` must not be null or whitespace only.
- **Lowercase Snake_Case for Labels**: All `misconception_label` values must follow `lowercase_snake_case` (e.g., `impetus_force_persistence`).
- **Encoding**: File must be UTF-8 encoded.
- **Class Balance**: For training with Logistic Regression, aim for at least 15–20 answer variations per misconception class to avoid extreme imbalance.
