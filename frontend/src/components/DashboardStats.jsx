import { useEffect, useState } from "react";
import { getDashboard } from "../services/api";
import "./DashboardStats.css";

const DashboardStats = () => {

  const [stats, setStats] = useState({
    total: 0,
    positive: 0,
    doctors: 0,
    today: 0,
  });

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const data = await getDashboard();
      setStats(data);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className="stats-container">

      <div className="stat-card">
        <h3>{stats.total}</h3>
        <p>Total Interactions</p>
      </div>

      <div className="stat-card">
        <h3>{stats.positive}</h3>
        <p>Positive</p>
      </div>

      <div className="stat-card">
        <h3>{stats.doctors}</h3>
        <p>Doctors</p>
      </div>

      <div className="stat-card">
        <h3>{stats.today}</h3>
        <p>Today's Meetings</p>
      </div>

    </div>
  );
};

export default DashboardStats;