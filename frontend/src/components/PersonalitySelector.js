import React from 'react';

const personalities = [
  {
    id: 'calm_mentor',
    name: 'Calm Mentor',
    description: 'Patient, wise, and supportive guide'
  },
  {
    id: 'witty_friend',
    name: 'Witty Friend',
    description: 'Fun, humorous, and engaging companion'
  },
  {
    id: 'therapist',
    name: 'Therapist',
    description: 'Professional, empathetic listener'
  }
];

const PersonalitySelector = ({ selectedPersonality, onSelect }) => {
  return (
    <div className="personality-selector">
      <h2>Select Personality</h2>
      <div className="personality-options">
        {personalities.map((personality) => (
          <div
            key={personality.id}
            className={`personality-option ${
              selectedPersonality === personality.id ? 'selected' : ''
            }`}
            onClick={() => onSelect(personality.id)}
          >
            <h3>{personality.name}</h3>
            <p>{personality.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PersonalitySelector;


