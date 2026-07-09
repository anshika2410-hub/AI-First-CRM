import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const sendMessage = async (message) => {
  const response = await API.post("/chat", {
    message,
  });

  return response.data;
};

export const saveInteraction = async (interaction) => {
  const response = await API.post("/interactions", interaction);
  return response.data;
};

export const getFollowupSuggestion = async (data) => {
  const response = await axios.post(
    "http://127.0.0.1:8000/suggest-followup",
    data
  );

  return response.data;
};

export const getDashboard = async () => {
  const response = await axios.get("http://127.0.0.1:8000/dashboard");
  return response.data;
};
export default API;