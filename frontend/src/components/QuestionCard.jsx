import React, { useState } from 'react';

export default function QuestionCard({
  questions,
  selectedQuestion,
  onSelectQuestion,
  studentAnswer,
  setStudentAnswer,
  onDiagnose,
  isDiagnosing,
}) {
  const [topicFilter, setTopicFilter] = useState('ALL');

  if (!questions || questions.length === 0) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '2.5rem' }}>
        <p style={{ color: 'var(--text-muted)' }}>Loading physics questions from knowledge base...</p>
      </div>
    );
  }

  // Extract unique topics for quick filter
  const topics = ['ALL', ...new Set(questions.map((q) => q.topic).filter(Boolean))];

  const filteredQuestions = topicFilter === 'ALL'
    ? questions
    : questions.filter((q) => q.topic === topicFilter);

  const activeQ = selectedQuestion || questions[0];

  const handleApplyPreset = (text) => {
    if (text) {
      setStudentAnswer(text);
    }
  };

  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.1rem' }}>
      {/* Top Header & Topic Filter */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.6rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span className="badge badge-indigo">Step 1: Scientific Reasoning</span>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
            ({questions.length} Scenarios Available)
          </span>
        </div>

        {/* Topic Filter Pills */}
        <div style={{ display: 'flex', gap: '0.35rem', flexWrap: 'wrap' }}>
          {topics.map((t) => (
            <button
              key={t}
              onClick={() => setTopicFilter(t)}
              className={`btn btn-sm ${topicFilter === t ? 'btn-primary' : 'btn-secondary'}`}
              style={{ fontSize: '0.72rem', padding: '0.2rem 0.6rem' }}
            >
              {t === 'ALL' ? 'All Topics' : t}
            </button>
          ))}
        </div>
      </div>

      {/* Question Dropdown */}
      <div>
        <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: '0.35rem' }}>
          Select Conceptual Physics Challenge:
        </label>
        <select
          value={activeQ.question_id}
          onChange={(e) => {
            const found = questions.find((q) => q.question_id === e.target.value);
            if (found) {
              onSelectQuestion(found);
              setStudentAnswer('');
            }
          }}
          style={{
            width: '100%',
            background: '#091024',
            border: '1px solid rgba(255, 255, 255, 0.12)',
            borderRadius: 'var(--radius-md)',
            padding: '0.65rem 0.9rem',
            color: '#ffffff',
            fontSize: '0.88rem',
            fontWeight: 500,
          }}
        >
          {filteredQuestions.map((q) => (
            <option key={q.question_id} value={q.question_id}>
              [{q.question_id}] {q.subtopic ? `${q.subtopic}: ` : ''}{q.question.substring(0, 75)}...
            </option>
          ))}
        </select>
      </div>

      {/* Highlighted Question Prompt Box */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(14, 23, 48, 0.95) 0%, rgba(9, 15, 33, 0.95) 100%)',
        border: '1px solid rgba(99, 102, 241, 0.35)',
        borderRadius: 'var(--radius-md)',
        padding: '1.25rem 1.4rem',
        boxShadow: '0 4px 20px rgba(0, 0, 0, 0.35)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem', flexWrap: 'wrap', gap: '0.4rem' }}>
          <span style={{ fontSize: '0.74rem', fontWeight: 700, color: '#818cf8', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
            {activeQ.topic} • {activeQ.subtopic || 'Conceptual Thought Experiment'}
          </span>
          <span className={`badge ${activeQ.difficulty === 'Easy' ? 'badge-teal' : 'badge-amber'}`}>
            {activeQ.difficulty || 'Intermediate'}
          </span>
        </div>

        <div style={{ fontSize: '1.18rem', fontWeight: 600, color: '#ffffff', lineHeight: 1.55 }}>
          {activeQ.question}
        </div>

        {activeQ.real_life_example && (
          <div style={{ marginTop: '0.6rem', fontSize: '0.8rem', color: '#94a3b8', fontStyle: 'italic' }}>
            Real-world context: {activeQ.real_life_example}
          </div>
        )}
      </div>

      {/* Quick Demo Test Presets for Judges */}
      <div style={{
        background: 'rgba(255, 255, 255, 0.02)',
        border: '1px dashed rgba(255, 255, 255, 0.1)',
        borderRadius: 'var(--radius-md)',
        padding: '0.75rem 0.9rem',
      }}>
        <div style={{ fontSize: '0.74rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '0.4rem' }}>
          💡 Instant Evaluator Presets (Click to autofill authentic sample student answers):
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={() => handleApplyPreset(activeQ.sample_misconception_answer || "The forward force from the stick stays inside the puck making it glide forward.")}
            style={{ fontSize: '0.75rem', justifyContent: 'flex-start', textAlign: 'left', whiteSpace: 'normal', height: 'auto', padding: '0.4rem 0.6rem' }}
          >
            <span>⚠️</span>
            <span style={{ color: '#fde68a' }}>Test Misconception Answer</span>
          </button>
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={() => handleApplyPreset(activeQ.sample_correct_answer || "No force is needed; by Newton's First Law it continues at constant velocity due to inertia.")}
            style={{ fontSize: '0.75rem', justifyContent: 'flex-start', textAlign: 'left', whiteSpace: 'normal', height: 'auto', padding: '0.4rem 0.6rem' }}
          >
            <span>✅</span>
            <span style={{ color: '#5eead4' }}>Test Canonical Answer</span>
          </button>
        </div>
      </div>

      {/* Free-text Student Answer */}
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.35rem' }}>
          <label style={{ fontSize: '0.84rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
            Your Scientific Explanation & Reasoning:
          </label>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            {studentAnswer.trim().length} characters
          </span>
        </div>
        <textarea
          value={studentAnswer}
          onChange={(e) => setStudentAnswer(e.target.value)}
          placeholder="Explain the physical cause and effect. What forces act, why does the object behave this way, and what law applies?"
          rows={4}
        />
        <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
          Tip: Explain <em>why</em> something happens rather than only guessing the final state.
        </div>
      </div>

      {/* Submit Action */}
      <button
        type="button"
        className="btn btn-primary"
        onClick={onDiagnose}
        disabled={isDiagnosing || !studentAnswer.trim()}
        style={{ padding: '0.8rem 1.4rem', fontSize: '0.96rem' }}
      >
        {isDiagnosing ? (
          <>
            <span className="spinner" /> Analyzing Reasoning against Misconception Models...
          </>
        ) : (
          <>⚡ Analyze My Explanation</>
        )}
      </button>
    </div>
  );
}
