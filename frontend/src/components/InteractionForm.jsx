import "./InteractionForm.css";
import { useState, useEffect } from "react";
import { FaMicrophone } from "react-icons/fa";
import { saveInteraction } from "../services/api";
import { getFollowupSuggestion } from "../services/api";

const InteractionForm = ({ aiFormData }) => {

    const [aiSuggestion, setAiSuggestion] = useState("");
    const generateSuggestion = async () => {
  try {

    const res = await getFollowupSuggestion({
      outcome: form.outcome,
      sentiment: form.sentiment,
      topics: form.topics,
      
    });

    setAiSuggestion(res.suggestion);

  } catch (err) {

    console.log(err);

  }
};

    const [form, setForm] = useState({
  hcp_name: "",
  interaction_type: "Meeting",
  interaction_date: "",
  interaction_time: "",
  attendees: "",
  topics: "",
  materials_shared: "",
  samples_distributed: "",
  sentiment: "",
  outcome: "",
  follow_up: "",
});

   useEffect(() => {
  if (Object.keys(aiFormData).length) {

    const updatedForm = {
      ...form,
      ...aiFormData,
    };

    setForm(updatedForm);

    // AI follow-up automatically generate
    getFollowupSuggestion({
      outcome: updatedForm.outcome,
      sentiment: updatedForm.sentiment,
      topics: updatedForm.topics,
    })
      .then((res) => setAiSuggestion(res.suggestion))
      .catch(console.error);
  }
}, [aiFormData]);


    const handleChange = (e) => {
    setForm({
    ...form,
    [e.target.name]: e.target.value,
  });
};

const handleSubmit = async () => {
  try {

    await saveInteraction(form);

    alert("Interaction Saved Successfully!");
a
    setForm({
      hcp_name: "",
      interaction_type: "Meeting",
      interaction_date: "",
      interaction_time: "",
      attendees: "",
      topics: "",
      materials_shared: "",
      samples_distributed: "",
      sentiment: "",
      outcome: "",
      follow_up: "",
    });

  } catch (err) {
    console.log(err);
    alert("Failed to save interaction");
  }
};

  return (
    <div className="interaction-form">

      <div className="card-header">
        <h2>Interaction Details</h2>
      </div>

      {/* HCP Name */}

      <div className="form-group">
        <label>HCP Name</label>
        <input
            type="text"
            name="hcp_name"
            value={form.hcp_name}
            onChange={handleChange}
            placeholder="Search or Select HCP"
        />
      </div>

      {/* Interaction Type */}

      <div className="form-group">
        <label>Interaction Type</label>

        <select
            name="interaction_type"
            value={form.interaction_type}
            onChange={handleChange}>
          <option>Meeting</option>
          <option>Call</option>
          <option>Email</option>
          <option>Conference</option>
        </select>
      </div>

      {/* Date Time */}

      <div className="row">

        <div className="form-group">
          <label>Date</label>
          <input
    type="date"
    name="interaction_date"
    value={form.interaction_date}
    onChange={handleChange}
/>
        </div>

        <div className="form-group">
          <label>Time</label>
          <input
    type="time"
    name="interaction_time"
    value={form.interaction_time}
    onChange={handleChange}
/>
        </div>

      </div>

      {/* Attendees */}

      <div className="form-group">
        <label>Attendees</label>
        <input
    type="text"
    name="attendees"
    value={form.attendees}
    onChange={handleChange}
    placeholder="Enter attendees..."
/>
      </div>

      {/* Topics */}

      <div className="form-group">

        <label>Topics Discussed</label>

        <textarea
          rows="4"
          name="topics"
          value={form.topics}
          onChange={handleChange}
          placeholder="Describe discussion..."
        ></textarea>

      </div>

      {/* Voice */}

      <div className="voice-box">

        <button
  type="button"
  className="voice-btn"
  onClick={() => alert("Voice summarization feature coming soon!")}
>
  <FaMicrophone />
  <span>Summarize from Voice Note</span>
</button>

      </div>

      {/* Materials */}

      <div className="form-group">

        <label>Materials Shared</label>

        <textarea
          rows="3"
          name="materials_shared"
          value={form.materials_shared}
          onChange={handleChange}
          placeholder="Brochure, Clinical Paper..."
        ></textarea>

      </div>

      {/* Samples */}

      <div className="form-group">

        <label>Samples Distributed</label>

        <textarea
  rows="2"
  name="samples_distributed"
  value={form.samples_distributed}
  onChange={handleChange}
  placeholder="Enter distributed samples..."
></textarea>

      </div>

      {/* Sentiment */}

  <div className="form-group">

  <label>Observed / Inferred HCP Sentiment</label>

  <div className="emoji-radio-group">

    <label className="emoji-radio">
      <input
        type="radio"
        name="sentiment"
        value="Positive"
        checked={form.sentiment?.toLowerCase() === "positive"}
        onChange={handleChange}
      />
      <span>😊 Positive</span>
    </label>


    <label className="emoji-radio">
      <input
        type="radio"
        name="sentiment"
        value="Neutral"
        checked={form.sentiment?.toLowerCase() === "neutral"}
        onChange={handleChange}
      />
      <span>😐 Neutral</span>
    </label>


    <label className="emoji-radio">
      <input
        type="radio"
        name="sentiment"
        value="Negative"
        checked={form.sentiment?.toLowerCase() === "negative"}
        onChange={handleChange}
      />
      <span>😞 Negative</span>
    </label>

  </div>

</div>

      {/* Outcome */}

      <div className="form-group">

        <label>Outcomes</label>

        <textarea
          rows="3"
           name="outcome"
        value={form.outcome}
        onChange={handleChange}
        onBlur={generateSuggestion}
          placeholder="Meeting outcome..."
        ></textarea>

      </div>

      {/* Follow Up */}

      <div className="form-group">

        <label>Follow-up Actions</label>

        <textarea
          rows="3"
          name="follow_up"
        value={form.follow_up}
        onChange={handleChange}
          placeholder="Enter follow-up actions..."
        ></textarea>

      </div>

      {/* AI */}

      <div className="ai-box">

        <h4>AI Suggested Follow-ups</h4>

        <div className="ai-content">
  {aiSuggestion
    ? aiSuggestion
        .split("\n")
        .filter(item => item.trim() !== "")
        .map((item, index) => (
          <p key={index}>
            {item.replace("-", "•")}
          </p>
        ))
    : "AI recommendations will appear here..."}
</div>

      </div>

    </div>
  );
};

export default InteractionForm;