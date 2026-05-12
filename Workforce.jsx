import Page from "../components/layout/Page";
import Card from "../components/ui/Card";
import StatTile from "../components/ui/StatTile";

export default function Workforce() {
  return (
    <Page title="Workforce Development" subtitle="A Tribal-first cyber talent pipeline.">
      <div className="stats-grid">
        <StatTile label="Tribal Citizens Trained" value="20+" trend="Goal: 40+" />
        <StatTile label="Certification Rate" value="80%" trend="CompTIA / ISC²" />
        <StatTile label="Avg Wage Increase" value="40%" trend="Post-placement" />
      </div>

      <Card title="Training Phases">
        <ol>
          <li>Foundations (12 weeks)</li>
          <li>Technical Skills (16 weeks)</li>
          <li>Leadership (8 weeks)</li>
        </ol>
      </Card>
    </Page>
  );
}
