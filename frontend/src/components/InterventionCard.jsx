import React, { useState } from 'react';

export default function InterventionCard({ intervention, onContinue }) {
  const [showHint, setShowHint] = useState(false);
  const [showWorkedExample, setShowWorkedExample] = useState(false);

  if (!intervention) return null;

  const {
    title,
    key_concept,
    short_explanation,
    explanation,
    common_mistake,
    real_life_analogy,
    worked_example,
    guided_hint,
  } = intervention;

  return (
    <div className="card" style={{
      background: 'linear-gradient(135deg, rgba(16, 26, 52, 0.95) 0%, rgba(10, 18, 38, 0.95) 100%)',
      border: '1px solid rgba(14, 165, 233, 0.35)',
    }}>
      {/* Top Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.85rem', flexWrap: 'wrap', gap: '0.4rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span style={{ fontSize: '0.72rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.08em', color: '#38bdf8' }}>
            TARGETED LESSON & COUNTEREXAMPLE
          </span>
          <span className="badge badge-teal">Core Concept</span>
        </div>
        <span style={{ fontSize: '0.78rem', color: '#94a3b8' }}>
          Concept: <strong style={{ color: '#ffffff' }}>{key_concept}</strong>
        </span>
      </div>

      {/* Main Intervention Title & Core Explanation */}
      <h3 style={{ fontSize: '1.2rem', color: '#ffffff', marginBottom: '0.35rem' }}>
        💡 {title}
      </h3>
      <p style={{ fontSize: '0.9rem', color: '#cbd5e1', lineHeight: 1.6, marginBottom: '1rem' }}>
        {explanation || short_explanation}
      </p>

      {/* Side-by-side Intuitive Trap vs Physical Principle */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: common_mistake && real_life_analogy ? '1fr 1fr' : '1fr',
        gap: '0.85rem',
        marginBottom: '1rem',
      }}>
        {common_mistake && (
          <div style={{
            background: 'rgba(239, 68, 68, 0.08)',
            border: '1px solid rgba(239, 68, 68, 0.25)',
            borderRadius: 'var(--radius-md)',
            padding: '0.85rem',
          }}>
            <div style={{ fontSize: '0.74rem', fontWeight: 700, color: '#fca5a5', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>
              ⚠️ The Common Intuitive Trap:
            </div>
            <div style={{ fontSize: '0.82rem', color: '#fee2e2', lineHeight: 1.5 }}>
              {common_mistake}
            </div>
          </div>
        )}

        {real_life_analogy && (
          <div style={{
            background: 'rgba(20, 184, 166, 0.08)',
            border: '1px solid rgba(20, 184, 166, 0.25)',
            borderRadius: 'var(--radius-md)',
            padding: '0.85rem',
          }}>
            <div style={{ fontSize: '0.74rem', fontWeight: 700, color: '#5eead4', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>
              🔬 Real-World Analogy:
            </div>
            <div style={{ fontSize: '0.82rem', color: '#ccfbf1', lineHeight: 1.5 }}>
              {real_life_analogy}
            </div>
          </div>
        )}
      </div>

      {/* Socratic Hint & Worked Example Expanders */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        {guided_hint && (
          <div style={{
            background: 'rgba(255, 255, 255, 0.03)',
            border: '1px solid var(--border-subtle)',
            borderRadius: 'var(--radius-md)',
            overflow: 'hidden',
          }}>
            <button
              type="button"
              onClick={() => setShowHint(!showHint)}
              style={{
                width: '100%',
                background: 'transparent',
                border: 'none',
                padding: '0.65rem 0.9rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                color: '#93c5fd',
                fontSize: '0.84rem',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              <span>🔍 Socratic Hint {showHint ? '▲' : '▼'}</span>
              <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>
                {showHint ? 'Click to hide' : 'Need a nudge?'}
              </span>
            </button>
            {showHint && (
              <div style={{ padding: '0 0.9rem 0.75rem 0.9rem', fontSize: '0.84rem', color: '#e0f2fe', lineHeight: 1.55 }}>
                {guided_hint}
              </div>
            )}
          </div>
        )}

        {worked_example && (
          <div style={{
            background: 'rgba(255, 255, 255, 0.03)',
            border: '1px solid var(--border-subtle)',
            borderRadius: 'var(--radius-md)',
            overflow: 'hidden',
          }}>
            <button
              type="button"
              onClick={() => setShowWorkedExample(!showWorkedExample)}
              style={{
                width: '100%',
                background: 'transparent',
                border: 'none',
                padding: '0.65rem 0.9rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                color: '#c4b5fd',
                fontSize: '0.84rem',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              <span>📐 Concrete Worked Example {showWorkedExample ? '▲' : '▼'}</span>
              <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>
                {showWorkedExample ? 'Click to hide' : 'View breakdown'}
              </span>
            </button>
            {showWorkedExample && (
              <div style={{ padding: '0 0.9rem 0.75rem 0.9rem', fontSize: '0.84rem', color: '#f3e8ff', lineHeight: 1.55 }}>
                {worked_example}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Continue Action */}
      {onContinue && (
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1.25rem' }}>
          <button
            type="button"
            onClick={onContinue}
            className="btn btn-teal"
            style={{ fontWeight: 700, fontSize: '0.92rem' }}
          >
            Try a New Question to Test Yourself ➔
          </button>
        </div>
      )}
    </div>
  );
}
