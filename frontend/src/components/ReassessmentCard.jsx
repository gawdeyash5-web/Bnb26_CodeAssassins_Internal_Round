import React, { useState } from 'react';

export default function ReassessmentCard({
  reassessmentQuestion,
  originalMisconception,
  onReassess,
  isReassessing,
  reassessmentResult,
  onViewXRay,
  onTryAnother,
}) {
  const [reassessmentAnswer, setReassessmentAnswer] = useState('');

  if (!reassessmentQuestion) {
    return (
      <div className="card" style={{ padding: '2.5rem 1.5rem', textAlign: 'center', border: '1px solid var(--border-subtle)' }}>
        <div style={{ fontSize: '2rem', marginBottom: '0.75rem' }}>📋</div>
        <h3 style={{ fontSize: '1.15rem', color: '#ffffff', marginBottom: '0.5rem' }}>
          No Transfer Question Available
        </h3>
        <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', maxWidth: '500px', margin: '0 auto 1.25rem', lineHeight: 1.5 }}>
          A validated transfer question is not currently available for this specific concept. To ensure honest assessment, submissions are disabled until a suitable question is loaded.
        </p>
        {onTryAnother && (
          <button type="button" onClick={onTryAnother} className="btn btn-primary" style={{ fontWeight: 700 }}>
            Choose Another Topic ➔
          </button>
        )}
      </div>
    );
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    if (reassessmentAnswer.trim()) {
      onReassess(reassessmentQuestion, reassessmentAnswer.trim(), originalMisconception);
    }
  };

  const outcome = reassessmentResult?.outcome;

  return (
    <div className="card" style={{
      background: 'linear-gradient(135deg, rgba(16, 26, 46, 0.95) 0%, rgba(9, 16, 32, 0.95) 100%)',
      border: '1px solid rgba(20, 184, 166, 0.35)',
      boxShadow: '0 8px 30px rgba(0, 0, 0, 0.4)',
    }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem', flexWrap: 'wrap', gap: '0.4rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span style={{ fontSize: '0.74rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.08em', color: '#2dd4bf' }}>
            TRY A NEW QUESTION
          </span>
          <span className="badge badge-teal">Transfer Challenge</span>
        </div>
        <span style={{ fontSize: '0.76rem', color: '#94a3b8' }}>
          New Physical Context
        </span>
      </div>

      {/* Purpose Explanation */}
      <p style={{ fontSize: '0.86rem', color: '#cbd5e1', lineHeight: 1.5, marginBottom: '0.85rem' }}>
        Can you apply what you just learned to this <strong>completely new situation</strong>?
      </p>

      {/* Transfer Scenario Card */}
      <div style={{
        background: 'rgba(11, 20, 42, 0.85)',
        border: '1px solid rgba(20, 184, 166, 0.25)',
        borderRadius: 'var(--radius-md)',
        padding: '1.1rem 1.3rem',
        marginBottom: '1rem',
      }}>
        <div style={{ fontSize: '0.72rem', fontWeight: 700, color: '#5eead4', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '0.35rem' }}>
          New Scenario:
        </div>
        <div style={{ fontSize: '1.08rem', fontWeight: 600, color: '#ffffff', lineHeight: 1.55 }}>
          {reassessmentQuestion}
        </div>
      </div>

      {/* Transfer Answer Form (shown before submission) */}
      {!outcome && (
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
          <div>
            <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '0.35rem' }}>
              Your Explanation in this Situation:
            </label>
            <textarea
              value={reassessmentAnswer}
              onChange={(e) => setReassessmentAnswer(e.target.value)}
              placeholder="Apply the physical principle you learned above. What happens, and why?"
              rows={3}
            />
          </div>

          <button
            type="submit"
            className="btn btn-teal"
            disabled={isReassessing || !reassessmentAnswer.trim()}
            style={{ padding: '0.75rem 1.3rem', fontSize: '0.94rem', fontWeight: 700 }}
          >
            {isReassessing ? (
              <>Checking Your New Answer...</>
            ) : (
              <>Check My New Answer ➔</>
            )}
          </button>
        </form>
      )}

      {/* Reassessment Outcome Result Banner */}
      {outcome && (
        <div style={{
          marginTop: '0.5rem',
          padding: '1.1rem 1.3rem',
          borderRadius: 'var(--radius-md)',
          background: outcome === 'improved'
            ? 'rgba(20, 184, 166, 0.12)'
            : outcome === 'inconclusive'
            ? 'rgba(245, 158, 11, 0.12)'
            : 'rgba(239, 68, 68, 0.12)',
          border: `1px solid ${
            outcome === 'improved'
              ? 'rgba(20, 184, 166, 0.4)'
              : outcome === 'inconclusive'
              ? 'rgba(245, 158, 11, 0.4)'
              : 'rgba(239, 68, 68, 0.4)'
          }`,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.45rem', flexWrap: 'wrap', gap: '0.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ fontSize: '1.2rem' }}>
                {outcome === 'improved' ? '🎉' : outcome === 'inconclusive' ? '⏸️' : '⚠️'}
              </span>
              <span style={{
                fontWeight: 800,
                fontSize: '1.05rem',
                color: outcome === 'improved' ? '#34d399' : outcome === 'inconclusive' ? '#fbbf24' : '#f87171',
                textTransform: 'uppercase',
                letterSpacing: '0.04em',
              }}>
                {outcome === 'improved'
                  ? 'Your New Answer Shows Improvement'
                  : outcome === 'inconclusive'
                  ? 'We Need More Evidence'
                  : 'This Misunderstanding May Still Be Present'}
              </span>
            </div>

            <span className={`badge ${
              outcome === 'improved' ? 'badge-teal' : outcome === 'inconclusive' ? 'badge-amber' : 'badge-red'
            }`}>
              {outcome === 'improved' ? 'IMPROVED' : outcome === 'inconclusive' ? 'INCONCLUSIVE' : 'PERSISTENT'}
            </span>
          </div>

          <div style={{ fontSize: '0.88rem', color: '#e2e8f0', lineHeight: 1.55 }}>
            {reassessmentResult.feedback}
          </div>

          {/* Action Buttons: View X-Ray or Try Another */}
          <div style={{ marginTop: '1.25rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
            {onTryAnother && (
              <button
                type="button"
                onClick={onTryAnother}
                className="btn btn-secondary btn-sm"
                style={{ fontSize: '0.84rem' }}
              >
                🔄 Try Another Question
              </button>
            )}

            {onViewXRay && (
              <button
                type="button"
                onClick={onViewXRay}
                className="btn btn-teal"
                style={{
                  fontWeight: 800,
                  fontSize: '0.92rem',
                  padding: '0.65rem 1.25rem',
                  boxShadow: '0 4px 14px rgba(20, 184, 166, 0.4)',
                }}
              >
                Misconception X-Ray — View My Learning Journey ➔
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
