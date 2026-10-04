import React from 'react';

export default function Header({
  activeTab,
  setActiveTab,
  learnerId,
  setLearnerId,
  isOnline,
  attemptCount,
  onOpenTechnical,
}) {
  return (
    <header style={{
      background: 'linear-gradient(180deg, #0e172e 0%, #0a1124 100%)',
      borderBottom: '1px solid var(--border-subtle)',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      backdropFilter: 'blur(12px)',
    }}>
      <div style={{
        maxWidth: '1280px',
        margin: '0 auto',
        padding: '0.9rem 1.5rem',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '1rem',
      }}>
        {/* Brand */}
        <div
          onClick={() => setActiveTab('learn')}
          style={{ display: 'flex', alignItems: 'center', gap: '0.85rem', cursor: 'pointer' }}
        >
          <div style={{
            width: '38px',
            height: '38px',
            borderRadius: '10px',
            background: 'linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '18px',
            boxShadow: '0 4px 12px rgba(79, 70, 229, 0.35)',
          }}>
            ⚛️
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
              <span style={{ fontSize: '1.25rem', fontWeight: 800, letterSpacing: '-0.02em', color: '#ffffff' }}>
                Re:Learn
              </span>
              <span className="badge badge-teal" style={{ fontSize: '0.68rem', padding: '0.15rem 0.5rem' }}>Physics Tutor</span>
            </div>
            <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>
              Conceptual Diagnosis & Guided Transfer
            </div>
          </div>
        </div>

        {/* 3 Primary Navigation Destinations */}
        <nav style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.35rem',
          background: 'rgba(7, 13, 30, 0.75)',
          padding: '0.3rem',
          borderRadius: 'var(--radius-lg)',
          border: '1px solid var(--border-subtle)',
        }}>
          {[
            { id: 'learn', label: '📖 Learn' },
            { id: 'progress', label: `📈 My Progress (${attemptCount})` },
            { id: 'how-it-works', label: '💡 How Re:Learn Works' },
          ].map((tab) => {
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  background: isActive ? 'linear-gradient(135deg, #3730a3 0%, #1e3a8a 100%)' : 'transparent',
                  color: isActive ? '#ffffff' : 'var(--text-secondary)',
                  border: isActive ? '1px solid rgba(99, 102, 241, 0.45)' : '1px solid transparent',
                  padding: '0.45rem 1rem',
                  borderRadius: 'var(--radius-md)',
                  fontSize: '0.86rem',
                  fontWeight: isActive ? 700 : 500,
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                  boxShadow: isActive ? '0 2px 8px rgba(0, 0, 0, 0.3)' : 'none',
                }}
              >
                {tab.label}
              </button>
            );
          })}
        </nav>

        {/* Learner Profile, Technical Details & Server Status */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
          {/* Technical Details / Judge Modal Trigger */}
          {onOpenTechnical && (
            <button
              type="button"
              onClick={onOpenTechnical}
              className="btn btn-secondary btn-sm"
              style={{
                fontSize: '0.78rem',
                fontWeight: 600,
                padding: '0.35rem 0.65rem',
                borderColor: 'rgba(255, 255, 255, 0.15)',
                color: '#cbd5e1',
              }}
              title="View model metrics, architecture, and physics taxonomy"
            >
              ⚙️ Technical Details
            </button>
          )}

          {/* Student Profile Input */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.4rem',
            background: 'rgba(255, 255, 255, 0.04)',
            border: '1px solid var(--border-subtle)',
            borderRadius: 'var(--radius-md)',
            padding: '0.35rem 0.65rem',
            fontSize: '0.78rem',
            color: 'var(--text-secondary)',
          }}>
            <span>👤</span>
            <input
              type="text"
              value={learnerId}
              onChange={(e) => setLearnerId(e.target.value.trim() || 'student_01')}
              title="Click to change student ID"
              style={{
                background: 'transparent',
                border: 'none',
                color: '#818cf8',
                fontWeight: 700,
                fontSize: '0.8rem',
                width: '80px',
                padding: 0,
                boxShadow: 'none',
              }}
            />
          </div>

          <div
            title={isOnline ? 'FastAPI Diagnostic Backend Online' : 'Connecting to API...'}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.35rem',
              fontSize: '0.74rem',
              fontWeight: 600,
              color: isOnline ? '#34d399' : '#f87171',
              background: isOnline ? 'rgba(52, 211, 153, 0.1)' : 'rgba(248, 113, 113, 0.1)',
              border: `1px solid ${isOnline ? 'rgba(52, 211, 153, 0.3)' : 'rgba(248, 113, 113, 0.3)'}`,
              borderRadius: 'var(--radius-full)',
              padding: '0.25rem 0.6rem',
            }}
          >
            <span style={{
              width: '7px',
              height: '7px',
              borderRadius: '50%',
              background: isOnline ? '#10b981' : '#ef4444',
              display: 'inline-block',
              boxShadow: isOnline ? '0 0 8px #10b981' : 'none',
            }} />
            {isOnline ? 'API Active' : 'Offline'}
          </div>
        </div>
      </div>
    </header>
  );
}
