import React, { useState, useEffect } from 'react';
import { fetchDiagnosticForkQuestions, evaluateDiagnosticFork } from '../api';
import DiagnosticForkCard from './DiagnosticForkCard';

export default function DiagnosticForkExplorer({
  activeForkData,
  onEvaluateActiveFork,
  isEvaluatingActiveFork,
  evaluationResult,
  onContinueToIntervention,
  learnerId = 'student_01',
}) {
  const [forkQuestions, setForkQuestions] = useState([]);
  const [selectedForkId, setSelectedForkId] = useState('');
  const [standaloneResult, setStandaloneResult] = useState(null);
  const [isEvaluatingStandalone, setIsEvaluatingStandalone] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function loadForks() {
      setIsLoading(true);
      try {
        const questions = await fetchDiagnosticForkQuestions();
        setForkQuestions(questions);
        if (questions.length > 0 && !selectedForkId) {
          setSelectedForkId(questions[0].question_id);
        }
      } catch (err) {
        console.error('Failed to load diagnostic fork bank:', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadForks();
  }, []);

  const selectedQuestion = forkQuestions.find((q) => q.question_id === selectedForkId);

  const handleEvaluateStandalone = async (questionId, choiceId, reasoning) => {
    setIsEvaluatingStandalone(true);
    try {
      const res = await evaluateDiagnosticFork(learnerId, -1, questionId, choiceId, reasoning);
      setStandaloneResult(res);
    } catch (err) {
      console.error('Error evaluating probe:', err);
    } finally {
      setIsEvaluatingStandalone(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', maxWidth: '1080px', margin: '0 auto' }}>
      {/* Title & Explanatory Banner */}
      <div
        className="card"
        style={{
          background: 'linear-gradient(135deg, rgba(14, 23, 46, 0.95) 0%, rgba(245, 158, 11, 0.08) 100%)',
          border: '1px solid rgba(245, 158, 11, 0.3)',
          padding: '1.5rem',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.35rem' }}>
          <span className="badge badge-amber">SIGNATURE FEATURE</span>
          <span style={{ fontSize: '0.76rem', color: 'var(--text-muted)' }}>
            EVIDENCE-BASED DISCRIMINATOR PROBES
          </span>
        </div>
        <h2 style={{ fontSize: '1.5rem', color: '#ffffff', letterSpacing: '-0.02em', margin: 0 }}>
          Diagnostic Fork — Investigate My Thinking
        </h2>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginTop: '0.35rem', maxWidth: '780px', lineHeight: 1.55 }}>
          When initial student explanations contain ambiguous phrases that could stem from multiple competing misconceptions, Re:Learn does not guess. Instead, it deploys a <strong>targeted diagnostic discriminator</strong> — an experimental scenario designed so that each choice provides direct physical evidence isolating the student's true mental model.
        </p>
      </div>

      {/* Active Session Fork (if currently triggered from Lab) */}
      {activeForkData && activeForkData.eligible && (
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.65rem' }}>
            <span style={{ fontSize: '0.82rem', fontWeight: 800, color: '#fbbf24', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              ⚡ Active Probe From Your Current Lab Challenge
            </span>
          </div>
          <DiagnosticForkCard
            forkData={activeForkData}
            onEvaluate={onEvaluateActiveFork}
            isEvaluating={isEvaluatingActiveFork}
            evaluationResult={evaluationResult}
            onContinue={onContinueToIntervention}
            onSkip={() => onContinueToIntervention()}
          />
        </div>
      )}

      {/* Interactive Diagnostic Fork Discriminator Bank */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
          <div>
            <h3 style={{ fontSize: '1.15rem', color: '#ffffff', margin: 0 }}>
              Curated Diagnostic Discriminator Scenarios
            </h3>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', margin: '0.2rem 0 0 0' }}>
              Explore how targeted physics probes distinguish between easily conflated misconception pairs.
            </p>
          </div>

          {forkQuestions.length > 0 && (
            <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
              {forkQuestions.map((fq) => {
                const isSelected = selectedForkId === fq.question_id;
                return (
                  <button
                    key={fq.question_id}
                    onClick={() => {
                      setSelectedForkId(fq.question_id);
                      setStandaloneResult(null);
                    }}
                    style={{
                      background: isSelected ? 'linear-gradient(135deg, #d97706 0%, #b45309 100%)' : 'rgba(255, 255, 255, 0.05)',
                      color: isSelected ? '#ffffff' : 'var(--text-secondary)',
                      border: isSelected ? '1px solid #fbbf24' : '1px solid var(--border-subtle)',
                      padding: '0.4rem 0.75rem',
                      borderRadius: 'var(--radius-md)',
                      fontSize: '0.8rem',
                      fontWeight: isSelected ? 700 : 500,
                      cursor: 'pointer',
                      transition: 'all 0.15s ease',
                    }}
                  >
                    {fq.question_id} ({fq.candidate_misconceptions.join(' vs ')})
                  </button>
                );
              })}
            </div>
          )}
        </div>

        {selectedQuestion && (
          <div style={{ borderTop: '1px solid var(--border-subtle)', paddingTop: '1.25rem' }}>
            <DiagnosticForkCard
              forkData={{
                question: selectedQuestion,
                candidate_ids: selectedQuestion.candidate_misconceptions,
                candidate_labels: selectedQuestion.candidate_labels,
                reason: `Targeted discriminator for distinguishing ${selectedQuestion.candidate_misconceptions.join(' vs ')}.`,
              }}
              onEvaluate={(qId, cId, rText) => handleEvaluateStandalone(qId, cId, rText)}
              isEvaluating={isEvaluatingStandalone}
              evaluationResult={standaloneResult}
              onContinue={() => setStandaloneResult(null)}
              onSkip={() => setStandaloneResult(null)}
            />
          </div>
        )}
      </div>
    </div>
  );
}
