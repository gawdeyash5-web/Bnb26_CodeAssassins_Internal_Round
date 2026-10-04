import React from 'react';

export default function DiagnosisCard({ diagnosis, answerEvaluation, studentAnswer, onContinue }) {
  if (!diagnosis) return null;

  const {
    misconception_label,
    misconception_id,
    misconception_name,
    confidence_score,
    status,
    explanation,
    evidence_keywords,
  } = diagnosis;

  const evalData = answerEvaluation || diagnosis.answer_evaluation || {};
  const wasCorrect = evalData.was_correct || (misconception_label === 'no_misconception_detected' ? 'correct' : 'uncertain');
  const wasCorrectDisplay = evalData.was_it_correct_display || (wasCorrect === 'correct' ? 'Correct' : wasCorrect === 'incorrect' ? 'Incorrect' : 'Not enough information');
  const isTrulyCorrect = wasCorrect === 'correct';
  const isIncorrect = wasCorrect === 'incorrect';
  const isUncertain = wasCorrect === 'not_enough_information' || status === 'uncertain';
  const confidencePct = Math.round((confidence_score || 0) * 100);

  const displayedStudentAnswer = evalData.your_answer || studentAnswer || '';
  const displayedCorrectAnswer = evalData.correct_answer || '';
  const displayedWhy = evalData.why_explanation || explanation || '';

  return (
    <div className="card" style={{
      borderLeft: `4px solid ${isTrulyCorrect ? 'var(--teal-500)' : isIncorrect ? 'var(--red-500)' : 'var(--amber-500)'}`,
      position: 'relative',
    }}>
      {/* Top Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: '0.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span style={{ fontSize: '0.74rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.08em', color: '#a5b4fc' }}>
            CORRECT ANSWER AND EXPLANATION
          </span>
        </div>

        {/* Correctness Badge */}
        {isTrulyCorrect ? (
          <span className="badge badge-teal">✅ Your Answer Looks Correct</span>
        ) : isIncorrect ? (
          <span className="badge badge-red">❌ Incorrect</span>
        ) : (
          <span className="badge badge-amber">⚠️ Not Enough Information</span>
        )}
      </div>

      {/* Mandatory Section: Correct Answer and Explanation */}
      <div style={{
        background: 'rgba(15, 23, 42, 0.65)',
        border: '1px solid var(--border-subtle)',
        borderRadius: 'var(--radius-md)',
        padding: '1.15rem 1.25rem',
        marginBottom: '1.25rem',
        display: 'flex',
        flexDirection: 'column',
        gap: '0.9rem',
      }}>
        {/* Item 1: Your Answer */}
        <div>
          <div style={{ fontSize: '0.74rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '0.25rem' }}>
            1. Your Answer:
          </div>
          <div style={{ fontSize: '0.94rem', color: '#f1f5f9', fontStyle: 'italic', paddingLeft: '0.5rem', borderLeft: '2px solid rgba(255,255,255,0.2)' }}>
            "{displayedStudentAnswer || '(No text recorded)'}"
          </div>
        </div>

        {/* Item 2: Was It Correct? */}
        <div>
          <div style={{ fontSize: '0.74rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '0.25rem' }}>
            2. Was It Correct?
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{
              fontWeight: 800,
              fontSize: '0.92rem',
              color: isTrulyCorrect ? '#34d399' : isIncorrect ? '#f87171' : '#fbbf24',
            }}>
              {wasCorrectDisplay}
            </span>
            {isTrulyCorrect && (
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                (Remember: permanent mastery comes from applying this concept across multiple situations.)
              </span>
            )}
          </div>
        </div>

        {/* Item 3: Correct Answer */}
        {displayedCorrectAnswer && (
          <div>
            <div style={{ fontSize: '0.74rem', fontWeight: 700, color: '#38bdf8', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '0.25rem' }}>
              3. Correct Answer:
            </div>
            <div style={{ fontSize: '0.94rem', color: '#ffffff', fontWeight: 600, lineHeight: 1.5 }}>
              {displayedCorrectAnswer}
            </div>
          </div>
        )}

        {/* Item 4: Why? */}
        {displayedWhy && (
          <div>
            <div style={{ fontSize: '0.74rem', fontWeight: 700, color: '#2dd4bf', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '0.25rem' }}>
              4. Why?
            </div>
            <div style={{ fontSize: '0.9rem', color: '#e2e8f0', lineHeight: 1.6, whiteSpace: 'pre-line' }}>
              {displayedWhy}
            </div>
          </div>
        )}
      </div>

      {/* AI Diagnostic Context (Simplified student-friendly language) */}
      <div style={{
        paddingTop: '0.75rem',
        borderTop: '1px solid var(--border-subtle)',
        display: 'flex',
        flexDirection: 'column',
        gap: '0.4rem',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem' }}>
          <div style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
            What Our AI Thinks:
          </div>
          {confidence_score > 0 && (
            <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>
              Confidence: {confidencePct}%
            </span>
          )}
        </div>

        <p style={{ fontSize: '0.86rem', color: 'var(--text-secondary)', lineHeight: 1.5, margin: 0 }}>
          {isTrulyCorrect
            ? 'Your explanation matches the expected scientific reasoning.'
            : isUncertain
            ? (explanation || "You may have a misunderstanding here. We couldn't identify the exact reason from this answer yet.")
            : (explanation || `We detected a likely misunderstanding related to ${misconception_name || misconception_label.replace(/_/g, ' ')}.`)}
        </p>
      </div>

      {/* Continue Action */}
      {onContinue && (
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1.25rem' }}>
          <button
            type="button"
            onClick={onContinue}
            className="btn btn-primary"
            style={{ fontWeight: 700, fontSize: '0.88rem' }}
          >
            Continue to Targeted Lesson ➔
          </button>
        </div>
      )}
    </div>
  );
}
