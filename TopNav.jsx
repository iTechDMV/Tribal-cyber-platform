export default function TopNav() {
  return (
    <header className="top-nav">
      <div className="top-nav-left">
        <div className="brand-mark" />
        <div className="top-nav-title">Tribal Cyber Platform</div>
      </div>

      <nav className="top-nav-links">
        <a href="/">Overview</a>
        <a href="/funding">Funding</a>
        <a href="/workforce">Workforce</a>
        <a href="/dashboard">Dashboard</a>
      </nav>
    </header>
  );
}
