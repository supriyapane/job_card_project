import React, { useState, useRef } from "react";
import "./App.css";
import search from "./assets/search.svg";
import voiceSearch from "./assets/voice-search-icon.svg";

const App = () => {
  const [jobJson, setJobJson] = useState(null);
  const [listening, setListening] = useState(false);
  const [textInput, setTextInput] = useState("");
  const recognitionRef = useRef(null);

  const startListening = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech recognition not supported in this browser");
      return;
    }

    const recognition = new SpeechRecognition();
    recognitionRef.current = recognition;

    recognition.lang = "en-IN";
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    setListening(true);
    recognition.start();

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;
      setTextInput(text);
      setTimeout(() => callBackend(text), 100);
    };

    recognition.onerror = (e) => {
      console.error("Mic error:", e.error);
      setListening(false);
    };

    recognition.onend = () => {
      setListening(false);
    };
  };

  const callBackend = async (text) => {
    try {
      const response = await fetch("http://127.0.0.1:5000/process-text", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        setJobJson({ error: true, message: `Server error: ${errorData.error || response.statusText}` });
        return;
      }

      const data = await response.json();
      setJobJson(data);
    } catch (error) {
      console.error("Error calling backend:", error);
      setJobJson({ error: true, message: "Backend connection failed" });
    }
  };

  // ⌨️ Text submit
  const handleTextSubmit = () => {
    if (!textInput.trim()) return;
    callBackend(textInput);
  };

  return (
    <div className="page-center">
      <h1 className="page-title">
        Job Card Creation Using Voice or Text
      </h1>

      <div className="search-container">
        <img src={search} className="search-icon" alt="search" />

        <textarea
          value={textInput}
          rows={1}
          className="search-input"
          placeholder="Enter job details or use voice..."
          onChange={(e) => setTextInput(e.target.value)}
          onInput={(e) => {
            e.target.style.height = "auto";
            e.target.style.height = e.target.scrollHeight + "px";
          }}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleTextSubmit();
            }
          }}
        />

        <img
          src={voiceSearch}
          className={`voice-search-icon ${listening ? "listening" : ""}`}
          alt="voice search"
          onClick={startListening}
        />
      </div>

      {jobJson && jobJson.error && (
        <div style={{ 
          color: "#721c24", 
          marginTop: "20px", 
          padding: "20px", 
          border: "2px solid #f5c6cb", 
          borderRadius: "12px",
          backgroundColor: "#f8d7da"
        }}>
          <h3 style={{ margin: "0 0 15px 0", color: "#721c24" }}>⚠️ Missing Required Fields</h3>
          
          {jobJson.missing_fields && jobJson.missing_fields.length > 0 ? (
            <div>
              <p><strong>Please provide these mandatory fields:</strong></p>
              <ul style={{ 
                margin: "15px 0", 
                paddingLeft: "25px", 
                lineHeight: "1.6"
              }}>
                {jobJson.missing_fields.map((field, index) => (
                  <li key={index} style={{ marginBottom: "5px", fontWeight: "500" }}>
                    {field}
                  </li>
                ))}
              </ul>
            </div>
          ) : (
            <div>
              <p style={{ margin: "0 0 10px 0" }}>
                <strong>Error:</strong> {jobJson.message || "Unknown error occurred"}
              </p>
              <p style={{ fontSize: "14px", color: "#721c24", margin: 0 }}>
                Please check your input and try again.
              </p>
            </div>
          )}
        </div>
      )}

      {jobJson && !jobJson.error && (
        <div className="json-block" style={{ marginTop: "20px" }}>
          <h3>Job Card Generated Successfully!</h3>
          <pre style={{ textAlign: "left", backgroundColor: "#f8f9fa", padding: "20px" }}>
            {JSON.stringify(jobJson, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default App;
