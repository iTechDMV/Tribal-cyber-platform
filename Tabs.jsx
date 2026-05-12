export default function Tabs({ tabs, active, onChange }) {
  return (
    <div className="tabs">
      {tabs.map((t) => (
        <div
          key={t}
          className={`tab ${active === t ? "active" : ""}`}
          onClick={() => onChange(t)}
        >
          {t}
        </div>
      ))}
    </div>
  );
}
