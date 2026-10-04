import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import QuestionCard from './components/QuestionCard';
import DiagnosisCard from './components/DiagnosisCard';
import DiagnosticForkCard from './components/DiagnosticForkCard';
import InterventionCard from './components/InterventionCard';
import ReassessmentCard from './components/ReassessmentCard';
import MisconceptionXRay from './components/MisconceptionXRay';
import LearnerHistory from './components/LearnerHistory';
import HowItWorks from './components/HowItWorks';
import TechnicalDetailsModal from './components/TechnicalDetailsModal';

import {
  fetchHealth,
  fetchQuestions,
  fetchTaxonomy,
  runDiagnosis,
  submitReassessment,
  fetchLearnerHistory,
  resetLearnerHistory,
  evaluateDiagnosticFork,
} from './api';

export default function App() {
  // Navigation: 'learn', 'progress', 'how-it-works', 'xray'
  const [activeTab, setActiveTab] = useState('learn');
  const [isTechnicalModalOpen, setIsTechnicalModalOpen] = useState(false);

  // Learner Session
  const [learnerId, setLearnerId] = useState('student_01');
  const [isOnline, setIsOnline] = useState(false);
  const [healthData, setHealthData] = useState(null);

  // Core Data
  const [questions, setQuestions] = useState([]);
  const [taxonomy, setTaxonomy] = useState([]);
  const [history, setHistory] = useState([]);

  // Learning Stepper State: 'question' | 'diagnosis' | 'intervention' | 'reassessment' | 'result'
  const [journeyStep, setJourneyStep] = useState('question');

  // Active Challenge State
  const [selectedQuestion, setSelectedQuestion] = useState(null);
  const [studentAnswer, setStudentAnswer] = useState('');
  const [diagnosis, setDiagnosis] = useState(null);
  const [intervention, setIntervention] = useState(null);
  const [reassessmentResult, setReassessmentResult] = useState(null);
  const [lastAttemptIndex, setLastAttemptIndex] = useState(0);

  // Diagnostic Fork & X-Ray State
  const [diagnosticFork, setDiagnosticFork] = useState(null);
  const [isEvaluatingFork, setIsEvaluatingFork] = useState(false);
  const [forkEvaluationResult, setForkEvaluationResult] = useState(null);
  const [forkCompleted, setForkCompleted] = useState(false);
  const [selectedXRayIndex, setSelectedXRayIndex] = useState(null);

  // Loading & Error States
  const [isLoading, setIsLoading] = useState(true);
  const [isDiagnosing, setIsDiagnosing] = useState(false);
  const [isReassessing, setIsReassessing] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // Initial Data Load
  useEffect(() => {
    async function loadInitialData() {
      setIsLoading(true);
      try {
        const [health, qList, tax, hist] = await Promise.all([
          fetchHealth().catch(() => ({ status: 'offline' })),
          fetchQuestions().catch(() => []),
          fetchTaxonomy().catch(() => []),
          fetchLearnerHistory(learnerId).catch(() => []),
        ]);

        setHealthData(health);
        setIsOnline(health.status === 'online');
        setQuestions(qList);
        if (qList.length > 0) {
          setSelectedQuestion(qList[0]);
        }
        setTaxonomy(tax);
        setHistory(hist);
      } catch (err) {
        setErrorMessage('Failed to connect to Re:Learn diagnostic service. Is the backend running?');
      } finally {
        setIsLoading(false);
      }
    }

    loadInitialData();
  }, [learnerId]);

  // Handle Initial Diagnosis Submission
  const handleDiagnose = async () => {
    if (!selectedQuestion || !studentAnswer.trim()) return;

    setIsDiagnosing(true);
    setErrorMessage('');
    setReassessmentResult(null);
    setForkEvaluationResult(null);
    setForkCompleted(false);

    try {
      const res = await runDiagnosis(
        selectedQuestion.question,
        studentAnswer.trim(),
        learnerId
      );

      setDiagnosis(res.diagnosis);
      setIntervention(res.intervention);
      setDiagnosticFork(res.diagnostic_fork || null);

      if (res.attempt && typeof res.attempt.attempt_index === 'number') {
        setLastAttemptIndex(res.attempt.attempt_index);
        setSelectedXRayIndex(res.attempt.attempt_index);
      }

      // Advance stepper to diagnosis
      setJourneyStep('diagnosis');

      // Refresh history
      const updatedHistory = await fetchLearnerHistory(learnerId);
      setHistory(updatedHistory);
    } catch (err) {
      setErrorMessage(err.message || 'Diagnostic service error');
    } finally {
      setIsDiagnosing(false);
    }
  };

  // Handle Diagnostic Fork Choice Evaluation
  const handleEvaluateFork = async (questionId, selectedChoiceId, reasoningText) => {
    setIsEvaluatingFork(true);
    setErrorMessage('');

    try {
      const res = await evaluateDiagnosticFork(
        learnerId,
        lastAttemptIndex,
        questionId,
        selectedChoiceId,
        reasoningText
      );

      setForkEvaluationResult(res);
      if (res.refined_diagnosis) {
        setDiagnosis(res.refined_diagnosis);
      }
      if (res.intervention) {
        setIntervention(res.intervention);
      }

      // Refresh history
      const updatedHistory = await fetchLearnerHistory(learnerId);
      setHistory(updatedHistory);
    } catch (err) {
      setErrorMessage(err.message || 'Diagnostic fork evaluation error');
    } finally {
      setIsEvaluatingFork(false);
    }
  };

  // Handle Transfer Reassessment Submission
  const handleReassess = async (reassessQuestion, reassessAnswer, origMisconception) => {
    setIsReassessing(true);
    setErrorMessage('');

    try {
      const res = await submitReassessment(
        learnerId,
        lastAttemptIndex,
        reassessQuestion,
        reassessAnswer,
        origMisconception
      );

      setReassessmentResult(res);
      setJourneyStep('result');

      // Refresh history to verify update
      const updatedHistory = await fetchLearnerHistory(learnerId);
      setHistory(updatedHistory);
    } catch (err) {
      setErrorMessage(err.message || 'Reassessment verification error');
    } finally {
      setIsReassessing(false);
    }
  };

  // Reset Attempt / Select Another Question
  const handleResetForNewQuestion = (q) => {
    if (q) setSelectedQuestion(q);
    setStudentAnswer('');
    setDiagnosis(null);
    setIntervention(null);
    setReassessmentResult(null);
    setDiagnosticFork(null);
    setForkEvaluationResult(null);
    setForkCompleted(false);
    setJourneyStep('question');
  };

  // Clear Session History
  const handleResetHistory = async () => {
    try {
      await resetLearnerHistory(learnerId);
      setHistory([]);
      handleResetForNewQuestion();
    } catch (err) {
      setErrorMessage('Failed to reset learner history');
    }
  };

  // Stepper step definitions
  const steps = [
    { id: 'question', label: '1. Question' },
    { id: 'diagnosis', label: '2. Diagnosis' },
    { id: 'intervention', label: '3. Learn' },
    { id: 'reassessment', label: '4. Recheck' },
    { id: 'result', label: '5. Result' },
  ];

  const stepOrder = ['question', 'diagnosis', 'intervention', 'reassessment', 'result'];
  const currentStepIdx = stepOrder.indexOf(journeyStep);

  return (
    <div className="app-container">
      {/* Primary Header */}
      <Header
        activeTab={activeTab}
        setActiveTab={(tab) => {
          setActiveTab(tab);
          if (tab === 'learn' && journeyStep === 'result') {
            // Keep on current result or allow user to browse
          }
        }}
        learnerId={learnerId}
        setLearnerId={setLearnerId}
        isOnline={isOnline}
        attemptCount={history.length}
        onOpenTechnical={() => setIsTechnicalModalOpen(true)}
      />

      <main className="main-content">
        {/* Error Notification Banner */}
        {errorMessage && (
          <div style={{
            background: 'var(--red-bg)',
            border: '1px solid var(--red-border)',
            borderRadius: 'var(--radius-md)',
            padding: '0.85rem 1.25rem',
            marginBottom: '1rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            color: '#fca5a5',
            fontSize: '0.88rem',
          }}>
            <span>⚠️ {errorMessage}</span>
            <button
              onClick={() => setErrorMessage('')}
              style={{ background: 'transparent', border: 'none', color: '#fca5a5', cursor: 'pointer', fontWeight: 700 }}
            >
              ✕
            </button>
          </div>
        )}

        {/* ========================================================
            PRIMARY DESTINATION 1: LEARN (STEP-BY-STEP JOURNEY)
           ======================================================== */}
        {activeTab === 'learn' && (
          <div style={{ maxWidth: '820px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            {/* Minimal Sub-Header */}
            <div style={{ textAlign: 'center', padding: '0.5rem 0' }}>
              <h2 style={{ fontSize: '1.45rem', color: '#ffffff', letterSpacing: '-0.02em', marginBottom: '0.3rem' }}>
                Newtonian Mechanics Learning Lab
              </h2>
              <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', maxWidth: '580px', margin: '0 auto', lineHeight: 1.5 }}>
                Explain physical scenarios in your own words. We diagnose underlying misconceptions, clarify ambiguities with Diagnostic Forks, and verify true transfer.
              </p>
            </div>

            {/* Progress Stepper Bar */}
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                background: 'rgba(7, 13, 30, 0.75)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-lg)',
                padding: '0.65rem 1.25rem',
                flexWrap: 'wrap',
                gap: '0.5rem',
              }}
            >
              {steps.map((st, i) => {
                const isCurrent = journeyStep === st.id;
                const isPast = currentStepIdx > i;
                const isClickable = isPast || isCurrent;

                return (
                  <div key={st.id} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <button
                      type="button"
                      disabled={!isClickable}
                      onClick={() => isClickable && setJourneyStep(st.id)}
                      style={{
                        background: isCurrent
                          ? 'linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%)'
                          : isPast
                          ? 'rgba(20, 184, 166, 0.15)'
                          : 'transparent',
                        color: isCurrent
                          ? '#ffffff'
                          : isPast
                          ? '#5eead4'
                          : 'var(--text-muted)',
                        border: isCurrent
                          ? '1px solid rgba(99, 102, 241, 0.5)'
                          : isPast
                          ? '1px solid rgba(20, 184, 166, 0.3)'
                          : '1px solid transparent',
                        borderRadius: 'var(--radius-md)',
                        padding: '0.35rem 0.75rem',
                        fontSize: '0.82rem',
                        fontWeight: isCurrent || isPast ? 700 : 500,
                        cursor: isClickable ? 'pointer' : 'default',
                        transition: 'all 0.15s ease',
                      }}
                    >
                      {isPast ? `✓ ${st.label}` : st.label}
                    </button>
                    {i < steps.length - 1 && (
                      <span style={{ color: 'rgba(255, 255, 255, 0.15)', fontSize: '0.75rem' }}>➔</span>
                    )}
                  </div>
                );
              })}
            </div>

            {/* STEP 1: QUESTION INPUT */}
            {journeyStep === 'question' && (
              <QuestionCard
                questions={questions}
                selectedQuestion={selectedQuestion}
                onSelectQuestion={(q) => handleResetForNewQuestion(q)}
                studentAnswer={studentAnswer}
                setStudentAnswer={setStudentAnswer}
                onDiagnose={handleDiagnose}
                isDiagnosing={isDiagnosing}
              />
            )}

            {/* STEP 2: DIAGNOSIS & DIAGNOSTIC FORK */}
            {journeyStep === 'diagnosis' && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                {/* If Diagnostic Fork is eligible and not yet completed */}
                {diagnosticFork?.eligible && !forkCompleted ? (
                  <>
                    <DiagnosisCard
                      diagnosis={diagnosis}
                      studentAnswer={studentAnswer}
                      answerEvaluation={diagnosis?.answer_evaluation}
                    />

                    <DiagnosticForkCard
                      forkData={diagnosticFork}
                      onEvaluate={handleEvaluateFork}
                      isEvaluating={isEvaluatingFork}
                      evaluationResult={forkEvaluationResult}
                      onContinue={() => {
                        setForkCompleted(true);
                        setJourneyStep('intervention');
                      }}
                      onSkip={() => {
                        setForkCompleted(true);
                        setJourneyStep('intervention');
                      }}
                    />
                  </>
                ) : (
                  /* Standard Diagnosis card with continue action */
                  <DiagnosisCard
                    diagnosis={diagnosis}
                    studentAnswer={studentAnswer}
                    answerEvaluation={diagnosis?.answer_evaluation}
                    onContinue={() => setJourneyStep('intervention')}
                  />
                )}
              </div>
            )}

            {/* STEP 3: TARGETED LESSON (INTERVENTION) */}
            {journeyStep === 'intervention' && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                {intervention ? (
                  <InterventionCard
                    intervention={intervention}
                    onContinue={() => setJourneyStep('reassessment')}
                  />
                ) : (
                  <div className="card" style={{ textAlign: 'center', padding: '2rem' }}>
                    <p style={{ color: 'var(--text-muted)' }}>No targeted intervention required. Your reasoning aligns with canonical principles!</p>
                    <button
                      type="button"
                      onClick={() => setJourneyStep('reassessment')}
                      className="btn btn-teal"
                      style={{ marginTop: '1rem' }}
                    >
                      Try a New Question ➔
                    </button>
                  </div>
                )}
              </div>
            )}

            {/* STEP 4: RECHECK (TRANSFER REASSESSMENT) */}
            {journeyStep === 'reassessment' && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                <ReassessmentCard
                  reassessmentQuestion={intervention?.reassessment_question}
                  originalMisconception={diagnosis?.misconception_label}
                  onReassess={handleReassess}
                  isReassessing={isReassessing}
                  reassessmentResult={reassessmentResult}
                  onTryAnother={() => handleResetForNewQuestion()}
                />
              </div>
            )}

            {/* STEP 5: RESULT & MISCONCEPTION X-RAY ACCESS */}
            {journeyStep === 'result' && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                <ReassessmentCard
                  reassessmentQuestion={intervention?.reassessment_question}
                  originalMisconception={diagnosis?.misconception_label}
                  onReassess={handleReassess}
                  isReassessing={isReassessing}
                  reassessmentResult={reassessmentResult}
                  onViewXRay={() => {
                    setSelectedXRayIndex(lastAttemptIndex);
                    setActiveTab('xray');
                  }}
                  onTryAnother={() => handleResetForNewQuestion()}
                />
              </div>
            )}
          </div>
        )}

        {/* ========================================================
            PRIMARY DESTINATION 2: MY PROGRESS
           ======================================================== */}
        {activeTab === 'progress' && (
          <LearnerHistory
            history={history}
            onResetHistory={handleResetHistory}
            learnerId={learnerId}
            onViewXRay={(idx) => {
              setSelectedXRayIndex(idx);
              setActiveTab('xray');
            }}
            onStartLearning={() => {
              setActiveTab('learn');
              setJourneyStep('question');
            }}
          />
        )}

        {/* ========================================================
            PRIMARY DESTINATION 3: HOW RE:LEARN WORKS
           ======================================================== */}
        {activeTab === 'how-it-works' && (
          <HowItWorks
            onStartLearning={() => {
              setActiveTab('learn');
              setJourneyStep('question');
            }}
          />
        )}

        {/* ========================================================
            DEDICATED MISCONCEPTION X-RAY VIEW (ACCESSIBLE FROM PROGRESS & RESULT)
           ======================================================== */}
        {activeTab === 'xray' && (
          <div>
            <div style={{ maxWidth: '1080px', margin: '0 auto 1rem auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <button
                type="button"
                onClick={() => setActiveTab('progress')}
                className="btn btn-secondary btn-sm"
                style={{ fontSize: '0.84rem' }}
              >
                ← Back to My Progress
              </button>

              <button
                type="button"
                onClick={() => {
                  setActiveTab('learn');
                  handleResetForNewQuestion();
                }}
                className="btn btn-teal btn-sm"
                style={{ fontSize: '0.84rem', fontWeight: 700 }}
              >
                🚀 Start New Challenge
              </button>
            </div>

            <MisconceptionXRay
              history={history}
              activeAttemptIndex={selectedXRayIndex}
              onSelectAttempt={(idx) => setSelectedXRayIndex(idx)}
              onStartLearning={() => {
                setActiveTab('learn');
                handleResetForNewQuestion();
              }}
            />
          </div>
        )}
      </main>

      {/* SECONDARY TECHNICAL DETAILS & JUDGE AUDIT MODAL */}
      <TechnicalDetailsModal
        isOpen={isTechnicalModalOpen}
        onClose={() => setIsTechnicalModalOpen(false)}
        healthData={healthData}
        taxonomy={taxonomy}
      />
    </div>
  );
}
