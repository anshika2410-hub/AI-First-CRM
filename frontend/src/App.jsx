import "./App.css";
import InteractionForm from "./components/InteractionForm";
import ChatAssistant from "./components/ChatAssistant";
import DashboardStats from "./components/DashboardStats";
import { useState } from "react";
function App() {
  const [aiFormData, setAiFormData] = useState({});
  return (
    <div className="app">

      <div className="page-title">
        <h1>Log HCP Interaction</h1>
      </div>
        <DashboardStats />
      <div className="dashboard">

        <div className="left-panel">
          <InteractionForm
    aiFormData={aiFormData}
/>
        </div>

        <div className="right-panel">
          <ChatAssistant
    setAiFormData={setAiFormData}
/>
        </div>

      </div>

    </div>
  );
}

export default App;