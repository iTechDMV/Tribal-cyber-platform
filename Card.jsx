export default function Card({ title, subtitle, badge, children }) {
  return (
    <div className="card">
      {(title || badge) && (
        <div className="card-header">
          <div>
            {title && <div className="card-title">{title}</div>}
            {subtitle && <div className="card-subtitle">{subtitle}</div>}
          </div>
          {badge}
        </div>
      )}
      {children}
    </div>
  );
}
