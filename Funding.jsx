import Page from "../components/layout/Page";
import Card from "../components/ui/Card";
import Badge from "../components/ui/Badge";
import Table from "../components/ui/Table";

export default function Funding() {
  return (
    <Page title="Federal Funding Alignment" subtitle="NTIA TBCP 2026 & BIA mapping.">
      <Card
        title="NTIA TBCP 2026"
        subtitle="$500M+ available • 30–40% Tribal match"
        badge={<Badge type="cyan">Spring 2026</Badge>}
      >
        <Table
          columns={["Requirement", "Module", "Evidence"]}
          rows={[
            ["Broadband Security", "Network Stack", "Firewall configs, IDS logs"],
            ["Workforce", "Training", "Completion reports"],
            ["Digital Equity", "Subscriber Protection", "CPE rollout"],
          ]}
        />
      </Card>
    </Page>
  );
}
