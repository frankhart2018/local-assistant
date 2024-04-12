import axios from "axios";

import { API_BASE } from "../utils/constants";

export const storePrompt = async (model, system, prompt) => {
  const response = await axios.post(`${API_BASE}/prompt`, {
    model,
    system,
    prompt,
  });

  return response;
};
