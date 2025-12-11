import React, { useState } from 'react';
import './App.css';
import ChatInterface from './components/ChatInterface';
import MemoryDisplay from './components/MemoryDisplay';
import PersonalitySelector from './components/PersonalitySelector';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [messages, setMessages] = useState([]);
  const [selectedPersonality, setSelectedPersonality] = useState('calm_mentor');
  const [extractedMemory, setExtractedMemory] = useState(null);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async (messageText) => {
    const newMessage = {
      role: 'user',
      content: messageText
    };
    
    const updatedMessages = [...messages, newMessage];
    setMessages(updatedMessages);
    setLoading(true);

    try {
      // Convert messages to API format
      const apiMessages = updatedMessages.map(msg => ({
        role: msg.role,
        content: msg.content
      }));

      // Call the chat endpoint
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: apiMessages,
          personality: selectedPersonality,
          user_id: 'default_user'
        }),
      });

      const data = await response.json();
      
      setExtractedMemory(data.extracted_memory);
      setResponse({
        personality: data.personality,
        response: data.response,
        before_response: data.before_response,
        after_response: data.after_response
      });

      // Add AI response to messages
      setMessages([...updatedMessages, {
        role: 'assistant',
        content: data.response
      }]);
    } catch (error) {
      console.error('Error:', error);
      alert('Error sending message. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleExtractMemory = async () => {
    if (messages.length === 0) {
      alert('Please add some messages first');
      return;
    }

    setLoading(true);
    try {
      const apiMessages = messages.map(msg => ({
        role: msg.role,
        content: msg.content
      }));

      const response = await fetch(`${API_BASE_URL}/api/extract-memory`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: apiMessages,
          user_id: 'default_user'
        }),
      });

      const data = await response.json();
      setExtractedMemory(data.extracted_memory);
    } catch (error) {
      console.error('Error:', error);
      alert('Error extracting memory. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    setExtractedMemory(null);
    setResponse(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🧠 Persona AI</h1>
        <p>Memory Extraction & Personality Engine</p>
      </header>

      <div className="container">
        <div className="left-panel">
          <PersonalitySelector
            selectedPersonality={selectedPersonality}
            onSelect={setSelectedPersonality}
          />
          
          <ChatInterface
            messages={messages}
            onSendMessage={handleSendMessage}
            onExtractMemory={handleExtractMemory}
            onClearChat={handleClearChat}
            loading={loading}
          />
        </div>

        <div className="right-panel">
          <MemoryDisplay memory={extractedMemory} />
          
          {response && (
            <div className="response-comparison">
              <h2>Personality Transformation</h2>
              <div className="comparison-container">
                <div className="response-box before">
                  <h3>Before (Default)</h3>
                  <p>{response.before_response}</p>
                </div>
                <div className="response-box after">
                  <h3>After ({response.personality.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())})</h3>
                  <p>{response.after_response}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;


