import React, { useState, useRef } from "react";
import search from "./assets/search.svg";
import voiceSearch from "./assets/voice-search-icon.svg";
import "./App.css"
const App = () => {
  const [jobJson, setJobJson] = useState(null);
  const [listening, setListening] = useState(false);
  const [textInput, setTextInput] = useState("");
  const [spokenText, setSpokenText] = useState("");
  const [isVoiceInput, setIsVoiceInput] = useState(false);

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

    setListening(true);
    recognition.start();

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;

      setIsVoiceInput(true);
      setSpokenText(text);
      setTextInput(text);
      createJobFromInput(text);
    };

    recognition.onerror = () => {
      setListening(false);
    };

    recognition.onend = () => {
      setListening(false);
    };
  };

  const createJobFromInput = async (text) => {
    try {
      setJobJson(null); 

      const response = await fetch("http://127.0.0.1:5000/create-job", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();
      setJobJson(data);
    } catch (error) {
      console.error("Backend error:", error);
      setJobJson({
        error: true,
        missing_fields: [],
        message: "Backend connection failed",
      });
    }
  };

  const handleTextSubmit = () => {
    if (!textInput.trim()) return;

    setIsVoiceInput(false);
    createJobFromInput(textInput);
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
          placeholder="Enter job details..."
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

      {listening && (
        <div className="listening-text">
           Listening...
        </div>
      )}

      {isVoiceInput && spokenText && (
        <div className="spoken-box">
          <h3>Spoken Text:</h3>
          <p>{spokenText}</p>
        </div>
      )}

      {jobJson?.error && jobJson?.missing_fields?.length > 0 && (
        <div className="error-box">
          <h3>Please fill below mandatory fields:</h3>
          <ul>
            {jobJson.missing_fields.map((field, index) => (
              <li key={index}>{field}</li>
            ))}
          </ul>
        </div>
      )}

      {jobJson?.error &&
        (!jobJson?.missing_fields ||
          jobJson?.missing_fields.length === 0) && (
          <div className="error-box">
            <h3>{jobJson.message || "Something went wrong"}</h3>
          </div>
        )}

      {jobJson && !jobJson.error && (
        <div className="json-block">
          <h3>Job Card Generated Successfully!</h3>
          <pre>
            {JSON.stringify(jobJson, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default App;
