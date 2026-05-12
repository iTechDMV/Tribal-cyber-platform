import { BrowserRouter, Routes, Route } from "react-router-dom";
import TopNav from "./components/layout/TopNav";
import Overview from "./pages/Overview";
import Funding from "./pages/Funding";
import Workforce from "./pages/Workforce";
import Dashboard from "./pages/Dashboard";
import "./theme.css";

export default function App() {
  return (
    <BrowserRouter>
      <TopNav />
      <Routes>
        <Route path="/" element={<Overview />} />
        <Route path="/funding" element={<Funding />} />
        <Route path="/workforce" element={<Workforce />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}
