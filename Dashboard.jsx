import { useState } from "react";
import Page from "../components/layout/Page";
import Card from "../components/ui/Card";
import Badge from "../components/ui/Badge";
import StatTile from "../components/ui/StatTile";
import Table from "../components/ui/Table";
import Tabs from "../components/ui/Tabs";

export default function Dashboard() {
  const [tab, setTab] = useState("Security");

  return (
    <Page title="Operations Dashboard" subtitle="Live-style operational metrics.">
      <Tabs tabs={["Security", "Funding", "Workforce"]} active={tab} onChange={setTab} />

      <div className="dashboard-grid">
        <Card title="Security Posture" badge={<Badge>Operational</Badge>}>
          <div className="stats-grid">
            <StatTile label="Incidents (30d)" value="3" trend="All contained" />
            <StatTile label="Uptime" value="99.9%" trend="Core infra" />
            <StatTile label="Protected Subscribers" value="1,000+" trend="DNS + CPE" />
          </div>

          <Table
            columns={["Alert", "Severity", "Status", "Updated"]}
            rows={[
              ["DDoS attempt", "High", "Mitigated", "2h ago"],
              ["Suspicious DNS", "Medium", "Reviewing", "6h ago"],
              ["Endpoint offline", "Low", "Pending", "1d ago"],
            ]}
          />
        </Card>

        <Card title="Funding & Workforce Snapshot">
          <div className="stats-grid">
            <StatTile label="NTIA TBCP 2026" value="In Draft" trend="70% complete" />
            <StatTile label="BIA Alignment" value="On Track" trend="Facility plan ready" />
            <StatTile label="Active Apprentices" value="8" trend="Next cohort soon" />
          </div>
        </Card>
      </div>
    </Page>
  );
}
