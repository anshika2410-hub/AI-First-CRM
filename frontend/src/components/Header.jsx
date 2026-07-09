import { FaUserMd } from "react-icons/fa";
import "./Header.css";

const Header = () => {
  return (
    <header className="header">

      <div className="header-left">
        <FaUserMd className="logo-icon" />

        <div>
          <h1>Log HCP Interaction</h1>
          <p>AI-First CRM • Healthcare Professional Module</p>
        </div>
      </div>

      <button className="save-btn">
        Save Draft
      </button>

    </header>
  );
};

export default Header;