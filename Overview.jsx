import Page from "../components/layout/Page";
import Button from "../components/ui/Button";
import StatTile from "../components/ui/StatTile";

export default function Overview() {
  return (
    <Page
      title="Tribal Cybersecurity Platform"
      subtitle="Federal funding ready — NTIA TBCP 2026 & BIA aligned."
    >
      <div className="btn-row">
        <Button>View Funding Alignment</Button>
        <Button variant="outline">Download Checklist</Button>
      </div>

      <div className="stats-grid">
        <StatTile label="Households Protected" value="1,000+" trend="Target: 1,500" />
        <StatTile label="Anchor Institutions" value="25+" trend="Growing" />
        <StatTile label="Tribal Citizens Trained" value="20+" trend="Scaling" />
      </div>
    </Page>
  );
}
