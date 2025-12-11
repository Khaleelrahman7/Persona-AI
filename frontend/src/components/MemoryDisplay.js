import React from 'react';

const MemoryDisplay = ({ memory }) => {
  if (!memory) {
    return (
      <div className="memory-display">
        <h2>Extracted Memory</h2>
        <div className="empty-memory">
          <p>No memory extracted yet.</p>
          <p style={{ fontSize: '0.9rem', marginTop: '10px' }}>
            Send messages and click "Extract Memory" to see extracted information.
          </p>
        </div>
      </div>
    );
  }

  const hasContent = 
    (memory.preferences && memory.preferences.length > 0) ||
    (memory.emotional_patterns && memory.emotional_patterns.length > 0) ||
    (memory.facts && memory.facts.length > 0);

  if (!hasContent) {
    return (
      <div className="memory-display">
        <h2>Extracted Memory</h2>
        <div className="empty-memory">
          <p>No new memory items found in the recent messages.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="memory-display">
      <h2>Extracted Memory</h2>
      
      {memory.preferences && memory.preferences.length > 0 && (
        <div className="memory-section">
          <h3>🎯 Preferences</h3>
          {memory.preferences.map((pref, idx) => (
            <div key={idx} className="memory-item">
              <p><strong>{pref.preference || 'N/A'}</strong></p>
              {pref.confidence && (
                <p className="confidence">Confidence: {pref.confidence}</p>
              )}
              {pref.context && (
                <p style={{ fontSize: '0.9rem', fontStyle: 'italic', color: '#777' }}>
                  "{pref.context}"
                </p>
              )}
            </div>
          ))}
        </div>
      )}

      {memory.emotional_patterns && memory.emotional_patterns.length > 0 && (
        <div className="memory-section">
          <h3>😊 Emotional Patterns</h3>
          {memory.emotional_patterns.map((pattern, idx) => (
            <div key={idx} className="memory-item">
              <p><strong>{pattern.pattern || 'N/A'}</strong></p>
              {pattern.emotion && (
                <p>Emotion: {pattern.emotion}</p>
              )}
              {pattern.triggers && pattern.triggers.length > 0 && (
                <p>Triggers: {pattern.triggers.join(', ')}</p>
              )}
              {pattern.context && (
                <p style={{ fontSize: '0.9rem', fontStyle: 'italic', color: '#777' }}>
                  "{pattern.context}"
                </p>
              )}
            </div>
          ))}
        </div>
      )}

      {memory.facts && memory.facts.length > 0 && (
        <div className="memory-section">
          <h3>📝 Facts</h3>
          {memory.facts.map((fact, idx) => (
            <div key={idx} className="memory-item">
              <p><strong>{fact.fact || 'N/A'}</strong></p>
              {fact.category && (
                <p>Category: {fact.category}</p>
              )}
              {fact.importance && (
                <p className="confidence">Importance: {fact.importance}</p>
              )}
              {fact.context && (
                <p style={{ fontSize: '0.9rem', fontStyle: 'italic', color: '#777' }}>
                  "{fact.context}"
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MemoryDisplay;


