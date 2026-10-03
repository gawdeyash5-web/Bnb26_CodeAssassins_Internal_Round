# Re:Learn - Physics Dataset Guide (Newton's Laws and Forces)

Prepared for **Member 2 (Physics/Data Lead)**. Everything in this guide is generated from the same source data as the CSV and JSON files, so the IDs and numbers always match.

> **Important honesty note:** all student answers are **author-written (synthetic)**, not collected from real students. They are realistic, but they are not real data. If you can, test the system with a few real classmates before the demo.

## 0. What is in this package

| File | What it is | Who uses it |
|---|---|---|
| `relearn_dataset.csv` / `.json` | 70 labelled student responses (55 wrong, 15 correct), exact 18 columns | Member 1 (ML), Member 4 (QA) |
| `split_assignments.csv` | Which row is train / validation / test (leak-safe) | Member 1 |
| `misconceptions.json` | The 5 misconception definitions (Part 1) | Everyone |
| `intervention_bank.json` / `.csv` | One targeted explanation plan per misconception (Part 8) | Member 3, Member 4 |
| `reassessment_bank.json` / `.csv` | 25 fresh follow-up questions (Part 9) | Member 3, Member 4 |
| `resolution_rules.json` | Rules for 'appears resolved' (Part 10) | Member 4 |
| this guide | Explanations, checks, handoff notes | You |

### What each column means (in simple language)

| Column | Plain meaning |
|---|---|
| question_id | Unique ID of the row (Q001...). |
| topic / subtopic | The big topic, and which Newton's law the question is about. |
| difficulty | Easy, Medium or Hard. |
| question / question_type | The question text, and its style (multiple-choice, numerical...). |
| correct_answer | The right answer, with the reason. |
| student_answer | What the (synthetic) student wrote. This is what the AI will read. |
| is_correct | true if the student's reasoning is right, false if not. |
| misconception_id / misconception_name | The label: M1 to M5, or NONE when the answer is correct. |
| reasoning_error | The faulty thinking behind the wrong answer, in one line. |
| explanation | A short explanation aimed at that exact mistake. |
| real_life_example | A familiar example that makes the idea concrete. |
| follow_up_question / follow_up_answer / follow_up_difficulty | A new question to check understanding afterwards, with its answer and level. |
| source_or_reason | Why this row exists (it is synthetic) and which mistake pattern it shows. |

## Parts 2-6, 11: the labelled dataset

- **70 rows**: 11 per misconception (M1-M5) plus **15 correct answers** (label NONE).
- Difficulty mix: Easy 17, Medium 32, Hard 21.
- Question types: Conceptual 11, Numerical 25, Reasoning/Explanation 11, Short-answer 4, Scenario-based 10, Multiple-choice 9.
- Rows are shuffled, so the file is not sorted by label.
- Multiple-choice options are written inside the `question` text as (A) (B) (C) (D).
- Open `relearn_dataset.csv` in Excel or Google Sheets, or load the JSON in Python (see Part 12).

## Part 1 - The five misconceptions

### M1 - Force required for motion

- **Simple description:** The student thinks an object only keeps moving if something keeps pushing it in the direction it is going.
- **Scientifically correct idea:** An object keeps its velocity (same speed, same direction) unless a net force acts on it. A net force is needed to CHANGE velocity (a = F_net / m), not to maintain it. Objects slow down on Earth because friction and air resistance are forces.
- **Common reasoning error:** Everyday objects stop when we stop pushing, so the student concludes that motion needs a continuous force. They overlook friction and air resistance, or imagine a force is 'stored' in a moving object (the impetus idea).
- **Simple intervention:** A force is needed to CHANGE how something moves (speed up, slow down, turn), not to KEEP it moving. If nothing pushes or pulls it, an object keeps moving at the same velocity.
- **Real-life analogy:** A skater gliding on smooth ice after one push does not need anyone pushing her every second. On a rough road she would stop because the road drags her backward.
- **Example:** A puck on frictionless ice moves at constant velocity: the net force is 0 N, yet it keeps moving.
- **Follow-up questions and answers:**
  1. *A cyclist stops pedalling and freewheels along a level road. She slowly slows down. Why does she slow down, and what would happen if there were no friction or air resistance?* -> She slows because friction and air resistance act backward on her, giving a backward net force. With no resistive forces nothing would change her velocity, so she would keep going at the same speed.
  2. *True or false: 'If an object is moving, a force must be acting on it in the direction of its motion.' Give an example that supports your answer.* -> False. Example: a puck gliding on frictionless ice, or a ball rising after being thrown (only gravity acts, and it points down). A net force is needed to change velocity, not to keep it.
  3. *A 0.5 kg puck on frictionless ice is pushed with a constant 5 N force for 2 s, then the force is removed. Describe its motion after the force is removed.* -> During the push a = 5 / 0.5 = 10 m/s², so after 2 s the speed is 20 m/s. After the force is removed no net force acts, so it keeps moving at a constant 20 m/s in a straight line.

### M2 - Zero net force means zero velocity

- **Simple description:** The student thinks that if the forces on an object balance (net force is zero), the object must be at rest.
- **Scientifically correct idea:** Zero net force means zero acceleration. The velocity stays constant: the object is either at rest or moving in a straight line at constant speed (Newton's first law).
- **Common reasoning error:** The student treats 'balanced' or 'cancelled' as 'nothing happening', mixing up 'velocity is zero' with 'velocity is not changing'.
- **Simple intervention:** Zero net force means zero ACCELERATION (the velocity does not change). The object can be at rest OR moving at constant velocity.
- **Real-life analogy:** A car on cruise control: the engine force balances the resistance and the speedometer stays at one value. The forces are balanced, but the car is definitely moving.
- **Example:** A skydiver at terminal velocity: weight = air resistance, net force 0 N, but she falls at a constant speed.
- **Follow-up questions and answers:**
  1. *A hot-air balloon rises at a steady 2 m/s. How does the upward lift compare with the balloon's weight, and what is the net force?* -> The lift equals the weight, so the net force is 0 N. The balloon is still moving upward at a constant 2 m/s.
  2. *True or false: 'An object at rest has zero net force, so an object with zero net force must be at rest.' Explain.* -> The first half is true. The second half is false: an object moving at constant velocity also has zero net force.
  3. *A ball bearing falls through thick syrup at a steady 0.2 m/s. Its weight is 0.5 N (ignore buoyancy). What is the drag force on it, and what is the net force?* -> Drag is 0.5 N upward and the net force is 0 N. The ball keeps falling at 0.2 m/s because zero net force means constant velocity, not zero velocity.

### M3 - Action-reaction forces cancel each other

- **Simple description:** The student thinks the two forces in a Newton's third-law pair cancel each other, so nothing can move.
- **Scientifically correct idea:** The forces in a third-law pair are equal in size and opposite in direction, but they act on two DIFFERENT objects. Only forces acting on the same object can cancel. Each object's motion depends on the net force on that object alone.
- **Common reasoning error:** The student adds up all forces in a situation without asking which object each force acts on.
- **Simple intervention:** The two forces in an action-reaction pair are equal and opposite, but they act on DIFFERENT objects. Forces on different objects cannot cancel each other.
- **Real-life analogy:** Two friends on skateboards push each other. Each gets pushed away. If the pair of forces cancelled, neither of them would roll.
- **Example:** A swimmer pushes the pool wall; the wall pushes the swimmer with an equal force. The swimmer accelerates because the wall's force acts on the swimmer.
- **Follow-up questions and answers:**
  1. *A student says: 'A rocket's exhaust pushes the rocket forward and the rocket pushes the exhaust backward with an equal force, so they cancel and the rocket cannot speed up.' What is wrong with this?* -> The two forces act on different objects: the gas feels one and the rocket feels the other. Only the force on the rocket matters for the rocket's motion, and it is not balanced by the force on the gas, so the rocket accelerates.
  2. *Two carts (1 kg and 3 kg) on a frictionless track attract each other with magnets. The magnetic force on the 1 kg cart is 6 N. What is the force on the 3 kg cart, and what is each cart's acceleration?* -> The force on the 3 kg cart is also 6 N, in the opposite direction. Accelerations: 6 / 1 = 6 m/s² for the 1 kg cart and 6 / 3 = 2 m/s² for the 3 kg cart, each toward the other.
  3. *You stand on a skateboard and throw a heavy ball forward. Why do you roll backward? Which force acts on you?* -> You push the ball forward and the ball pushes you backward with an equal force. That backward force acts on you and nothing balances it, so you accelerate backward.

### M4 - Heavier objects fall faster

- **Simple description:** The student thinks heavier objects fall faster than lighter ones.
- **Scientifically correct idea:** Ignoring air resistance, all objects near Earth's surface fall with the same acceleration g (about 9.8 m/s²), whatever their mass. The bigger weight of a heavy object is matched by its bigger mass: a = mg / m = g.
- **Common reasoning error:** The student sees that gravity pulls harder on a heavy object but forgets the heavy object is also harder to accelerate, or blames mass for effects that really come from air resistance.
- **Simple intervention:** Without air resistance, all objects fall with the same acceleration (g = 9.8 m/s² near Earth's surface), no matter their mass.
- **Real-life analogy:** A big truck with a big engine and a small car with a small engine can accelerate equally if engine size is in proportion to mass. Gravity acts like an engine whose power is proportional to the object's mass.
- **Example:** Two balls of 1 kg and 5 kg dropped together in a vacuum hit the ground at the same time.
- **Follow-up questions and answers:**
  1. *Gravity pulls ten times harder on a 10 kg object than on a 1 kg object. Why doesn't the 10 kg object fall ten times faster?* -> Because it also has ten times the mass, so it is ten times harder to accelerate. a = F / m = (10 x 9.8) / 10 = 9.8 m/s², the same as the 1 kg object.
  2. *A 1 kg and a 4 kg object are dropped from rest in a vacuum near Earth's surface (g = 9.8 m/s²). What is the speed of each after 2 s?* -> Both are 19.6 m/s (v = g x t = 9.8 x 2).
  3. *A flat sheet of paper and the same sheet crumpled into a ball are dropped together. The ball lands first. Both have the same weight. Why?* -> Air resistance is larger on the flat sheet because it has more area, so its net downward force is smaller. The weight is the same; the difference comes from air resistance, not from mass.

### M5 - Force and acceleration are the same thing

- **Simple description:** The student treats force and acceleration as the same thing, or uses their words and units interchangeably.
- **Scientifically correct idea:** Force (newtons) is a push or pull. Acceleration (m/s²) is the rate of change of velocity. A net force causes acceleration according to F_net = m x a, so the same force gives different accelerations to different masses.
- **Common reasoning error:** Because force and acceleration go together in everyday talk ('a big push makes it speed up'), the student merges them and ignores mass.
- **Simple intervention:** Force is a push or pull (newtons). Acceleration is how fast velocity changes (m/s²). They are linked by a = F / m but they are different things: the same force gives different accelerations to different masses.
- **Real-life analogy:** Push an empty shopping cart and a full one with the same effort: same push (force), but the empty cart speeds up much faster.
- **Example:** The same 20 N net force gives a 2 kg cart 10 m/s² but a 10 kg cart only 2 m/s².
- **Follow-up questions and answers:**
  1. *A net force acts on a cart. If the mass of the cart is doubled but the net force stays the same, what happens to its acceleration?* -> The acceleration halves (a = F / m).
  2. *The net force on an object is 12 N and its acceleration is 4 m/s². What is its mass?* -> 3 kg (m = F / a = 12 / 4).
  3. *A 0.1 kg tennis ball has an acceleration of 100 m/s². A 1000 kg car has an acceleration of 0.1 m/s². Which has the larger net force?* -> Ball: F = 0.1 x 100 = 10 N. Car: F = 1000 x 0.1 = 100 N. The car has the larger net force even though its acceleration is much smaller.

**Why these five are genuinely different:** M1 is about *what keeps motion going* (force vs velocity). M2 is about *what balanced forces do* (zero net force vs zero velocity). M3 is about *which object a force acts on* (third-law pairs). M4 is about *free fall and mass*. M5 is about *the meaning and units of force vs acceleration*. M1 and M2 are the closest pair (see Part 7 and the honest note in Part 13).

## Part 7 - How to distinguish similar misconceptions

### The same final answer, five different reasons

Suppose a puck, a car or a spacecraft is moving, and five students all say **"It stops."** The words *after* it show which misconception is behind it:

| Student says | Likely label | Clue |
|---|---|---|
| "It stops because nothing is pushing it any more." | M1 | Focuses on the *absence of a push*. Force is treated as the thing that keeps motion alive. |
| "It stops because the forces are equal and cancel." | M2 | Focuses on *balance/cancelling*. The cancelling is correct; the conclusion 'stops' is wrong. |
| "The action and reaction cancel, so it stops." | M3 | Cancels a *third-law pair* (forces on different objects). |
| "Acceleration is zero, so there is no force and it stops." | M5 | Treats *acceleration as the force itself* (a = 0 means no force). |
| (M4 is about falling and mass, so 'it stops' does not normally appear. If a student writes 'heavier ones fall faster' it is M4.) | M4 | Words like heavier, more weight, falls faster. |

### Matching pairs inside the dataset

- **Same question, same wrong conclusion, different reasoning (M1 vs M2):** `Q012` (M1): "It will slow down and stop. To keep a car moving the engine force has to be bigger than the resistance, and here they're only equal." versus `Q034` (M2): "0 m/s. The forces are equal, so they cancel and the car comes to rest.".
- **"Cancel" language (M2 vs M3):** `Q031` (M2): "0 m. The 6 N forces cancel out, so the cart doesn't go anywhere." versus `Q023` (M3): "Because the crate pushes back on me with 200 N, equal and opposite to my push, so they cancel and it stays still.".
- **Ignoring mass (M4 vs M5):** `Q048` (M4): "Weights are 9.8 N and 98 N. The 10 kg object has ten times the force on it, so it speeds up faster than the 1 kg object." versus `Q025` (M5): "P has the bigger acceleration because its force (40 N) is bigger than Q's (10 N).".
- **Force tied to speed (M1) vs force equals acceleration (M5):** `Q067` (M1): "6 N, because force = mass x speed = 2 x 3." versus `Q042` (M5): "3 N, because the acceleration is 3 so the force is 3.".

### Clues for every category

| ID | Words and ideas that point to it | What is the student focused on? | Often confused with | One question that separates them |
|---|---|---|---|---|
| M1 | 'keep pushing', 'needs a force to keep moving', 'force of the hit', 'runs out/used up', 'engine must be bigger', F = mass x speed | Force as the *cause of motion itself* | M2 (both say 'stops'), M5 (force linked to speed) | 'If nothing pushes it, what happens?' M1 says it stops; M2 talks about balanced forces instead |
| M2 | 'balanced', 'cancel', 'equal forces', 'equilibrium means stationary', 'not going anywhere' | *Balance of forces on one object* equals no motion | M1, M3 (both use 'cancel') | 'Was it moving before the forces balanced?' |
| M3 | 'action and reaction cancel', 'equal and opposite so nothing moves', 'cart can never start' | *Which object each force acts on* is ignored | M2 (cancel language) | 'Which object does each of the two forces act on?' |
| M4 | 'heavier', 'more weight', 'gravity pulls harder so faster', 'total weight is bigger' | *Gravity's pull* without mass | M5 (both ignore mass) | 'What is the acceleration of each one?' M4 stays on falling; M5 is about any force |
| M5 | 'force is acceleration', 'N and m/s2 are the same', 'acceleration drawn as a force', 'same force = same acceleration' | *Treating two quantities as one* | M4 (ignores mass), M1 (force vs velocity) | 'What are the units of each?' |

**Quick decision rules (useful for a human check or a prompt):**

1. Does the student equate force with **velocity or motion** ('needs force to move', F = mv)? -> **M1**.
2. Does the student say forces are **balanced or cancelled on one object** and conclude it is at rest or stops? -> **M2**.
3. Does the student cancel **two forces that act on different objects**? -> **M3**.
4. Does the student say **heavier things fall faster**? -> **M4**.
5. Does the student equate force with **acceleration** (numbers, units or drawings)? -> **M5**.

## Part 8 - Intervention bank

Each plan is short and beginner-friendly. The `short_explanation` is shown first; use `detailed_explanation`, `worked_example` and `hint` only if the student needs more help.

### M1 - Force required for motion

- **short_explanation:** A force is needed to CHANGE how something moves (speed up, slow down, turn), not to KEEP it moving. If nothing pushes or pulls it, an object keeps moving at the same velocity.
- **detailed_explanation:** Things around us usually stop because friction and air resistance act on them, not because their motion 'runs out'. Where friction is tiny (ice, space) objects keep going. So when something moves at steady speed, the forces on it are balanced (net force = 0). A forward push may still be there, but it is only cancelling friction or drag. Force is linked to CHANGE in velocity (acceleration), not to velocity itself.
- **common_mistake:** Saying 'it's moving, so there must be a force pushing it forward'.
- **real_life_analogy:** A skater gliding on smooth ice after one push does not need anyone pushing her every second. On a rough road she would stop because the road drags her backward.
- **worked_example:** A 1000 kg car cruises at a steady 20 m/s. Air drag + friction = 500 N backward. Step 1: steady speed -> acceleration 0 -> net force 0. Step 2: so the engine must give 500 N forward to cancel the 500 N backward. Net = 500 - 500 = 0 N. Step 3: if there were no drag or friction, the engine force needed would be 0 N.
- **hint:** Ask yourself: is the velocity changing? If not, the net force is zero.
- **follow_up_question:** A spacecraft coasts through empty space with its engines off. What is its velocity doing, and why?
- **follow_up_answer:** Its velocity stays constant, because no net force acts on it.

### M2 - Zero net force means zero velocity

- **short_explanation:** Zero net force means zero ACCELERATION (the velocity does not change). The object can be at rest OR moving at constant velocity.
- **detailed_explanation:** Newton's first law has two halves: an object at rest stays at rest, and an object moving stays moving at the same velocity, as long as the forces on it are balanced. Balanced forces do not stop an object; they stop its velocity from CHANGING. 'Balanced' does not mean 'stopped'. To know which case you have, look at how the object was moving to begin with.
- **common_mistake:** Saying 'the forces cancel, so it stops' or 'so it isn't moving'.
- **real_life_analogy:** A car on cruise control: the engine force balances the resistance and the speedometer stays at one value. The forces are balanced, but the car is definitely moving.
- **worked_example:** A 500 kg lift moves upward at a constant 1.5 m/s. Weight = 500 x 9.8 = 4900 N. Step 1: constant velocity -> net force 0. Step 2: so the cable tension is 4900 N, equal to the weight. Step 3: the lift is still moving; in 4 s it rises 1.5 x 4 = 6 m.
- **hint:** Balanced forces change nothing about the velocity. Was the object moving at the start?
- **follow_up_question:** A hot-air balloon rises at a steady 2 m/s. How does the lift compare with the weight?
- **follow_up_answer:** They are equal, so the net force is 0 N. The balloon keeps rising at 2 m/s.

### M3 - Action-reaction forces cancel each other

- **short_explanation:** The two forces in an action-reaction pair are equal and opposite, but they act on DIFFERENT objects. Forces on different objects cannot cancel each other.
- **detailed_explanation:** To decide whether forces cancel, only add up the forces acting on ONE object. When you push a wall, your push acts on the wall and the wall's push acts on you. For you, only the wall's push counts; for the wall, only your push counts. Each object then has its own net force and its own acceleration (a = F / m). Forces that DO cancel (balanced forces) act on the same object.
- **common_mistake:** Adding the action force and the reaction force to get zero, when the question is about only one of the objects.
- **real_life_analogy:** Two friends on skateboards push each other. Each gets pushed away. If the pair of forces cancelled, neither of them would roll.
- **worked_example:** A 40 kg student on skates pushes a 60 kg friend with 80 N on smooth ice. Step 1: the friend feels 80 N forward, so a = 80 / 60 = 1.33 m/s². Step 2: the student feels 80 N backward, so a = 80 / 40 = 2 m/s². Step 3: the forces do not cancel because they act on different people.
- **hint:** For each force, write down which object it acts on. Only add forces that act on the same object.
- **follow_up_question:** A student says a rocket's exhaust pushes on the rocket and the rocket pushes on the exhaust, so the forces cancel and the rocket can't speed up. What is wrong?
- **follow_up_answer:** The two forces act on different objects (rocket and gas), so they cannot cancel. The force on the rocket is what accelerates the rocket.

### M4 - Heavier objects fall faster

- **short_explanation:** Without air resistance, all objects fall with the same acceleration (g = 9.8 m/s² near Earth's surface), no matter their mass.
- **detailed_explanation:** A heavier object has a bigger weight (W = mg), so gravity pulls harder on it. But it also has more mass, so it is harder to accelerate. The two effects match exactly: a = F / m = mg / m = g. In air, a feather falls slowly because of air resistance, not because it is lighter.
- **common_mistake:** Looking only at the bigger pull of gravity and forgetting the bigger mass (inertia).
- **real_life_analogy:** A big truck with a big engine and a small car with a small engine can accelerate equally if engine size is in proportion to mass. Gravity acts like an engine whose power is proportional to the object's mass.
- **worked_example:** Drop a 2 kg rock and an 8 kg rock in a vacuum. Weights: 2 x 9.8 = 19.6 N and 8 x 9.8 = 78.4 N. Accelerations: 19.6 / 2 = 9.8 m/s² and 78.4 / 8 = 9.8 m/s². Same acceleration, so they land together.
- **hint:** Compare the force AND the mass: a = F / m. What happens to mg / m?
- **follow_up_question:** A 3 kg and a 12 kg object are dropped in a vacuum. What is the speed of each after 1.5 s? (g = 9.8 m/s²)
- **follow_up_answer:** Both are 14.7 m/s (9.8 x 1.5).

### M5 - Force and acceleration are the same thing

- **short_explanation:** Force is a push or pull (newtons). Acceleration is how fast velocity changes (m/s²). They are linked by a = F / m but they are different things: the same force gives different accelerations to different masses.
- **detailed_explanation:** Force is the cause; acceleration is the effect. Newton's second law says net force = mass x acceleration. So with the same force a light object accelerates more than a heavy one. Force cannot be measured in m/s² and acceleration cannot be measured in newtons. Acceleration is not a force and never appears as an arrow on a free-body diagram.
- **common_mistake:** Saying 'the force is 3 m/s²' or 'the same force always gives the same acceleration'.
- **real_life_analogy:** Push an empty shopping cart and a full one with the same effort: same push (force), but the empty cart speeds up much faster.
- **worked_example:** A 10 kg box gets a net force of 30 N. a = F / m = 30 / 10 = 3 m/s². If the box were 5 kg: a = 30 / 5 = 6 m/s². Same force, different acceleration.
- **hint:** Check the units. Newtons are for force, m/s² for acceleration. What quantity connects them?
- **follow_up_question:** A 4 kg object accelerates at 2.5 m/s². What is the net force on it?
- **follow_up_answer:** 10 N (F = ma = 4 x 2.5).

## Part 9 - Reassessment bank (25 fresh questions)

These are new situations, not copies of the training questions, so they test whether the student can *transfer* the idea.

| ID | Misconception | Difficulty | Type | Question | Correct answer |
|---|---|---|---|---|---|
| R-M1-01 | M1 | Easy | Conceptual | A comet drifts through empty space, far from any star or planet. Is any force needed to keep it moving in a straight line at constant speed? | No. With no net force it keeps its velocity (Newton's first law). |
| R-M1-02 | M1 | Easy | Multiple-choice | A ball is kicked along a long, smooth, flat surface where friction is negligible. After it leaves the foot, which is true? (A) The kick force is gradually used up, so it slows. (B) It moves at constant velocity with no horizontal force acting. (C) It speeds up because of leftover kick force. (D) It needs a small push every second. | B |
| R-M1-03 | M1 | Medium | Scenario-based | A sled glides at a steady 4 m/s across a frozen lake. Friction is negligible. A student draws a forward arrow labelled 'motion force' on the sled. Should that arrow be there? Why or why not? | No. Nothing pushes the sled forward; constant velocity means zero net force. Only weight and the normal force act (and they cancel). |
| R-M1-04 | M1 | Medium | Numerical | A 3 kg trolley moves at a constant 2 m/s on a frictionless track. (a) What is the net horizontal force on it? (b) A 6 N forward force then acts on it for 1 s. What is its speed afterwards? | (a) 0 N. (b) a = 6 / 3 = 2 m/s², so the speed becomes 2 + 2 x 1 = 4 m/s. |
| R-M1-05 | M1 | Hard | Reasoning/Explanation | A truck travels at 20 m/s on a level road. The engine force is 2500 N and the total resistance is 2500 N. The driver raises the engine force to 3000 N (resistance stays 2500 N for now). Describe the truck's motion before and after the change. | Before: net force 0, so constant 20 m/s. After: net force 500 N forward, so it accelerates (a = 500 / mass). In practice air drag grows with speed until it reaches 3000 N, then the truck settles at a new, higher constant speed. |
| R-M2-01 | M2 | Easy | Multiple-choice | Which of these objects could have zero net force? I. A ball resting on a table. II. A probe moving at a steady 5 m/s through deep space with nothing acting on it. (A) I only (B) II only (C) Both I and II (D) Neither | C |
| R-M2-02 | M2 | Medium | Short-answer | A runner jogs at a steady 3 m/s in a straight line along flat ground. What is the net force on her, and what is her velocity? | Net force 0 N; her velocity is 3 m/s in the direction she runs. |
| R-M2-03 | M2 | Medium | Numerical | A 0.4 kg puck moves at 5 m/s along a table. A small fan blows on it with 0.2 N forward and friction pulls back with 0.2 N. How far does the puck travel in 3 s? | Net force is 0 N, so it keeps moving at 5 m/s. Distance = 5 x 3 = 15 m. |
| R-M2-04 | M2 | Hard | Scenario-based | A box rides on a horizontal conveyor belt moving at a constant 0.5 m/s. The box does not slip. What is the net force on the box? | 0 N. Constant velocity means zero acceleration, so no net force. No horizontal force is needed; weight and the normal force cancel vertically. |
| R-M2-05 | M2 | Hard | Reasoning/Explanation | Give two examples of objects with balanced forces: one at rest and one moving. State the velocity of each. | Example: a book on a table (velocity 0) and a car on cruise control at a steady 25 m/s (velocity 25 m/s, constant). |
| R-M3-01 | M3 | Easy | Conceptual | A person kicks a soccer ball. Name the equal and opposite force pair and say which object each force acts on. Do these two forces cancel each other? | The foot pushes the ball (force acts on the ball); the ball pushes the foot (force acts on the foot). They are equal and opposite but do not cancel because they act on different objects. |
| R-M3-02 | M3 | Medium | Numerical | A 70 kg astronaut and a 210 kg satellite float at rest in space. The astronaut pushes the satellite with 35 N. Find each one's acceleration while the push lasts. | Satellite: 35 / 210 = 0.17 m/s² away from the astronaut. Astronaut: 35 / 70 = 0.5 m/s² in the opposite direction. |
| R-M3-03 | M3 | Medium | Conceptual | A swimmer pushes on the pool wall with 150 N to start a lap. What is the force of the wall on the swimmer? Does it cancel the swimmer's push on the wall? Explain. | 150 N, directed away from the wall. It does not cancel the swimmer's push, because that push acts on the wall. The wall's force on the swimmer is what accelerates the swimmer. |
| R-M3-04 | M3 | Hard | Numerical | A 1000 kg car pulls a 500 kg trailer along a level road. Ignore resistance. The road pushes the car forward with a total force of 1500 N. Find the acceleration of the car and trailer, and the tension in the coupling. | a = 1500 / 1500 = 1 m/s². Trailer: T = 500 x 1 = 500 N. (Check on the car: 1500 - 500 = 1000 x 1.) The tension pulls the trailer forward and the car backward; those act on different objects. |
| R-M3-05 | M3 | Medium | Reasoning/Explanation | A small fridge magnet clings to a large iron door. The magnet pulls on the door and the door pulls on the magnet with equal force. If you pull the magnet slightly away and release it, why does the magnet move toward the door while the door does not visibly move? | The forces are equal and opposite but act on different objects. a = F / m, so the light magnet gets a large acceleration while the massive door (also held by its hinges) hardly moves. |
| R-M4-01 | M4 | Easy | Short-answer | A coin and a lead pellet are released together at the top of a long vacuum tube. Which hits the bottom first? | They land at the same time. In a vacuum all objects fall with the same acceleration. |
| R-M4-02 | M4 | Medium | Numerical | An airless drop tower is 19.6 m tall. A 0.2 kg tennis ball and a 20 kg boulder are released together from the top. How long does each take to reach the bottom? (g = 9.8 m/s²) | Both take 2.0 s (t = sqrt(2h / g) = sqrt(2 x 19.6 / 9.8) = 2.0 s). |
| R-M4-03 | M4 | Medium | Numerical | On Mars (g = 3.7 m/s²) a 5 kg rock and a 50 kg rock are dropped. Find the weight and the acceleration of each. | Weights: 18.5 N and 185 N. Both accelerate at 3.7 m/s². |
| R-M4-04 | M4 | Hard | Reasoning/Explanation | A heavy bowling ball and a light foam ball of identical size are dropped from a tall building. The foam ball arrives noticeably later. Is the difference caused by mass itself or by air resistance? What would you expect in a vacuum? | It is caused by air resistance: it is a much larger fraction of the foam ball's small weight. In a vacuum both would land together. |
| R-M4-05 | M4 | Hard | Scenario-based | A 2 kg block and a 6 kg block are joined by a slack string and dropped together (ignore air resistance). Does the string become tight? Explain. | No. Both accelerate at g, so the string stays slack and carries no tension; they fall together. |
| R-M5-01 | M5 | Easy | Multiple-choice | A student writes 'net force = 4 m/s²'. What is wrong? (A) Nothing. (B) m/s² is a unit of acceleration; force is measured in newtons. (C) The number should be bigger. (D) Force can only be measured in kg. | B |
| R-M5-02 | M5 | Medium | Numerical | A cyclist and bike with total mass 60 kg accelerate at 1.5 m/s². What is the net force? | 90 N (F = ma = 60 x 1.5). |
| R-M5-03 | M5 | Medium | Numerical | Two shopping carts are each pushed with the same net force of 30 N. Cart A accelerates at 3 m/s² and cart B at 0.5 m/s². Find the mass of each cart. | Cart A: 30 / 3 = 10 kg. Cart B: 30 / 0.5 = 60 kg. |
| R-M5-04 | M5 | Hard | Numerical | A 500 kg rocket has an upward thrust of 7000 N. Its weight is 4900 N (g = 9.8 m/s²). Find the net force and the acceleration. Which of thrust, weight and acceleration are forces? | Net force = 7000 - 4900 = 2100 N upward. a = 2100 / 500 = 4.2 m/s². Thrust and weight are forces; acceleration is not. |
| R-M5-05 | M5 | Medium | Reasoning/Explanation | The same 90 N push is applied to a 3 kg skateboard and a 3000 kg truck. Find both accelerations and say what this shows about force and acceleration. | Skateboard: 90 / 3 = 30 m/s². Truck: 90 / 3000 = 0.03 m/s². The same force gives very different accelerations, so force is not the same as acceleration; mass links them. |

The column *why_this_tests_the_misconception* is in `reassessment_bank.csv/.json`.

## Part 10 - Learner resolution logic

Flow for one misconception:

```
DIAGNOSED -> INTERVENED -> fresh question 1
   correct -> tentatively_resolved -> fresh question 2 (different situation)
                 correct -> 'Misconception appears resolved.'   (+ delayed re-check later)
                 wrong   -> 'Further assessment recommended.'
   wrong   -> detailed explanation + worked example + hint -> fresh question 2
                 correct -> 'Further assessment recommended.' -> question 3
                 wrong   -> 'Misconception may still be present.' (stop loop, suggest teacher)
```

Simple rules for the developer (also in `resolution_rules.json`):

- R1: Only start an intervention if the classifier's confidence >= 0.6. Below that, ask one clarifying probe question instead.
- R2: After the short intervention, ask ONE fresh reassessment question for the same misconception (Easy or Medium).
- R3: If it is correct (and for multiple-choice the student gave a one-line reason, or the answer was numerical/written), status = tentatively_resolved. Ask a SECOND fresh question (Medium or Hard, different situation).
- R4: If the second question is also correct, status = appears_resolved. Schedule one delayed re-check later (next session or after at least 3 other questions).
- R5: If the first reassessment answer is wrong, show the detailed explanation + worked example + hint, then ask a fresh question.
- R6: If that is correct, status = further_assessment_recommended (not resolved yet); ask one more. If correct, status = appears_resolved.
- R7: If two reassessment answers in a row are wrong, status = may_still_be_present. Stop the automatic loop and suggest a teacher or tutor.
- R8: Never reuse a question already shown to this learner. Never reuse the original training question as the reassessment question.
- R9: If the new wrong answer matches a DIFFERENT misconception, log the new misconception and do not count it as a failure for the old one.
- R10: A single correct answer is never proof of learning. Wording shown to the learner must be tentative ('appears resolved').

**Wording to show the learner:** *Misconception appears resolved*, *Further assessment recommended*, *Misconception may still be present*. Never write 'learned' or 'fixed'. One correct answer does not prove complete learning (a multiple-choice question can even be guessed).

Minimal Python skeleton:

```python
def update_status(state, correct):
    # state = {'status': 'intervened', 'streak_wrong': 0, 'asked': 0, 'support': False}
    state['asked'] += 1
    if correct:
        state['streak_wrong'] = 0
        if state['status'] == 'intervened':           state['status'] = 'tentatively_resolved'
        elif state['status'] == 'tentatively_resolved': state['status'] = 'appears_resolved'
        elif state['status'] == 'needs_more':          state['status'] = 'further_assessment_recommended' if not state['support'] else 'appears_resolved'
    else:
        state['streak_wrong'] += 1
        state['support'] = True                       # show detailed explanation next
        state['status'] = 'may_still_be_present' if state['streak_wrong'] >= 2 else 'needs_more'
    if state['asked'] >= 3 and state['status'] not in ('appears_resolved',):
        state['status'] = 'may_still_be_present'
    return state
```

(The skeleton is only a starting point. Member 4 should adapt it to the app's state model and add the 'further_assessment_recommended -> one more question' step.)

## Part 12 - Preparing for machine learning (beginner-friendly)

**What the model learns:** read a student's answer and guess which label (M1-M5, or NONE) it belongs to.

### 1. Which columns can be the model's INPUT?

- **`student_answer`** - the main input. This is the only thing guaranteed to exist when a real student uses the website.
- **`question`** (and optionally `question_type`) - helpful context, because the same sentence can mean different things for different questions. At prediction time the system knows which question it just asked.

### 2. Which column is the TARGET (the answer the model should predict)?

- **`misconception_id`** (values M1, M2, M3, M4, M5, NONE).

### 3. Which columns must NOT be inputs (they give the answer away = *data leakage*)?

| Column | Why it must be excluded |
|---|---|
| misconception_name | It is the label written in words. |
| is_correct | It almost equals the label (false/true = wrong/NONE). |
| reasoning_error, explanation, real_life_example | They were written *knowing* the label. |
| follow_up_question / answer / difficulty | Chosen *from* the label. |
| source_or_reason | Contains the mistake pattern name. |
| correct_answer | It is the same for the wrong and the right student answers to one question; it adds little and can encourage copying question text. Keep it out of the first version. |
| question_id | Just a row number. |
| subtopic | In this dataset it is strongly tied to the label (e.g. free fall = M4). A model could cheat by learning 'free-fall question = M4' instead of reading the answer. A real student could make an M5 mistake on a free-fall question. Keep it out of the first version. |
| topic | Always the same, no information. |

### 4. How to split the data (train / validation / test)

Think of it like exam preparation: **train** = the practice questions you study; **validation** = a mock test to tune your method; **test** = the real exam you look at only once at the end. If exam questions were already in your practice set, your score would be fake. That is *data leakage*.

`split_assignments.csv` already does this for you: **train 44, validation 13, test 13** (each misconception has 7 / 2 / 2 examples, and the correct class 9 / 3 / 3).

How leakage was avoided:

- No identical or near-identical question, or student answer, appears in two different splits. An automatic check compared every pair of rows (text similarity); no pair scoring 0.60 or higher sits in different splits.
- The two rows that share one question (`Q012` and `Q034`, the 'car' pair) have the same `group_id`, so they always stay together (both in train). The `group_id` column exists for this purpose.
- Similar-looking questions of different labels were kept on the same side where possible.

**Warnings for Member 1:** 70 rows is small. (a) Do not tune on the test set. (b) Report **per-class results and a confusion matrix**, not just overall accuracy; expect M1 vs M2 and M2 vs M3 to be the hardest. (c) With so few rows, a simple model (text vectors + logistic regression), a sentence-embedding classifier, or an LLM prompt that includes the five definitions from `misconceptions.json` is more realistic than anything complicated. (d) Do not oversell test results: 13 test rows means one mistake changes accuracy by about 8 percentage points.

Loading in Python:

```python
import json, pandas as pd
df = pd.read_json('relearn_dataset.json')
sp = pd.read_csv('split_assignments.csv')
df = df.merge(sp, on='question_id')
X_cols = ['question', 'student_answer']       # inputs
y_col = 'misconception_id'                    # target
train = df[df.split == 'train']; val = df[df.split == 'validation']; test = df[df.split == 'test']
```

## Part 13 - Data quality check (results)

All checks below were run by a script on the final files (`build.py` logic reproduced in these numbers).

| Check | Result |
|---|---|
| Rows in JSON / CSV | 70 / 70 (equal) |
| Exact 18 columns in the CSV | True |
| Empty fields | 0 |
| Unique question_id values | True |
| Examples per misconception | M5: 11, M4: 11, M1: 11, M2: 11, NONE: 15, M3: 11 |
| Rows where is_correct disagrees with label | 0 |
| Exact duplicate student answers | 0 |
| Questions shared by two rows | 1 (the deliberate M1/M2 'car' pair, same group, same split) |
| Cross-split near-duplicates (similarity >= 0.60) | 0 |
| Highest follow-up vs own-question similarity | 0.58 (different scenarios) |
| Highest reassessment vs any training/follow-up question | 0.66 (different numbers and settings) |
| Reassessment questions per misconception | M1: 5, M2: 5, M3: 5, M4: 5, M5: 5 |
| Numerical answers re-computed by script | 52 checks, 0 failed |
| Units present in numerical answers | Yes (N, m/s, m/s2, kg, m, s) |

**Problems found and fixed while building:**

1. Some follow-up questions reused scenarios from the training rows (spacecraft, car) -> replaced with new situations.
2. One elevator question said 'is moving' while the wrong answer said 'stationary' (self-contradicting) -> rewritten so the question stays neutral.
3. One M4 wrong answer accidentally contained an M5-style idea ('98 m/s2') -> rewritten to show only the M4 error.
4. Two correct answers used almost the same template as incorrect ones (cart/crate, ball/cart) -> rewritten with different contexts and numbers.
5. Two similar M1 questions sat on opposite sides of the train/validation boundary -> moved to the same side.
6. Two M5 student answers in train and test were worded almost the same -> reworded one.
7. One reassessment question copied the template of a training question -> redesigned (drop-tower timing; inverse mass problem).

**Honest limitations (please tell your team):**

- **M1 and M2 are logically close.** 'Zero net force means stopped' is the contrapositive of 'motion needs force', so some answers could fairly be labelled either. We separate them by *reasoning style* (needs a push vs balanced means stopped). Expect the model to confuse them sometimes, and consider merging them into one 'M1/M2' bucket in the first prototype if results are poor.
- M4 vs M5 can overlap when a student ignores mass. M4 is the free-fall version; M5 is the general version.
- The dataset is synthetic and small (70 rows). Real students will write messier answers, include typos, and mix several misconceptions.
- Everything is physics at school level: fixed g = 9.8 m/s2; the Moon's g = 1.6 m/s2; Mars's g = 3.7 m/s2; air resistance ignored unless stated.
- No research citations are given because none were used; all questions are original.

## Part 14 - Beginner explanation

**1. What is this dataset?** A big, tidy table of physics questions with example student answers. Each answer is tagged with the specific mistake in thinking (if any). It teaches the AI what each mistake looks like and gives the website its questions and explanations.

**2. What is a misconception?** A *wrong idea that feels right*. A student might know the formula and still believe 'heavier things fall faster'. Fixing it needs more than saying 'wrong'. You have to explain why the idea feels right and why it fails.

**3. What do M1-M5 mean?**

- **M1** - thinking a force is needed to keep something moving.
- **M2** - thinking balanced forces mean the object is at rest.
- **M3** - thinking action and reaction forces cancel each other.
- **M4** - thinking heavier objects fall faster.
- **M5** - thinking force and acceleration are the same thing.

**4. What is a labelled example?** One row where a human (us) already wrote the right label. Like a flashcard: the front is the student's answer, the back is 'this is M3'. The AI studies many flashcards and later guesses the label of new answers.

**5. What will Member 1 (ML Developer) do?** Train or prompt a classifier using `student_answer` (and `question`) as input and `misconception_id` as target, following the splits, and report results per class.

**6. What will Member 3 (Frontend) do?** Build the screens: show a question, take the answer, show the diagnosis, show the intervention (short explanation, hint, worked example), show the reassessment question, and show the result message. The questions and texts come from the dataset and banks.

**7. What will Member 4 (Integration/QA) do?** Connect all the pieces: model output -> correct intervention -> fresh reassessment question -> status update -> learner history, and test that the connections work with sample cases.

**8. How does the dataset connect to the website?** The website shows questions (from `question` and the reassessment bank), sends the student's text to the model, uses the predicted `misconception_id` as the key to find the right plan in `intervention_bank`, then picks a question from `reassessment_bank` with the same id.

**9. How does the flow work?**

```
Student question               (dataset: question)
        |
Student answer                 (typed by the student)
        |
AI / model                     (Member 1's classifier)
        |
Misconception prediction       (M1..M5 or NONE + confidence)
        |
Targeted intervention          (intervention_bank, keyed by misconception_id)
        |
Fresh reassessment question    (reassessment_bank, same misconception_id)
        |
New answer                     (typed by the student)
        |
Check if misconception appears resolved   (resolution rules, Part 10)
```

## Part 15 - Team handoff

### A. Give this to Member 1 - ML Developer

- **Files:** `relearn_dataset.json` (or `.csv`), `split_assignments.csv`, `misconceptions.json`.
- **Input:** `student_answer` (+ `question`). **Target:** `misconception_id` with 6 classes: M1, M2, M3, M4, M5, NONE.
- **Do not use** as input: misconception_name, is_correct, reasoning_error, explanation, real_life_example, follow_up_*, source_or_reason, correct_answer, subtopic, question_id (Part 12).
- **Splits:** use `split_assignments.csv` exactly. Never move rows between splits. Keep rows with the same `group_id` together.
- **Evaluate with:** per-class precision/recall/F1, macro-F1, and a confusion matrix. Watch M1 vs M2 and M2 vs M3.
- **Output the app needs:** `{"predicted_misconception_id": "M2", "confidence": 0.78, "top_3": [["M2",0.78],["M1",0.15],["M3",0.04]]}`. If confidence is below 0.6 the app asks a probing question instead of intervening.
- **Realistic options for 70 rows:** TF-IDF + logistic regression as a baseline; sentence embeddings + logistic regression; or an LLM prompt with the 5 definitions and a few examples. All are fine for a hackathon.

### B. Give this to Member 3 - Frontend Developer

- **Question bank:** use the `question`, `question_type`, `difficulty` fields from `relearn_dataset.json`. Multiple-choice options are inside `question` as (A) (B) (C) (D); split them with a small regular expression for button display.
- **After diagnosis, show:** `short_explanation` first, then buttons 'Give me a hint' (`hint`), 'Show a worked example' (`worked_example`), 'Explain in more detail' (`detailed_explanation`). Fields come from `intervention_bank.json`, looked up by `misconception_id`.
- **Reassessment screen:** one question from `reassessment_bank.json` with `question` and `difficulty` shown. Never display `correct_answer` or `why_this_tests_the_misconception` until after the student answers.
- **Result messages (exact wording):** 'Misconception appears resolved.', 'Further assessment recommended.', 'Misconception may still be present.' (also in `resolution_rules.json`).
- **Display names:** use `misconception_name` for the user-friendly label, e.g. 'Force required for motion'.

### C. Give this to Member 4 - Integration/QA

- **The key that links everything:** `misconception_id` (M1-M5). It must exist in `misconceptions.json`, `intervention_bank.json` and `reassessment_bank.json`.
- **Pipeline:** diagnosis -> intervention -> reassessment -> history. Use `resolution_rules.json` and the learner history example in it as the data shape.
- **Rules to test:** (1) a reassessment question is never the same as the question just answered; (2) a question is never shown twice to one learner; (3) low confidence leads to a probe question, not an intervention; (4) status text is always one of the three allowed messages; (5) after 3 attempts the loop stops.
- **Ready-made QA cases (from the TEST split; keep them out of any tuning):**

| question_id | Student answer | Expected label |
|---|---|---|
| Q001 | Yes. Zero acceleration means zero force, because acceleration is the force. | M5 |
| Q004 | Faster, because together the total weight is bigger, so the pair is heavier than the heavy ball alone. | M4 |
| Q013 | The oar pushes the water backward, so the water pushes the oar forward with equal force. These two forces are on different objects (water and oar/boat), so they don't cancel, and the forward force on the boat speeds it up. | NONE |
| Q017 | B - the net force makes the object accelerate, and a larger mass gives a smaller acceleration for the same force. | NONE |
| Q023 | Because the crate pushes back on me with 200 N, equal and opposite to my push, so they cancel and it stays still. | M3 |
| Q035 | A forward arrow labelled 'force of the hit' pointing the way it moves, plus the weight and the normal force. | M1 |
| Q036 | Friction between the marble and the table pulls backward on it. Moving objects don't slow down by themselves, they only slow if a force acts against the motion. | NONE |
| Q039 | Both are zero because the 120 N force and the 120 N reaction force cancel. | M3 |
| Q042 | 3 N, because the acceleration is 3 so the force is 3. | M5 |
| Q048 | Weights are 9.8 N and 98 N. The 10 kg object has ten times the force on it, so it speeds up faster than the 1 kg object. | M4 |
| Q059 | Equilibrium is when the forces are balanced, so the object is stationary. A moving object can't be in equilibrium. | M2 |
| Q062 | Because moving things need a force to keep them going. If I stop pushing there is no force so it can't keep moving. | M1 |
| Q069 | Thrust equals drag and lift equals weight, so everything is balanced and the plane is in equilibrium. That means it isn't really moving forward, it's just hovering in the air. | M2 |

- **Extra QA idea:** feed the M1 and M2 'car' pair (`Q012` and `Q034`). They end in the same words but should receive different interventions.

## Final checklist

- [x] Misconceptions created (5)
- [x] Training dataset created (70 rows)
- [x] Correct examples included (15)
- [x] Wrong examples included (55)
- [x] Intervention bank created (5 plans)
- [x] Reassessment bank created (25 questions)
- [x] ML-ready format created (inputs/target/splits)
- [x] JSON created
- [x] CSV created
- [x] Dataset quality checked (automatic checks + manual review; limitations listed in Part 13)
- [x] Team handoff prepared

*Remember: the examples are synthetic. A quick test with real students will tell you far more than any additional synthetic row.*