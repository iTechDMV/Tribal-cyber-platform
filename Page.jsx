export default function Page({ title, subtitle, children }) {
  return (
    <main className="page">
      {title && <h1 className="page-title">{title}</h1>}
      {subtitle && <p className="page-subtitle">{subtitle}</p>}
      {children}
    </main>
  );
}
