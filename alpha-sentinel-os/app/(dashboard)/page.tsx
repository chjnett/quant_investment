import { MarketCard } from "@/app/components/market-card";
import { AgentLogs } from "@/app/components/agent-logs";

export default function DashboardPage() {
    return (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            <div className="col-span-full">
                <h2 className="text-2xl font-bold tracking-tight">Investment Dashboard</h2>
            </div>
            <MarketCard title="S&P 500" value="4,783.45" change="+0.5%" />
            <MarketCard title="NASDAQ" value="15,000.00" change="+1.2%" />

            <div className="col-span-full mt-4">
                <AgentLogs />
            </div>
        </div>
    );
}
