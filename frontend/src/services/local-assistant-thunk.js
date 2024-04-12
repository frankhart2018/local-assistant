import { createAsyncThunk } from "@reduxjs/toolkit";

import * as localAssistantService from "./local-assistant-service";

export const storePromptThunk = createAsyncThunk(
  "localAssistant/storePrompt",
  async (payload) => {
    try {
      const response = await localAssistantService.storePrompt(
        payload.model,
        payload.system,
        payload.prompt
      );
      return response;
    } catch (e) {
      return e;
    }
  }
);
