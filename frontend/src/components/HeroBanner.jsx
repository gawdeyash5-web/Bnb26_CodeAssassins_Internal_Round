import React from 'react';

export default function HeroBanner({ onOpenFork, onOpenXRay }) {
  return (
    <div style={{
      background: 'linear-gradient(135deg, rgba(17, 29, 61, 0.85) 0%, rgba(10, 18, 38, 0.95) 100%)',
      border: '1px solid rgba(99, 102, 241, 0.25)',
      borderRadius: 'var(--radius-lg)',
      padding: '1.25rem 1.6rem',
      marginBottom: '1.25rem',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      flexWrap: 'wrap',
      gap: '1.2rem',
      boxShadow: 'var(--shadow-sm)',
    }}>
      <div style={{ maxWidth: '720px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.35rem', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.74rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.08em', color: '#a5b4fc' }}>
            The Physics Cognitive Diagnostic System
          </span>
          <span className="badge badge-teal">Newtonian Mechanics</span>
        </div>
        <h2 style={{ fontSize: '1.35rem', fontWeight: 800, color: '#ffffff', marginBottom: '0.35rem' }}>
          Why do students struggle with physics?
        </h2>
        <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.55, marginBottom: '0.85rem' }}>
          Standard quizzes only grade right vs wrong. <strong>Re:Learn</strong> uses cognitive diagnostic classifiers to identify the student's <em>underlying misconception</em>, deploys <strong>Diagnostic Forks</strong> to resolve diagnostic ambiguity, guides remediation with targeted interventions, and proves transfer with <strong>Misconception X-Ray</strong>.
        </p>

        {/* Quick Access Badges for Signature Features */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', flexWrap: 'wrap' }}>
          {onOpenFork && (
            <button
              type="button"
              onClick={onOpenFork}
              className="btn btn-sm btn-secondary"
              style={{
                fontSize: '0.78rem',
                fontWeight: 700,
                color: '#fbbf24',
                borderColor: 'rgba(245, 158, 11, 0.35)',
                background: 'rgba(245, 158, 11, 0.08)',
              }}
            >
              🔀 Diagnostic Fork — Investigate My Thinking
            </button>
          )}

          {onOpenXRay && (
            <button
              type="button"
              onClick={onOpenXRay}
              className="btn btn-sm btn-secondary"
              style={{
                fontSize: '0.78rem',
                fontWeight: 700,
                color: '#5eead4',
                borderColor: 'rgba(20, 184, 166, 0.35)',
                background: 'rgba(20, 184, 166, 0.08)',
              }}
            >
              🔍 Misconception X-Ray — View My Learning Journey
            </button>
          )}
        </div>
      </div>

      {/* 5-Stage Learning Loop Visualizer */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '0.35rem',
        background: 'rgba(7, 13, 30, 0.6)',
        padding: '0.6rem 0.8rem',
        borderRadius: 'var(--radius-md)',
        border: '1px solid var(--border-subtle)',
        fontSize: '0.74rem',
        color: 'var(--text-secondary)',
        flexWrap: 'wrap',
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ color: '#818cf8', fontWeight: 700 }}>1. Reason</div>
          <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>Initial Answer</div>
        </div>
        <span style={{ color: 'var(--text-muted)' }}>→</span>
        <div style={{ textAlign: 'center' }}>
          <div style={{ color: '#fbbf24', fontWeight: 700 }}>2. Fork</div>
          <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>Clarify Probe</div>
        </div>
        <span style={{ color: 'var(--text-muted)' }}>→</span>
        <div style={{ textAlign: 'center' }}>
          <div style={{ color: '#60a5fa', fontWeight: 700 }}>3. Intervene</div>
          <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>Targeted Analogy</div>
        </div>
        <span style={{ color: 'var(--text-muted)' }}>→</span>
        <div style={{ textAlign: 'center' }}>
          <div style={{ color: '#38bdf8', fontWeight: 700 }}>4. Transfer</div>
          <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>Reassessment</div>
        </div>
        <span style={{ color: 'var(--text-muted)' }}>→</span>
        <div style={{ textAlign: 'center' }}>
          <div style={{ color: '#34d399', fontWeight: 700 }}>5. X-Ray</div>
          <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>Audit Journey</div>
        </div>
      </div>
    </div>
  );
}
