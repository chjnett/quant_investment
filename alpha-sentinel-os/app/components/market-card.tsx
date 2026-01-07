export function MarketCard({ title, value, change }: { title: string; value: string; change: string }) {
    const isPositive = change.startsWith("+");
    return (
        <div className="rounded-lg border bg-card text-card-foreground shadow-sm p-6">
            <div className="flex flex-row items-center justify-between space-y-0 pb-2">
                <h3 className="tracking-tight text-sm font-medium">{title}</h3>
            </div>
            <div className="text-2xl font-bold">{value}</div>
            <p className={`text-xs ${isPositive ? "text-green-500" : "text-red-500"}`}>
                {change} from last session
            </p>
        </div>
    );
}
