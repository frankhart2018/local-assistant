import React from "react";
import { configureStore } from "@reduxjs/toolkit";
import localAssistantReducer from "./reducers/local-assistant-reducer";
import { VERSION } from "./utils/version";
import { Provider } from "react-redux";
import { Route, Routes } from "react-router";
import Chat from "./components/pages/Chat/Chat";

const store = configureStore({
  reducer: {
    localAssistant: localAssistantReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
});

const App = () => {
  document.title = `Local Assistant v${VERSION}`;

  return (
    <Provider store={store}>
      <Routes>
        <Route path="/" element={<Chat />} />
      </Routes>
    </Provider>
  );
};

export default App;
