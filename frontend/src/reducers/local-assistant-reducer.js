import { createSlice } from "@reduxjs/toolkit";
import { storePromptThunk } from "../services/local-assistant-thunk";

const initialState = {
  promptId: null,
};

const localAssistantSlice = createSlice({
  name: "localAssistant",
  initialState,
  reducers: {
    clearPromptId(state, _) {
      state.promptId = null;
    }
  },
  extraReducers: (builder) => {
    builder.addCase(storePromptThunk.fulfilled, (state, action) => {
      const payload = action.payload;

      if ("data" in payload) {
        state.promptId = payload.data.prompt_id;
      }
    });
  },
});

export const { clearPromptId } = localAssistantSlice.actions;
export default localAssistantSlice.reducer;
