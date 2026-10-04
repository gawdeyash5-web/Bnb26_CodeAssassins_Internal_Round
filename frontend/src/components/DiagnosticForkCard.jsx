import React, { useState } from 'react';

export default function DiagnosticForkCard({
  forkData,
  onEvaluate,
  isEvaluating,
  evaluationResult,
  onContinue,
  onSkip,
}) {
  const [selectedChoiceId, setSelectedChoiceId] = useState('');
  const [reasoningText, setReasoningText] = useState('');
  const [hasSubmitted, setHasSubmitted] = useState(false);

  if (!forkData || !forkData.question) return null;

  const { question, candidate_ids, candidate_labels, reason } = forkData;
  const isCompleted = hasSubmitted || !!evaluationResult;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedChoiceId) return;
    setHasSubmitted(true);
    onEvaluate(question.question_id, selectedChoiceId, reasoningText);
  };

  return (
    <div
      className="card"
      style={{
        border: '1px solid rgba(245, 158, 11, 0.45)',
        background: 'linear-gradient(180deg, rgba(245, 158, 11, 0.08) 0%, rgba(17, 29, 61, 0.95) 100%)',
        position: 'relative',
        boxShadow: '0 8px 32px rgba(245, 158, 11, 0.15)',
      }}
    >
      {/* Header Badge & Title */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '1rem',
          flexWrap: 'wrap',
          gap: '0.5rem',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <div
            style={{
              width: '28px',
              height: '28px',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '14px',
              fontWeight: 800,
              color: '#070d1e',
            }}
          >
            🔀
          </div>
          <div>
            <span
              style={{
                fontSize: '0.72rem',
                fontWeight: 800,
                textTransform: 'uppercase',
                letterSpacing: '0.08em',
                color: '#fbbf24',
              }}
            >
              FOLLOW-UP QUESTION
            </span>
            <h3 style={{ fontSize: '1.2rem', color: '#ffffff', margin: 0 }}>
              One More Question to Understand Your Thinking
            </h3>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
          <span className="badge badge-amber">Clarifying Question</span>
        </div>
      </div>

      {/* Student-Friendly Explanation (No ML Jargon) */}
      <div
        style={{
          background: 'rgba(0, 0, 0, 0.3)',
          border: '1px solid rgba(255, 255, 255, 0.08)',
          borderRadius: 'var(--radius-md)',
          padding: '0.85rem 1rem',
          marginBottom: '1.25rem',
          fontSize: '0.86rem',
          color: '#e2e8f0',
          lineHeight: 1.55,
        }}
      >
        <p style={{ margin: 0 }}>
          💡 <strong>Why this question?</strong> Our diagnostic analysis noticed two possible interpretations in your previous response. To select the most helpful intervention for your exact mental model, consider this follow-up challenge.
        </p>
      </div>

      {/* The Diagnostic Question Prompt */}
      <div style={{ marginBottom: '1.25rem' }}>
        <div
          style={{
            fontSize: '0.78rem',
            textTransform: 'uppercase',
            letterSpacing: '0.06em',
            color: 'var(--text-muted)',
            fontWeight: 700,
            marginBottom: '0.35rem',
          }}
        >
          {question.scenario_title || 'Targeted Probe Scenario'}
        </div>
        <p
          style={{
            fontSize: '1.02rem',
            fontWeight: 600,
            color: '#f8fafc',
            lineHeight: 1.5,
            margin: 0,
          }}
        >
          {question.question}
        </p>
      </div>

      {/* Pre-submission: Choice Selection Form */}
      {!isCompleted ? (
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
            {question.choices.map((choice) => {
              const isSelected = selectedChoiceId === choice.choice_id;
              return (
                <div
                  key={choice.choice_id}
                  onClick={() => setSelectedChoiceId(choice.choice_id)}
                  style={{
                    background: isSelected ? 'rgba(99, 102, 241, 0.16)' : 'rgba(12, 21, 46, 0.7)',
                    border: isSelected
                      ? '1.5px solid #818cf8'
                      : '1px solid rgba(255, 255, 255, 0.09)',
                    borderRadius: 'var(--radius-md)',
                    padding: '0.85rem 1rem',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: '0.85rem',
                    transition: 'all 0.15s ease',
                  }}
                >
                  <div
                    style={{
                      width: '24px',
                      height: '24px',
                      borderRadius: '50%',
                      border: isSelected ? '2px solid #818cf8' : '2px solid var(--text-muted)',
                      background: isSelected ? '#4f46e5' : 'transparent',
                      color: isSelected ? '#ffffff' : 'var(--text-muted)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '0.78rem',
                      fontWeight: 800,
                      flexShrink: 0,
                      marginTop: '2px',
                    }}
                  >
                    {choice.choice_id}
                  </div>
                  <div style={{ flex: 1, fontSize: '0.9rem', color: isSelected ? '#ffffff' : '#cbd5e1', lineHeight: 1.45 }}>
                    {choice.text}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Optional reasoning text input */}
          <div style={{ marginTop: '0.5rem' }}>
            <label
              htmlFor="fork-reasoning"
              style={{
                display: 'block',
                fontSize: '0.78rem',
                color: 'var(--text-muted)',
                fontWeight: 600,
                marginBottom: '0.35rem',
              }}
            >
              Optional: Briefly state why you chose this option
            </label>
            <textarea
              id="fork-reasoning"
              value={reasoningText}
              onChange={(e) => setReasoningText(e.target.value)}
              placeholder="e.g. In my view, because there are no opposing forces..."
              rows={2}
              style={{ minHeight: '60px', fontSize: '0.86rem' }}
            />
          </div>

          {/* Action Buttons */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '0.5rem', flexWrap: 'wrap', gap: '0.75rem' }}>
            <button
              type="button"
              onClick={onSkip}
              className="btn btn-secondary btn-sm"
              style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}
            >
              Skip Fork & Proceed with Initial Diagnosis
            </button>

            <button
              type="submit"
              disabled={!selectedChoiceId || isEvaluating}
              className="btn btn-primary"
              style={{
                background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
                borderColor: 'rgba(245, 158, 11, 0.4)',
                color: '#070d1e',
                fontWeight: 800,
              }}
            >
              {isEvaluating ? 'Evaluating Evidence...' : 'Submit Choice & Refine Diagnosis ➔'}
            </button>
          </div>
        </form>
      ) : (
        /* Post-submission: Refined Diagnosis & Evidence Feedback */
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {evaluationResult && (
            <div
              style={{
                background:
                  evaluationResult.refined_diagnosis?.status === 'uncertain'
                    ? 'var(--amber-bg)'
                    : 'rgba(20, 184, 166, 0.12)',
                border:
                  evaluationResult.refined_diagnosis?.status === 'uncertain'
                    ? '1px solid var(--amber-border)'
                    : '1px solid var(--teal-border)',
                borderRadius: 'var(--radius-md)',
                padding: '1rem',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.4rem' }}>
                <span style={{ fontSize: '1.1rem' }}>
                  {evaluationResult.refined_diagnosis?.status === 'uncertain' ? '⚠️' : '🎯'}
                </span>
                <span
                  style={{
                    fontSize: '0.82rem',
                    fontWeight: 800,
                    textTransform: 'uppercase',
                    color:
                      evaluationResult.refined_diagnosis?.status === 'uncertain'
                        ? '#fbbf24'
                        : '#5eead4',
                  }}
                >
                  Refined Diagnosis: {evaluationResult.refined_diagnosis?.misconception_name || evaluationResult.refined_diagnosis?.misconception_id}
                </span>
                <span
                  style={{
                    marginLeft: 'auto',
                    fontSize: '0.78rem',
                    fontWeight: 700,
                    color: '#ffffff',
                    background: 'rgba(0, 0, 0, 0.3)',
                    padding: '0.15rem 0.5rem',
                    borderRadius: 'var(--radius-full)',
                  }}
                >
                  Confidence: {Math.round((evaluationResult.refined_diagnosis?.confidence_score || 0) * 100)}%
                </span>
              </div>

              <p style={{ fontSize: '0.88rem', color: '#e2e8f0', margin: '0 0 0.5rem 0', lineHeight: 1.5 }}>
                {evaluationResult.evidence_summary}
              </p>

              {evaluationResult.post_answer_explanation && (
                <div
                  style={{
                    background: 'rgba(0, 0, 0, 0.25)',
                    borderRadius: 'var(--radius-sm)',
                    padding: '0.65rem 0.85rem',
                    fontSize: '0.82rem',
                    color: '#cbd5e1',
                    lineHeight: 1.45,
                    borderLeft: '3px solid #818cf8',
                  }}
                >
                  <strong>Physical Principle:</strong> {evaluationResult.post_answer_explanation}
                </div>
              )}
            </div>
          )}

          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '0.25rem' }}>
            <button
              type="button"
              onClick={onContinue}
              className="btn btn-teal"
              style={{ fontWeight: 800 }}
            >
              Continue to Targeted Intervention ➔
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
