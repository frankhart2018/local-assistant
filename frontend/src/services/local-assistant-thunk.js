import { createAsyncThunk } from "@reduxjs/toolkit";

import * as localAssistantService from "./local-assistant-service";

const callServiceOrReturnError = async (serviceFn, args = null) => {
  try {
    const response = args === null ? await serviceFn() : await serviceFn(...args);
    return response;
  } catch (e) {
    return e;
  }
};

export const storePromptThunk = createAsyncThunk(
  "localAssistant/storePrompt",
  async (payload) => {
    console.log(payload);
    return await callServiceOrReturnError(localAssistantService.storePrompt, [
      payload.model,
      payload.system,
      payload.prompt,
    ]);
  }
);

export const fetchModelListThunk = createAsyncThunk(
  "localAssistant/fetchModelsList",
  async () => {
    return await callServiceOrReturnError(localAssistantService.fetchModelList);
  }
);
