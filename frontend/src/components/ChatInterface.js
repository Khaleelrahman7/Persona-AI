import React, { useState, useRef, useEffect } from 'react';

const ChatInterface = ({ messages, onSendMessage, onExtractMemory, onClearChat, loading }) => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !loading) {
      onSendMessage(input);
      setInput('');
    }
  };

  return (
    <div className="chat-interface">
      <h2>Chat Messages ({messages.length}/30)</h2>
      
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="empty-memory">
            <p>Start a conversation! Add up to 30 messages.</p>
            <p style={{ fontSize: '0.9rem', marginTop: '10px', color: '#999' }}>
              The AI will extract your preferences, emotional patterns, and facts.
            </p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="message-role">{msg.role.toUpperCase()}</div>
              <div>{msg.content}</div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="chat-input-area">
        <input
          type="text"
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={loading || messages.length >= 30}
        />
        <button type="submit" className="btn btn-primary" disabled={loading || messages.length >= 30}>
          Send
        </button>
      </form>

      <div className="chat-buttons">
        <button 
          onClick={onExtractMemory} 
          className="btn btn-secondary"
          disabled={loading || messages.length === 0}
        >
          Extract Memory
        </button>
        <button 
          onClick={onClearChat} 
          className="btn btn-secondary"
          disabled={loading}
        >
          Clear Chat
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;


