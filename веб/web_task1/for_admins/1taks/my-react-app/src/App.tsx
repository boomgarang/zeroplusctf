import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/login/login";
import Panel from "./components/panel/panel";
import CookieConsent from "./components/cookies/CookieConsent";
import Dogovor from "./components/dogovor/dogorov.tsx";
import "./App.css";

function App() {
  return (
    // Wrap the routing logic with Router
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/panel" element={<Panel />} />
          <Route path="/cookies-dogovor" element={<Dogovor />} />
        </Routes>
        {/* CookieConsent отображается на всех страницах */}
        <CookieConsent />
      </div>
    </Router>
  );
}

export default App;
