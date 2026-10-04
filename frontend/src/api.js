/**
 * Re:Learn API Client
 * Connects frontend React components to the FastAPI Python backend.
 */

const API_BASE = '/api';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Failed to fetch backend health status');
  return res.json();
}

export async function fetchQuestions() {
  const res = await fetch(`${API_BASE}/questions`);
  if (!res.ok) throw new Error('Failed to load conceptual physics questions');
  return res.json();
}

export async function fetchTaxonomy() {
  const res = await fetch(`${API_BASE}/taxonomy`);
  if (!res.ok) throw new Error('Failed to load misconception taxonomy');
  return res.json();
}

export async function runDiagnosis(question, studentAnswer, learnerId = 'student_01') {
  const res = await fetch(`${API_BASE}/diagnose`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      question,
      student_answer: studentAnswer,
      learner_id: learnerId,
    }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Diagnostic service error occurred');
  }
  return res.json();
}

export async function submitReassessment(
  learnerId,
  attemptIndex,
  reassessmentQuestion,
  reassessmentAnswer,
  originalMisconception
) {
  const res = await fetch(`${API_BASE}/reassess`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      learner_id: learnerId,
      attempt_index: attemptIndex,
      reassessment_question: reassessmentQuestion,
      reassessment_answer: reassessmentAnswer,
      original_misconception: originalMisconception,
    }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Reassessment verification error');
  }
  return res.json();
}

export async function fetchLearnerHistory(learnerId = 'student_01') {
  const res = await fetch(`${API_BASE}/history/${learnerId}`);
  if (!res.ok) throw new Error('Failed to load learner progress history');
  return res.json();
}

export async function resetLearnerHistory(learnerId = 'student_01') {
  const res = await fetch(`${API_BASE}/history/${learnerId}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to reset history');
  return res.json();
}

export async function fetchDiagnosticForkQuestions() {
  const res = await fetch(`${API_BASE}/diagnostic-fork/questions`);
  if (!res.ok) throw new Error('Failed to load diagnostic fork questions');
  return res.json();
}

export async function evaluateDiagnosticFork(
  learnerId,
  attemptIndex,
  questionId,
  selectedChoiceId,
  reasoningText = ''
) {
  const res = await fetch(`${API_BASE}/diagnostic-fork/evaluate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      learner_id: learnerId,
      attempt_index: attemptIndex,
      question_id: questionId,
      selected_choice_id: selectedChoiceId,
      reasoning_text: reasoningText,
    }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Diagnostic fork evaluation error');
  }
  return res.json();
}

export async function fetchLearnerAttempt(learnerId = 'student_01', attemptIndex = -1) {
  const res = await fetch(`${API_BASE}/attempts/${learnerId}/${attemptIndex}`);
  if (!res.ok) throw new Error('Failed to load specific learner attempt');
  return res.json();
}
