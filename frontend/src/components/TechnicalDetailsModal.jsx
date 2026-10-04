import React, { useState } from 'react';
import TaxonomyExplorer from './TaxonomyExplorer';
import JudgeAuditView from './JudgeAuditView';

export default function TechnicalDetailsModal({ isOpen, onClose, healthData, taxonomy }) {
  const [subTab, setSubTab] = useState('audit');

  if (!isOpen) return null;

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(7, 13, 30, 0.85)',
        backdropFilter: 'blur(8px)',
        zIndex: 1000,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '1.5rem',
      }}
    >
      <div
        className="card"
        style={{
          maxWidth: '1000px',
          width: '100%',
          maxHeight: '90vh',
          display: 'flex',
          flexDirection: 'column',
          background: '#0d152d',
          border: '1px solid rgba(99, 102, 241, 0.4)',
          boxShadow: '0 20px 60px rgba(0, 0, 0, 0.7)',
          overflow: 'hidden',
          padding: 0,
        }}
      >
        {/* Modal Header */}
        <div
          style={{
            padding: '1.25rem 1.5rem',
            borderBottom: '1px solid var(--border-subtle)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            background: 'rgba(0, 0, 0, 0.25)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <span style={{ fontSize: '1.25rem' }}>⚙️</span>
            <div>
              <h3 style={{ fontSize: '1.15rem', color: '#ffffff', margin: 0 }}>
                Technical Details & Judge Audit
              </h3>
              <p style={{ fontSize: '0.76rem', color: 'var(--text-muted)', margin: 0 }}>
                Architecture specifications, taxonomy rules, and ML diagnostic pipeline metrics
              </p>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
            {/* Sub-tabs */}
            <div style={{ display: 'flex', gap: '0.35rem', background: 'rgba(255, 255, 255, 0.05)', padding: '0.2rem', borderRadius: 'var(--radius-md)' }}>
              <button
                type="button"
                onClick={() => setSubTab('audit')}
                className={`btn btn-sm ${subTab === 'audit' ? 'btn-primary' : 'btn-secondary'}`}
                style={{ fontSize: '0.78rem', padding: '0.3rem 0.75rem' }}
              >
                Model & API Audit
              </button>
              <button
                type="button"
                onClick={() => setSubTab('taxonomy')}
                className={`btn btn-sm ${subTab === 'taxonomy' ? 'btn-primary' : 'btn-secondary'}`}
                style={{ fontSize: '0.78rem', padding: '0.3rem 0.75rem' }}
              >
                Physics Taxonomy
              </button>
            </div>

            <button
              type="button"
              onClick={onClose}
              className="btn btn-secondary btn-sm"
              style={{ padding: '0.35rem 0.75rem', fontSize: '0.9rem', color: '#cbd5e1' }}
            >
              ✕ Close
            </button>
          </div>
        </div>

        {/* Modal Body */}
        <div style={{ padding: '1.5rem', overflowY: 'auto', flex: 1 }}>
          {subTab === 'audit' && (
            <JudgeAuditView healthData={healthData} />
          )}

          {subTab === 'taxonomy' && (
            <TaxonomyExplorer taxonomy={taxonomy} />
          )}
        </div>
      </div>
    </div>
  );
}
