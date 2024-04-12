import React, { useEffect, useState } from "react";
import Markdown from "react-markdown";
import { useDispatch, useSelector } from "react-redux";

import { storePromptThunk } from "../../../services/local-assistant-thunk";
import { API_BASE } from "../../../utils/constants";

import "./Chat.css";
import { clearPromptId } from "../../../reducers/local-assistant-reducer";

const Chat = () => {
  const [messages, setMessages] = useState("");
  const [systemPrompt, setSystemPrompt] = useState("");
  const [userPrompt, setUserPrompt] = useState("");
  const { promptId } = useSelector((state) => state.localAssistant);

  const dispatch = useDispatch();

  const callModel = () => {
    setMessages("");
    const eventSource = new EventSource(`${API_BASE}/stream-assistant?prompt_id=${promptId}`);

    eventSource.onmessage = function (event) {
      if (event.data.trim() === "END") {
        eventSource.close();
        dispatch(clearPromptId());
        return;
      }
      setMessages((prev) => {
        return `${prev}${event.data.replaceAll("<NEWLINE>", "\n")}`;
      });
    };

    eventSource.onerror = function (error) {
      console.error("EventSource failed:", error);
      dispatch(clearPromptId());
      eventSource.close();
    };
  };

  const savePrompt = () => {
    dispatch(
      storePromptThunk({
        model: "codegemma",
        system: systemPrompt,
        prompt: userPrompt,
      })
    );
  };

  useEffect(() => {
    if (promptId !== null) {
      callModel();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [promptId]);

  return (
    <div className="container">
      <p>
        <label htmlFor="system-prompt">System Prompt:</label>
        <input
          type="text"
          id="system-prompt"
          className="input"
          value={systemPrompt}
          onChange={(e) => setSystemPrompt(e.target.value)}
          autoFocus
        />
        <br />
        <br />
        <label htmlFor="user-prompt">User Prompt:</label>
        <input
          type="text"
          id="user-prompt"
          className="input"
          value={userPrompt}
          onChange={(e) => setUserPrompt(e.target.value)}
        />
        <br />
        <br />
        <input
          type="button"
          className="button"
          onClick={savePrompt}
          value="Prompt"
        />
      </p>
      <Markdown className="output-box">{messages}</Markdown>
    </div>
  );
};

export default Chat;
