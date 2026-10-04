import React from 'react';

export default function TaxonomyExplorer({ taxonomy }) {
  if (!taxonomy || taxonomy.length === 0) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
        <p style={{ color: 'var(--text-muted)' }}>Loading physics taxonomy catalog...</p>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      <div style={{ maxWidth: '820px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.35rem' }}>
          <span style={{ fontSize: '0.74rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.08em', color: '#818cf8' }}>
            Pedagogical Knowledge Base
          </span>
          <span className="badge badge-indigo">{taxonomy.length} Core Concepts</span>
        </div>
        <h2 style={{ fontSize: '1.45rem', fontWeight: 800, color: '#ffffff', marginBottom: '0.35rem' }}>
          Curated Physics Misconception Taxonomy
        </h2>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
          Standardized conceptual catalog mapping student intuitive fallacies to formal Newtonian mechanics principles.
        </p>
      </div>

      {/* Grid of Concept Cards */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))',
        gap: '1.25rem',
      }}>
        {taxonomy.map((item) => {
          const isCorrect = item.misconception_id === 'NONE';

          return (
            <div
              key={item.misconception_id}
              className="card"
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '0.85rem',
                borderTop: `4px solid ${isCorrect ? 'var(--teal-500)' : 'var(--indigo-500)'}`,
              }}
            >
              {/* Card Header */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className="badge badge-indigo">
                  {item.misconception_id}
                </span>
                <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                  {item.misconception_label}
                </span>
              </div>

              <div>
                <h3 style={{ fontSize: '1.15rem', color: '#ffffff', marginBottom: '0.35rem' }}>
                  {item.misconception_name}
                </h3>
                <p style={{ fontSize: '0.86rem', color: '#94a3b8', lineHeight: 1.55 }}>
                  {item.simple_description || item.common_reasoning_error}
                </p>
              </div>

              {/* Principle vs Trap */}
              <div style={{
                background: 'rgba(20, 184, 166, 0.08)',
                border: '1px solid rgba(20, 184, 166, 0.25)',
                borderRadius: 'var(--radius-md)',
                padding: '0.8rem 0.95rem',
              }}>
                <div style={{ fontSize: '0.72rem', fontWeight: 700, color: '#5eead4', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>
                  Canonical Physical Law:
                </div>
                <div style={{ fontSize: '0.82rem', color: '#ccfbf1', lineHeight: 1.5 }}>
                  {item.scientifically_correct_concept || item.simple_intervention}
                </div>
              </div>

              {item.real_life_analogy && (
                <div style={{ fontSize: '0.8rem', color: '#cbd5e1', lineHeight: 1.5 }}>
                  <strong style={{ color: '#818cf8' }}>Counterexample:</strong> {item.real_life_analogy}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
