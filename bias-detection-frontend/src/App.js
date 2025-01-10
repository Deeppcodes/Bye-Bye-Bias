import React, { useState } from 'react';
import './App.css';

function App() {
  const [inputValue, setInputValue] = useState('');
  const [outputValue, setOutputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [suggestions, setSuggestions] = useState([]);

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
    // Clear previous results when input changes
    setError('');
    setOutputValue('');
    setSuggestions([]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setSuggestions([]);
    setOutputValue('');

    try {
      const response = await fetch('http://localhost:5001/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputValue }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to analyze text');
      }

      if (data.error) {
        setError(data.error);
      } else {
        setSuggestions(data.suggestions);
        setOutputValue(data.improved_text);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Welcome to Bye-Bye Bias</h1>
      <h2>Fostering Inclusive Communication and Detecting Bias in Writing</h2>
      
      <div className="container">
        <div className="input-block">
          <h3>Enter Text</h3>
          <form onSubmit={handleSubmit}>
            <textarea
              value={inputValue}
              onChange={handleInputChange}
              placeholder="Type or paste your text here..."
              disabled={isLoading}
            ></textarea>
            <button type="submit" disabled={isLoading || !inputValue.trim()}>
              {isLoading ? 'Analyzing...' : 'Analyze Text'}
            </button>
          </form>
        </div>
        
        <div className="output-block">
          <h3>Analysis Results</h3>
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
          
          {suggestions.length > 0 && (
            <div className="suggestions">
              <h4>Suggestions for Improvement:</h4>
              <ul>
                {suggestions.map((suggestion, index) => (
                  <li key={index}>{suggestion}</li>
                ))}
              </ul>
            </div>
          )}
          
          {outputValue && (
            <div className="improved-text">
              <h4>Improved Version:</h4>
              <textarea
                value={outputValue}
                readOnly
                placeholder="Improved text will appear here..."
              ></textarea>
            </div>
          )}
        </div>
      </div>

      <footer className="footer">
        <p>This tool helps identify and rephrase potentially biased language to promote inclusive communication.</p>
      </footer>
    </div>
  );
}

export default App;