import React, { useState, useEffect } from 'react';

export default function MisconceptionXRay({
  history,
  activeAttemptIndex,
  onSelectAttempt,
  onStartLearning,
}) {
  const [selectedIdx, setSelectedIdx] = useState(
    activeAttemptIndex !== undefined && activeAttemptIndex !== null && activeAttemptIndex >= 0
      ? activeAttemptIndex
      : history && history.length > 0
      ? history.length - 1
      : 0
  );

  useEffect(() => {
    if (activeAttemptIndex !== undefined && activeAttemptIndex !== null && activeAttemptIndex >= 0) {
      setSelectedIdx(activeAttemptIndex);
    }
  }, [activeAttemptIndex]);

  // If no history at all, show useful empty state
  if (!history || history.length === 0) {
    return (
      <div
        className="card"
        style={{
          textAlign: 'center',
          padding: '4rem 1.5rem',
          maxWidth: '680px',
          margin: '2rem auto',
          border: '1px dashed var(--border-subtle)',
        }}
      >
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🔬</div>
        <h2 style={{ fontSize: '1.4rem', color: '#ffffff', marginBottom: '0.5rem' }}>
          Misconception X-Ray — View My Learning Journey
        </h2>
        <p
          style={{
            fontSize: '0.92rem',
            color: 'var(--text-secondary)',
            lineHeight: 1.6,
            marginBottom: '1.5rem',
          }}
        >
          No learning journeys have been recorded yet. The Misconception X-Ray visualizes the complete cognitive progression of a student from initial misconceptions through targeted interventions to transfer reassessments.
        </p>
        <button
          type="button"
          onClick={onStartLearning}
          className="btn btn-primary"
          style={{ padding: '0.75rem 1.5rem', fontSize: '0.95rem' }}
        >
          🚀 Start a Challenge in Diagnostic Lab
        </button>
      </div>
    );
  }

  // Get active attempt
  const currentAttempt = history[selectedIdx] || history[history.length - 1];

  // Helper mappings
  const outcome = currentAttempt.reassessment_outcome || 'not_assessed';
  const isImproved = outcome === 'improved';
  const isPersistent = outcome === 'persistent';
  const isInconclusive = outcome === 'inconclusive';

  const initialConf = Math.round((currentAttempt.initial_confidence_score || currentAttempt.confidence_score || 0) * 100);
  const finalConf = Math.round((currentAttempt.confidence_score || 0) * 100);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', maxWidth: '1080px', margin: '0 auto' }}>
      {/* Title & Description Banner */}
      <div
        className="card"
        style={{
          background: 'linear-gradient(135deg, rgba(14, 23, 46, 0.95) 0%, rgba(20, 184, 166, 0.08) 100%)',
          border: '1px solid rgba(20, 184, 166, 0.25)',
          padding: '1.5rem',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
              <span className="badge badge-teal">SIGNATURE FEATURE</span>
              <span style={{ fontSize: '0.76rem', color: 'var(--text-muted)' }}>
                COGNITIVE PROGRESSION AUDIT
              </span>
            </div>
            <h2 style={{ fontSize: '1.5rem', color: '#ffffff', letterSpacing: '-0.02em', margin: 0 }}>
              Misconception X-Ray — View My Learning Journey
            </h2>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', marginTop: '0.35rem', maxWidth: '640px' }}>
              Inspect the step-by-step evidence trail: from the student's initial intuitive reasoning and ML diagnosis, through the Diagnostic Fork and pedagogical intervention, to the final transfer reassessment.
            </p>
          </div>

          {/* Attempt Selector */}
          {history.length > 1 && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem', minWidth: '200px' }}>
              <label
                htmlFor="attempt-select"
                style={{ fontSize: '0.74rem', textTransform: 'uppercase', fontWeight: 700, color: 'var(--text-muted)' }}
              >
                Select Attempt ({history.length} recorded)
              </label>
              <select
                id="attempt-select"
                value={selectedIdx}
                onChange={(e) => {
                  const idx = parseInt(e.target.value, 10);
                  setSelectedIdx(idx);
                  if (onSelectAttempt) onSelectAttempt(idx);
                }}
                style={{
                  background: '#0a1128',
                  border: '1px solid rgba(255, 255, 255, 0.15)',
                  color: '#ffffff',
                  padding: '0.5rem 0.75rem',
                  borderRadius: 'var(--radius-md)',
                  fontSize: '0.85rem',
                  cursor: 'pointer',
                }}
              >
                {history.map((att, i) => (
                  <option key={att.attempt_id || i} value={i}>
                    Attempt #{i + 1} — {att.misconception_label || 'Concept'} ({att.reassessment_outcome?.toUpperCase() || 'IN PROGRESS'})
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>
      </div>

      {/* 5-STAGE SEQUENTIAL TIMELINE */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>

        {/* ========================================================
            STAGE A: INITIAL REASONING
           ======================================================== */}
        <div
          className="card"
          style={{
            borderLeft: '4px solid #6366f1',
            background: 'var(--bg-card)',
            position: 'relative',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <div style={{
                width: '26px',
                height: '26px',
                borderRadius: '50%',
                background: '#4f46e5',
                color: '#ffffff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '0.8rem',
                fontWeight: 800
              }}>
                A
              </div>
              <span style={{ fontSize: '0.84rem', fontWeight: 800, textTransform: 'uppercase', color: '#c7d2fe', letterSpacing: '0.05em' }}>
                Stage 1: Initial Reasoning & Baseline Diagnosis
              </span>
            </div>
            <span className="badge badge-indigo">
              {currentAttempt.initial_misconception_id || currentAttempt.misconception_id || 'M1'}
            </span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
            {/* Original Question Prompt */}
            <div style={{ background: 'rgba(0, 0, 0, 0.25)', padding: '0.9rem', borderRadius: 'var(--radius-sm)' }}>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 700, marginBottom: '0.25rem' }}>
                Original Physics Question
              </div>
              <div style={{ fontSize: '0.9rem', color: '#f8fafc', lineHeight: 1.45 }}>
                {currentAttempt.question}
              </div>
            </div>

            {/* Student's Actual Initial Answer & Correctness */}
            <div style={{ background: 'rgba(0, 0, 0, 0.25)', padding: '0.9rem', borderRadius: 'var(--radius-sm)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.25rem' }}>
                <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 700 }}>
                  Student's Actual Answer
                </span>
                <span style={{
                  fontSize: '0.75rem',
                  fontWeight: 800,
                  color: currentAttempt.was_correct === 'correct' ? '#34d399' : currentAttempt.was_correct === 'incorrect' ? '#f87171' : '#fbbf24',
                }}>
                  {currentAttempt.was_correct === 'correct' ? '✅ Correct' : currentAttempt.was_correct === 'incorrect' ? '❌ Incorrect' : '⚠️ Unverified'}
                </span>
              </div>
              <div style={{ fontSize: '0.9rem', color: '#e2e8f0', fontStyle: 'italic', lineHeight: 1.45 }}>
                "{currentAttempt.student_answer}"
              </div>
              {currentAttempt.correct_answer && (
                <div style={{ marginTop: '0.5rem', fontSize: '0.8rem', color: '#94a3b8' }}>
                  <strong style={{ color: '#38bdf8' }}>Expected: </strong>
                  {currentAttempt.correct_answer}
                </div>
              )}
            </div>
          </div>

          {/* Model Prediction Metrics */}
          <div style={{
            marginTop: '0.85rem',
            paddingTop: '0.85rem',
            borderTop: '1px solid var(--border-subtle)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: '0.75rem',
            fontSize: '0.82rem',
          }}>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>What Our AI Thinks: </span>
              <strong style={{ color: '#ffffff' }}>
                {currentAttempt.initial_misconception_label === 'uncertain_misunderstanding' || currentAttempt.misconception_label === 'uncertain_misunderstanding'
                  ? "We couldn't identify a specific misunderstanding yet"
                  : currentAttempt.initial_misconception_label || currentAttempt.misconception_label}
              </strong>
              <span style={{ color: 'var(--text-muted)', marginLeft: '0.5rem' }}>
                (Confidence: {initialConf}%)
              </span>
            </div>

            {currentAttempt.initial_evidence_keywords && currentAttempt.initial_evidence_keywords.length > 0 && (
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)', fontWeight: 600 }}>Keywords:</span>
                {currentAttempt.initial_evidence_keywords.map((kw, i) => (
                  <span
                    key={i}
                    style={{
                      background: 'rgba(255, 255, 255, 0.06)',
                      borderRadius: 'var(--radius-sm)',
                      padding: '0.15rem 0.45rem',
                      fontSize: '0.72rem',
                      fontFamily: 'var(--font-mono)',
                      color: '#cbd5e1',
                    }}
                  >
                    "{kw}"
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Visual Connector */}
        <div style={{ display: 'flex', justifyContent: 'center', margin: '-0.35rem 0' }}>
          <span style={{ color: 'var(--text-muted)', fontSize: '1.2rem' }}>↓</span>
        </div>

        {/* ========================================================
            STAGE B: DIAGNOSTIC INVESTIGATION (DIAGNOSTIC FORK)
           ======================================================== */}
        <div
          className="card"
          style={{
            borderLeft: `4px solid ${currentAttempt.diagnostic_fork_used ? 'var(--amber-500)' : 'var(--border-subtle)'}`,
            background: currentAttempt.diagnostic_fork_used ? 'rgba(245, 158, 11, 0.04)' : 'var(--bg-card)',
            position: 'relative',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <div style={{
                width: '26px',
                height: '26px',
                borderRadius: '50%',
                background: currentAttempt.diagnostic_fork_used ? '#f59e0b' : '#334155',
                color: currentAttempt.diagnostic_fork_used ? '#070d1e' : '#94a3b8',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '0.8rem',
                fontWeight: 800
              }}>
                B
              </div>
              <span style={{
                fontSize: '0.84rem',
                fontWeight: 800,
                textTransform: 'uppercase',
                color: currentAttempt.diagnostic_fork_used ? '#fbbf24' : 'var(--text-muted)',
                letterSpacing: '0.05em'
              }}>
                Stage 2: Diagnostic Investigation {currentAttempt.diagnostic_fork_used ? '(Diagnostic Fork Active)' : '(Direct Path)'}
              </span>
            </div>

            {currentAttempt.diagnostic_fork_used ? (
              <span className="badge badge-amber">Fork Evidence Applied</span>
            ) : (
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Fork Skipped / Not Required</span>
            )}
          </div>

          {currentAttempt.diagnostic_fork_used ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {/* Follow-up question & response */}
              <div style={{ background: 'rgba(0, 0, 0, 0.25)', padding: '0.9rem', borderRadius: 'var(--radius-sm)' }}>
                <div style={{ fontSize: '0.72rem', color: '#fbbf24', textTransform: 'uppercase', fontWeight: 700, marginBottom: '0.2rem' }}>
                  Targeted Clarifying Question ({currentAttempt.diagnostic_fork_question_id})
                </div>
                <div style={{ fontSize: '0.9rem', color: '#ffffff', marginBottom: '0.65rem', lineHeight: 1.45 }}>
                  {currentAttempt.diagnostic_fork_question}
                </div>

                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 700, marginBottom: '0.2rem' }}>
                  Student's Actual Selection (Option {currentAttempt.diagnostic_fork_selected_choice_id})
                </div>
                <div style={{ fontSize: '0.88rem', color: '#cbd5e1', fontStyle: 'italic', lineHeight: 1.45 }}>
                  "{currentAttempt.diagnostic_fork_selected_text}"
                </div>
              </div>

              {/* How response affected diagnosis */}
              <div style={{
                background: 'rgba(245, 158, 11, 0.08)',
                border: '1px solid rgba(245, 158, 11, 0.25)',
                padding: '0.75rem 0.9rem',
                borderRadius: 'var(--radius-sm)',
                fontSize: '0.84rem',
                color: '#fef3c7',
                lineHeight: 1.5,
              }}>
                <div style={{ fontWeight: 700, marginBottom: '0.2rem' }}>
                  🔍 Conceptual Impact on Diagnosis:
                </div>
                <div>
                  {currentAttempt.diagnostic_fork_explanation || currentAttempt.diagnostic_fork_interpretation}
                </div>
                <div style={{ marginTop: '0.4rem', fontSize: '0.78rem', color: '#fbbf24' }}>
                  Refined Diagnosis: <strong>{currentAttempt.misconception_label} ({currentAttempt.misconception_id})</strong> — Refined Confidence: {finalConf}%
                </div>
              </div>
            </div>
          ) : (
            <div style={{
              background: 'rgba(255, 255, 255, 0.02)',
              border: '1px dashed var(--border-subtle)',
              padding: '1rem',
              borderRadius: 'var(--radius-sm)',
              fontSize: '0.86rem',
              color: 'var(--text-secondary)',
              lineHeight: 1.5,
            }}>
              <p style={{ margin: 0 }}>
                {initialConf >= 60
                  ? `No diagnostic follow-up was needed for this attempt. The initial model confidence was sufficiently high (${initialConf}% >= 60%), providing an unambiguous baseline to proceed directly to the targeted intervention.`
                  : currentAttempt.diagnostic_fork_explanation || 'No specialized discriminator probe was requested for this concept category. The system proceeded with the primary pedagogical intervention.'}
              </p>
            </div>
          )}
        </div>

        {/* Visual Connector */}
        <div style={{ display: 'flex', justifyContent: 'center', margin: '-0.35rem 0' }}>
          <span style={{ color: 'var(--text-muted)', fontSize: '1.2rem' }}>↓</span>
        </div>

        {/* ========================================================
            STAGE C: TARGETED INTERVENTION
           ======================================================== */}
        <div
          className="card"
          style={{
            borderLeft: '4px solid var(--teal-500)',
            background: 'var(--bg-card)',
            position: 'relative',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <div style={{
                width: '26px',
                height: '26px',
                borderRadius: '50%',
                background: 'var(--teal-500)',
                color: '#070d1e',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '0.8rem',
                fontWeight: 800
              }}>
                C
              </div>
              <span style={{ fontSize: '0.84rem', fontWeight: 800, textTransform: 'uppercase', color: '#5eead4', letterSpacing: '0.05em' }}>
                Stage 3: Targeted Pedagogical Intervention
              </span>
            </div>
            <span className="badge badge-teal">Pedagogical Bridge</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <div>
              <h4 style={{ fontSize: '1.08rem', color: '#ffffff', marginBottom: '0.25rem' }}>
                {currentAttempt.intervention_title || 'Physics Conceptual Remediation'}
              </h4>
              <p style={{ fontSize: '0.88rem', color: '#cbd5e1', lineHeight: 1.55 }}>
                {currentAttempt.intervention_summary}
              </p>
            </div>

            {currentAttempt.intervention_analogy && (
              <div style={{
                background: 'rgba(20, 184, 166, 0.08)',
                border: '1px solid rgba(20, 184, 166, 0.25)',
                borderRadius: 'var(--radius-sm)',
                padding: '0.75rem 0.9rem',
                fontSize: '0.84rem',
                color: '#e2e8f0',
              }}>
                <span style={{ color: '#5eead4', fontWeight: 700 }}>Real-Life Analogy: </span>
                {currentAttempt.intervention_analogy}
              </div>
            )}
          </div>
        </div>

        {/* Visual Connector */}
        <div style={{ display: 'flex', justifyContent: 'center', margin: '-0.35rem 0' }}>
          <span style={{ color: 'var(--text-muted)', fontSize: '1.2rem' }}>↓</span>
        </div>

        {/* ========================================================
            STAGE D: TRANSFER REASSESSMENT
           ======================================================== */}
        <div
          className="card"
          style={{
            borderLeft: `4px solid ${currentAttempt.reassessment_completed ? '#38bdf8' : 'var(--text-muted)'}`,
            background: 'var(--bg-card)',
            position: 'relative',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <div style={{
                width: '26px',
                height: '26px',
                borderRadius: '50%',
                background: currentAttempt.reassessment_completed ? '#0284c7' : '#334155',
                color: '#ffffff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '0.8rem',
                fontWeight: 800
              }}>
                D
              </div>
              <span style={{ fontSize: '0.84rem', fontWeight: 800, textTransform: 'uppercase', color: '#7dd3fc', letterSpacing: '0.05em' }}>
                Stage 4: Transfer Scenario Reassessment
              </span>
            </div>

            {currentAttempt.reassessment_completed ? (
              <span className="badge badge-indigo">Transfer Evaluated</span>
            ) : (
              <span className="badge badge-amber">Reassessment Pending</span>
            )}
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
            {/* Transfer Scenario Question */}
            <div style={{ background: 'rgba(0, 0, 0, 0.25)', padding: '0.9rem', borderRadius: 'var(--radius-sm)' }}>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 700, marginBottom: '0.25rem' }}>
                Transfer Reassessment Scenario (Different Context)
              </div>
              <div style={{ fontSize: '0.9rem', color: '#f8fafc', lineHeight: 1.45 }}>
                {currentAttempt.reassessment_question || 'No reassessment question recorded.'}
              </div>
            </div>

            {/* Student's Actual Reassessment Answer */}
            <div style={{ background: 'rgba(0, 0, 0, 0.25)', padding: '0.9rem', borderRadius: 'var(--radius-sm)' }}>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 700, marginBottom: '0.25rem' }}>
                Student's Actual Reassessment Answer
              </div>
              <div style={{ fontSize: '0.9rem', color: '#e2e8f0', fontStyle: 'italic', lineHeight: 1.45 }}>
                {currentAttempt.reassessment_answer ? `"${currentAttempt.reassessment_answer}"` : 'Awaiting student response in Diagnostic Lab.'}
              </div>
            </div>
          </div>
        </div>

        {/* Visual Connector */}
        <div style={{ display: 'flex', justifyContent: 'center', margin: '-0.35rem 0' }}>
          <span style={{ color: 'var(--text-muted)', fontSize: '1.2rem' }}>↓</span>
        </div>

        {/* ========================================================
            STAGE E: OBSERVED OUTCOME
           ======================================================== */}
        <div
          className="card"
          style={{
            borderLeft: `4px solid ${
              isImproved ? 'var(--teal-500)' : isInconclusive ? 'var(--amber-500)' : isPersistent ? 'var(--red-500)' : 'var(--text-muted)'
            }`,
            background: isImproved
              ? 'rgba(20, 184, 166, 0.08)'
              : isInconclusive
              ? 'rgba(245, 158, 11, 0.08)'
              : isPersistent
              ? 'rgba(239, 68, 68, 0.08)'
              : 'var(--bg-card)',
            position: 'relative',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem', flexWrap: 'wrap', gap: '0.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <div style={{
                width: '26px',
                height: '26px',
                borderRadius: '50%',
                background: isImproved ? 'var(--teal-500)' : isInconclusive ? 'var(--amber-500)' : 'var(--red-500)',
                color: '#070d1e',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '0.8rem',
                fontWeight: 800
              }}>
                E
              </div>
              <span style={{ fontSize: '0.84rem', fontWeight: 800, textTransform: 'uppercase', color: '#ffffff', letterSpacing: '0.05em' }}>
                Stage 5: Observed Conceptual Outcome
              </span>
            </div>

            {/* Outcome Badge */}
            {currentAttempt.reassessment_completed ? (
              <span className={`badge ${
                isImproved ? 'badge-teal' : isInconclusive ? 'badge-amber' : 'badge-red'
              }`} style={{ fontSize: '0.82rem', padding: '0.3rem 0.75rem' }}>
                {isImproved
                  ? '🎉 Your New Answer Shows Improvement'
                  : isInconclusive
                  ? '⏸️ We Need More Evidence'
                  : '⚠️ This Misunderstanding May Still Be Present'}
              </span>
            ) : (
              <span className="badge badge-amber">Reassessment Pending</span>
            )}
          </div>

          {/* Outcome Explanation */}
          <div style={{ fontSize: '0.9rem', color: '#f8fafc', lineHeight: 1.55, marginBottom: '0.75rem' }}>
            {currentAttempt.reassessment_feedback || (
              currentAttempt.reassessment_completed
                ? 'Evaluation recorded without specific textual feedback.'
                : 'Complete the transfer reassessment in the Diagnostic Lab to observe the conceptual resolution outcome.'
            )}
          </div>

          {/* Transparent Pedagogical Rationale */}
          <div style={{
            background: 'rgba(0, 0, 0, 0.25)',
            border: '1px solid rgba(255, 255, 255, 0.06)',
            borderRadius: 'var(--radius-sm)',
            padding: '0.75rem 0.9rem',
            fontSize: '0.8rem',
            color: 'var(--text-secondary)',
            lineHeight: 1.5,
          }}>
            <strong>Pedagogical Standard: </strong>
            {isImproved && (
              <span>The student's explanation in the transfer scenario demonstrated correct physical principles without reverting to the diagnosed misconception. This confirms supported conceptual improvement for this attempt (does not imply permanent retention).</span>
            )}
            {isPersistent && (
              <span>The student's transfer response continued to exhibit characteristics of the identified misconception. Targeted follow-up with worked examples is advised.</span>
            )}
            {isInconclusive && (
              <span>The transfer reasoning was ambiguous, incomplete, or borderline. Rather than guessing, the system flags the evidence as inconclusive and recommends further dialogue.</span>
            )}
            {!currentAttempt.reassessment_completed && (
              <span>Outcome is determined only after an active transfer reassessment is submitted and analyzed.</span>
            )}
          </div>
        </div>

      </div>

      {/* Footer Navigation Button to Lab */}
      <div style={{ display: 'flex', justifyContent: 'center', marginTop: '0.5rem' }}>
        <button
          type="button"
          onClick={onStartLearning}
          className="btn btn-secondary"
          style={{ fontSize: '0.88rem' }}
        >
          🔬 Return to Diagnostic Lab
        </button>
      </div>
    </div>
  );
}
