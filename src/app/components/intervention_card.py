"""Targeted Pedagogical Intervention component for Re:Learn application.

Renders the core educational moment: "Let's Fix This Misconception",
with distinct visual styling for conceptual clarification, Socratic hint, and physical examples.
"""

from typing import Any, Dict
import streamlit as st
from src.app.styles import render_html


# Physical analogy / example catalog matching Member 2's taxonomy
CONCEPTUAL_EXAMPLES = {
    "impetus_force_persistence": {
        "title": "Deep Space & Frictionless Curling",
        "description": "Imagine an astronaut releasing a wrench in deep space. With engines off and zero friction, the wrench coasts forever at constant velocity. No 'engine' or internal push is needed to sustain motion; motion is an object's natural state unless an external force acts on it."
    },
    "heavier_objects_fall_faster": {
        "title": "Apollo 15 Lunar Hammer & Feather Drop",
        "description": "During Apollo 15, astronaut David Scott dropped a 1.32 kg geological hammer and a 0.03 kg falcon feather simultaneously on the airless Moon. Free from atmospheric drag, both hit the lunar dust at the exact same instant, validating Galileo's equivalence principle."
    },
    "acceleration_zero_at_top": {
        "title": "Velocity vs. Rate of Change",
        "description": "Velocity is where you are moving right now; acceleration is how quickly velocity is changing. Even when a thrown ball's vertical velocity crosses zero at its highest point, Earth's gravity is pulling downward at 9.8 m/s² uninterrupted."
    },
    "action_reaction_same_object": {
        "title": "Jumping Off a Skateboard",
        "description": "When you leap forward off a skateboard, your feet push backward on the board (Action on board), while the board pushes your feet forward (Reaction on you). Because the two forces act on different objects, they can never cancel each other out."
    }
}


def render_intervention_card(intervention: Dict[str, Any], misconception_key: str = ""):
    """Render the prominent 'Let's Fix This Misconception' learning module.

    Parameters
    ----------
    intervention : dict
        Output from get_intervention(misconception_label).
    misconception_key : str, optional
        Raw misconception label to lookup tailored physical examples.
    """
    title = intervention.get("title", "Concept Remediation")
    explanation = intervention.get("explanation", "Review the fundamental laws governing this scenario.")
    key_concept = intervention.get("key_concept", "Fundamental Physics Principles")
    guided_hint = intervention.get("guided_hint", "Analyze the net forces acting at that specific moment.")

    # Tailored physical example if available
    norm_key = (misconception_key or "").strip().lower()
    example_data = CONCEPTUAL_EXAMPLES.get(norm_key, None)

    example_html = ""
    if example_data:
        example_html = f"""
        <!-- 3. Physical Example / Thought Experiment (Visually Distinct: Cyan/Teal panel) -->
        <div style="
            background: rgba(6, 182, 212, 0.08);
            border: 1px solid rgba(6, 182, 212, 0.3);
            border-radius: 12px;
            padding: 1rem 1.15rem;
            margin-top: 0.85rem;
        ">
            <div style="display: flex; align-items: center; gap: 0.45rem; margin-bottom: 0.35rem;">
                <span style="font-size: 1rem;">🔬</span>
                <span style="font-size: 0.76rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #22d3ee;">
                    Physical Thought Experiment: {example_data['title']}
                </span>
            </div>
            <div style="font-size: 0.88rem; color: #e2e8f0; line-height: 1.55;">
                {example_data['description']}
            </div>
        </div>
        """

    card_html = f"""
    <div style="
        background: linear-gradient(135deg, rgba(19, 25, 45, 0.95) 0%, rgba(12, 17, 33, 0.95) 100%);
        border: 1px solid rgba(139, 92, 246, 0.35);
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), 0 0 25px rgba(139, 92, 246, 0.12);
    ">
        <!-- Main Section Kicker -->
        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 0.8rem; margin-bottom: 0.9rem; flex-wrap: wrap;">
            <div style="display: flex; align-items: center; gap: 0.65rem;">
                <div style="
                    width: 36px;
                    height: 36px;
                    border-radius: 10px;
                    background: linear-gradient(135deg, #8b5cf6 0%, #d946ef 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 18px;
                    box-shadow: 0 4px 14px rgba(139, 92, 246, 0.4);
                ">
                    💡
                </div>
                <div>
                    <div style="font-size: 0.72rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: #c084fc;">
                        PEDAGOGICAL INTERVENTION
                    </div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: #ffffff; letter-spacing: -0.015em;">
                        Let's Fix This Misconception
                    </div>
                </div>
            </div>

            <span style="
                font-size: 0.74rem;
                font-weight: 600;
                padding: 0.25rem 0.7rem;
                border-radius: 9999px;
                background: rgba(139, 92, 246, 0.18);
                color: #d8b4fe;
                border: 1px solid rgba(139, 92, 246, 0.35);
            ">
                🔑 {key_concept}
            </span>
        </div>

        <!-- 1. Misconception Explanation & Conceptual Clarification (Deep violet card) -->
        <div style="
            background: rgba(14, 21, 38, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 12px;
            padding: 1rem 1.15rem;
            margin-bottom: 0.85rem;
        ">
            <div style="font-size: 0.78rem; font-weight: 700; color: #a5b4fc; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.35rem;">
                📘 Core Scientific Principle ({title})
            </div>
            <div style="font-size: 0.92rem; color: #f1f5f9; line-height: 1.6;">
                {explanation}
            </div>
        </div>

        <!-- 2. Socratic Guided Hint (Visually Distinct: Amber callout card) -->
        <div style="
            background: rgba(245, 158, 11, 0.08);
            border-left: 3px solid #f59e0b;
            border-radius: 0 10px 10px 0;
            padding: 0.9rem 1.1rem;
            margin-bottom: 0.5rem;
        ">
            <div style="display: flex; align-items: center; gap: 0.4rem; font-size: 0.76rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #fbbf24; margin-bottom: 0.25rem;">
                <span>🧠</span> Guided Socratic Hint
            </div>
            <div style="font-size: 0.9rem; color: #fef3c7; font-style: italic; line-height: 1.5;">
                "{guided_hint}"
            </div>
        </div>

        {example_html}
    </div>
    """
    render_html(card_html)
