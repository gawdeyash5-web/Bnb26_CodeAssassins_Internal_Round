import React from 'react';

export default function HowItWorks({ onStartLearning }) {
  return (
    <div style={{ maxWidth: '840px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Header */}
      <div className="card" style={{ padding: '2rem 1.75rem', textAlign: 'center' }}>
        <div style={{ display: 'inline-flex', padding: '0.4rem 0.8rem', borderRadius: 'var(--radius-full)', background: 'rgba(99, 102, 241, 0.12)', border: '1px solid rgba(99, 102, 241, 0.3)', color: '#a5b4fc', fontSize: '0.8rem', fontWeight: 700, marginBottom: '0.75rem' }}>
          THE RE:LEARN PEDAGOGY
        </div>
        <h2 style={{ fontSize: '1.75rem', color: '#ffffff', marginBottom: '0.5rem', letterSpacing: '-0.02em' }}>
          How Re:Learn Works
        </h2>
        <p style={{ fontSize: '0.95rem', color: 'var(--text-secondary)', maxWidth: '620px', margin: '0 auto', lineHeight: 1.6 }}>
          Standard quizzes only grade answers as right or wrong. Re:Learn uncovers <em>why</em> you answered the way you did, guides you through intuitive physics traps, and verifies that you can apply physical laws to fresh situations.
        </p>
      </div>

      {/* 3 Core Pillars */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {/* Pillar 1: Diagnosis */}
        <div className="card" style={{ borderLeft: '4px solid #6366f1', padding: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.5rem' }}>
            <span style={{ fontSize: '1.3rem' }}>🎯</span>
            <h3 style={{ fontSize: '1.15rem', color: '#ffffff', margin: 0 }}>
              1. Diagnosis over Grading
            </h3>
          </div>
          <p style={{ fontSize: '0.9rem', color: '#cbd5e1', lineHeight: 1.6, margin: 0 }}>
            Instead of multiple-choice guessing, you explain the physical scenario in your own words. Our AI analyzes your reasoning against canonical Newtonian mechanics and identifies the exact misconception you may be holding (such as the belief that continuous motion requires a continuous force).
          </p>
        </div>

        {/* Pillar 2: Diagnostic Fork (Signature Feature) */}
        <div className="card" style={{ borderLeft: '4px solid #f59e0b', padding: '1.5rem', background: 'linear-gradient(180deg, rgba(245, 158, 11, 0.04) 0%, rgba(17, 29, 61, 0.8) 100%)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '0.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <span style={{ fontSize: '1.3rem' }}>🔀</span>
              <h3 style={{ fontSize: '1.15rem', color: '#ffffff', margin: 0 }}>
                2. Diagnostic Fork: Resolving Ambiguity
              </h3>
            </div>
            <span className="badge badge-amber">Signature Feature</span>
          </div>
          <p style={{ fontSize: '0.9rem', color: '#cbd5e1', lineHeight: 1.6, margin: '0 0 0.75rem 0' }}>
            Sometimes an explanation contains words that could match more than one misconception. Rather than making a blind guess, Re:Learn presents a <strong>Diagnostic Fork</strong>: a single targeted follow-up scenario that cleanly distinguishes between competing interpretations.
          </p>
          <div style={{ background: 'rgba(0, 0, 0, 0.25)', borderRadius: 'var(--radius-sm)', padding: '0.75rem 1rem', fontSize: '0.84rem', color: '#fef3c7', lineHeight: 1.5 }}>
            <strong>Why this matters:</strong> You are never forced into the wrong explanation. The system gathers targeted evidence first, then provides the remediation that matches your exact thinking.
          </div>
        </div>

        {/* Pillar 3: Transfer & Misconception X-Ray */}
        <div className="card" style={{ borderLeft: '4px solid #14b8a6', padding: '1.5rem', background: 'linear-gradient(180deg, rgba(20, 184, 166, 0.04) 0%, rgba(17, 29, 61, 0.8) 100%)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '0.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
              <span style={{ fontSize: '1.3rem' }}>🔍</span>
              <h3 style={{ fontSize: '1.15rem', color: '#ffffff', margin: 0 }}>
                3. Transfer Verification & Misconception X-Ray
              </h3>
            </div>
            <span className="badge badge-teal">Signature Feature</span>
          </div>
          <p style={{ fontSize: '0.9rem', color: '#cbd5e1', lineHeight: 1.6, margin: '0 0 0.75rem 0' }}>
            After you review the targeted counterexample and analogy, we test your understanding on a <strong>different transfer question</strong>. Merely repeating the lesson is not enough — true learning means applying the law in a new context.
          </p>
          <p style={{ fontSize: '0.9rem', color: '#cbd5e1', lineHeight: 1.6, margin: 0 }}>
            The <strong>Misconception X-Ray</strong> reveals the complete journey: initial reasoning → diagnostic evidence → targeted intervention → transfer answer → observed outcome (Improved, Persistent, or Inconclusive).
          </p>
        </div>
      </div>

      {/* CTA Button */}
      <div style={{ textAlign: 'center', marginTop: '0.5rem' }}>
        <button
          type="button"
          onClick={onStartLearning}
          className="btn btn-primary"
          style={{ padding: '0.85rem 2rem', fontSize: '1rem', fontWeight: 700 }}
        >
          🚀 Start Learning Physics
        </button>
      </div>
    </div>
  );
}
