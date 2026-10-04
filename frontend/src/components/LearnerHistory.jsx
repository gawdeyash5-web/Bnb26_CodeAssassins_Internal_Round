import React from 'react';

export default function LearnerHistory({ history, onResetHistory, learnerId, onViewXRay, onStartLearning }) {
  if (!history || history.length === 0) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '3.5rem 1.5rem', maxWidth: '640px', margin: '2rem auto' }}>
        <div style={{ fontSize: '2.5rem', marginBottom: '0.85rem' }}>📈</div>
        <h3 style={{ fontSize: '1.25rem', color: '#ffffff', marginBottom: '0.4rem' }}>
          No Learning Attempts Recorded Yet
        </h3>
        <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', maxWidth: '440px', margin: '0 auto 1.5rem auto', lineHeight: 1.55 }}>
          Start your first physics challenge in the <strong>Learn</strong> section. Your conceptual progress and Misconception X-Ray will appear here.
        </p>
        {onStartLearning && (
          <button
            type="button"
            onClick={onStartLearning}
            className="btn btn-primary"
            style={{ fontWeight: 700 }}
          >
            🚀 Start Your First Challenge
          </button>
        )}
      </div>
    );
  }

  const improvedCount = history.filter((h) => h.reassessment_outcome === 'improved').length;
  const persistentCount = history.filter((h) => h.reassessment_outcome === 'persistent').length;
  const inconclusiveCount = history.filter((h) => h.reassessment_outcome === 'inconclusive').length;
  const pendingCount = history.filter((h) => !h.reassessment_completed).length;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', maxWidth: '1000px', margin: '0 auto' }}>
      {/* Top Stats Overview */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '1rem',
      }}>
        <div className="card" style={{ padding: '1rem 1.25rem' }}>
          <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 700 }}>
            Total Attempts
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#ffffff', marginTop: '0.2rem' }}>
            {history.length}
          </div>
        </div>

        <div className="card" style={{ padding: '1rem 1.25rem', borderLeft: '4px solid var(--teal-500)' }}>
          <div style={{ fontSize: '0.74rem', color: '#5eead4', textTransform: 'uppercase', fontWeight: 700 }}>
            Concepts Resolved
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#34d399', marginTop: '0.2rem' }}>
            {improvedCount}
          </div>
        </div>

        <div className="card" style={{ padding: '1rem 1.25rem', borderLeft: '4px solid var(--amber-500)' }}>
          <div style={{ fontSize: '0.74rem', color: '#fde68a', textTransform: 'uppercase', fontWeight: 700 }}>
            Needs More Evidence
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#fbbf24', marginTop: '0.2rem' }}>
            {inconclusiveCount}
          </div>
        </div>

        <div className="card" style={{ padding: '1rem 1.25rem', borderLeft: '4px solid var(--red-500)' }}>
          <div style={{ fontSize: '0.74rem', color: '#fca5a5', textTransform: 'uppercase', fontWeight: 700 }}>
            Needs Revisit
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#f87171', marginTop: '0.2rem' }}>
            {persistentCount + pendingCount}
          </div>
        </div>
      </div>

      {/* History Header & Clear Action */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '0.5rem' }}>
        <h3 style={{ fontSize: '1.15rem', color: '#ffffff' }}>
          Learning Journey History for <span style={{ color: '#818cf8' }}>{learnerId}</span>
        </h3>
        <button
          type="button"
          onClick={onResetHistory}
          className="btn btn-secondary btn-sm"
          style={{ fontSize: '0.76rem', color: '#f87171' }}
        >
          🗑️ Clear History
        </button>
      </div>

      {/* Timeline Feed */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {history.slice().reverse().map((item, idx) => {
          const attemptNum = history.length - idx;
          const conf = Math.round((item.confidence_score || 0) * 100);
          const outcome = item.reassessment_outcome;

          return (
            <div key={item.attempt_id || idx} className="card" style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.4rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                  <span style={{ fontWeight: 800, fontSize: '0.96rem', color: '#ffffff' }}>
                    Attempt #{attemptNum}
                  </span>
                  <span className="badge badge-indigo">
                    {item.misconception_label}
                  </span>
                  <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                    Confidence: {conf}%
                  </span>
                </div>

                {/* Outcome Badge */}
                {item.reassessment_completed ? (
                  <span className={`badge ${
                    outcome === 'improved' ? 'badge-teal' : outcome === 'inconclusive' ? 'badge-amber' : 'badge-red'
                  }`}>
                    {outcome === 'improved'
                      ? '✅ Improved'
                      : outcome === 'inconclusive'
                      ? '⚠️ Needs More Evidence'
                      : '❌ Persistent'}
                  </span>
                ) : (
                  <span className="badge badge-amber">Reassessment Pending</span>
                )}
              </div>

              {/* Initial Question & Answer */}
              <div style={{ background: 'rgba(0, 0, 0, 0.25)', borderRadius: 'var(--radius-sm)', padding: '0.75rem', fontSize: '0.84rem' }}>
                <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 700, marginBottom: '0.2rem' }}>
                  Question:
                </div>
                <div style={{ color: '#e2e8f0', marginBottom: '0.4rem' }}>
                  {item.question}
                </div>
                <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 700, marginBottom: '0.2rem' }}>
                  Your Initial Reasoning:
                </div>
                <div style={{ color: '#cbd5e1', fontStyle: 'italic' }}>
                  "{item.student_answer}"
                </div>
              </div>

              {/* Transfer Reassessment Feedback if available */}
              {item.reassessment_completed && (
                <div style={{
                  background: 'rgba(20, 184, 166, 0.05)',
                  border: '1px solid rgba(20, 184, 166, 0.2)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '0.75rem',
                  fontSize: '0.84rem',
                }}>
                  <div style={{ color: '#5eead4', fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 700, marginBottom: '0.2rem' }}>
                    Transfer Verification Result:
                  </div>
                  <div style={{ color: '#e2e8f0' }}>
                    {item.reassessment_feedback}
                  </div>
                </div>
              )}

              {/* Diagnostic Fork indicator if used */}
              {item.diagnostic_fork_used && (
                <div style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '0.4rem',
                  fontSize: '0.76rem',
                  color: '#fbbf24',
                  background: 'rgba(245, 158, 11, 0.12)',
                  border: '1px solid rgba(245, 158, 11, 0.25)',
                  padding: '0.25rem 0.6rem',
                  borderRadius: 'var(--radius-sm)',
                  width: 'fit-content',
                }}>
                  <span>🔀</span> Diagnostic Fork Applied ({item.diagnostic_fork_question_id})
                </div>
              )}

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '0.25rem', flexWrap: 'wrap', gap: '0.5rem' }}>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                  Recorded: {item.timestamp ? new Date(item.timestamp).toLocaleString() : 'Recent'}
                </div>

                {onViewXRay && (
                  <button
                    type="button"
                    onClick={() => onViewXRay(attemptNum - 1)}
                    className="btn btn-sm btn-teal"
                    style={{ fontSize: '0.82rem', fontWeight: 700, padding: '0.35rem 0.85rem' }}
                  >
                    🔍 Misconception X-Ray — View My Learning Journey ➔
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
