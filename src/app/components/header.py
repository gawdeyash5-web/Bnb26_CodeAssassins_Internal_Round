"""Header component for Re:Learn application.

Renders the top branding, product identity, tagline, and real-time learner status.
"""

from typing import Any, Dict, List
import streamlit as st
from src.app.styles import render_html


def render_header(learner_id: str, history: List[Dict[str, Any]] = None):
    """Render the top Re:Learn header bar with brand identity and session status.

    Parameters
    ----------
    learner_id : str
        The active learner identifier.
    history : list of dict, optional
        Recorded attempts for the active learner.
    """
    attempt_count = len(history) if history else 0
    
    header_html = f"""
    <div style="
        position: relative;
        overflow: hidden;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(14, 21, 38, 0.95) 0%, rgba(10, 15, 29, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.09);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.6), 0 0 20px rgba(99, 102, 241, 0.12);
        padding: 1.25rem 1.6rem;
        margin-bottom: 1.25rem;
    ">
        <!-- Top decorative gradient accent line -->
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 35%, #ec4899 70%, #06b6d4 100%);
        "></div>

        <div style="
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
        ">
            <!-- Left Branding -->
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="
                    width: 44px;
                    height: 44px;
                    border-radius: 11px;
                    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 55%, #06b6d4 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 22px;
                    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.45);
                    flex-shrink: 0;
                ">
                    ⚛️
                </div>
                <div>
                    <div style="display: flex; align-items: center; gap: 0.65rem;">
                        <span style="
                            font-size: 1.55rem;
                            font-weight: 800;
                            letter-spacing: -0.025em;
                            color: #ffffff;
                            line-height: 1.15;
                        ">Re<span style="
                            background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
                            -webkit-background-clip: text;
                            -webkit-text-fill-color: transparent;
                        ">:Learn</span></span>
                        <span style="
                            font-size: 0.7rem;
                            font-weight: 700;
                            text-transform: uppercase;
                            letter-spacing: 0.09em;
                            padding: 0.18rem 0.55rem;
                            border-radius: 5px;
                            background: rgba(99, 102, 241, 0.16);
                            color: #a5b4fc;
                            border: 1px solid rgba(99, 102, 241, 0.32);
                        ">Adaptive Physics Learning</span>
                    </div>
                    <div style="
                        font-size: 0.86rem;
                        color: #94a3b8;
                        margin-top: 0.2rem;
                        font-weight: 400;
                    ">
                        Understand the mistake. Fix the misconception. Learn for real.
                    </div>
                </div>
            </div>

            <!-- Right Session Chips -->
            <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
                <div style="
                    display: flex;
                    align-items: center;
                    gap: 0.45rem;
                    padding: 0.35rem 0.8rem;
                    border-radius: 9999px;
                    background: rgba(16, 185, 129, 0.1);
                    border: 1px solid rgba(16, 185, 129, 0.28);
                ">
                    <span style="
                        width: 7px;
                        height: 7px;
                        border-radius: 50%;
                        background-color: #10b981;
                        box-shadow: 0 0 8px #10b981;
                        display: inline-block;
                    "></span>
                    <span style="font-size: 0.76rem; font-weight: 600; color: #34d399;">Active Session</span>
                </div>

                <div style="
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    padding: 0.35rem 0.85rem;
                    border-radius: 9999px;
                    background: rgba(99, 102, 241, 0.12);
                    border: 1px solid rgba(99, 102, 241, 0.25);
                    font-size: 0.78rem;
                    color: #c7d2fe;
                ">
                    <span>🧑‍🎓</span>
                    <span style="font-weight: 700; color: #ffffff;">{learner_id}</span>
                    <span style="color: #6366f1;">•</span>
                    <span style="color: #94a3b8;">{attempt_count} {'attempt' if attempt_count == 1 else 'attempts'}</span>
                </div>
            </div>
        </div>
    </div>
    """
    render_html(header_html)
