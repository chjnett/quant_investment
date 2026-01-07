"use client";

export function AgentLogs() {
    return (
        <div className="rounded-lg border bg-card text-card-foreground shadow-sm">
            <div className="p-6 flex flex-col space-y-1.5">
                <h3 className="font-semibold leading-none tracking-tight">Agent Logs</h3>
                <p className="text-sm text-muted-foreground">Real-time reasoning logs</p>
            </div>
            <div className="p-6 pt-0">
                <div className="text-sm font-mono bg-muted p-4 rounded h-40 overflow-y-auto">
                    <p>[INFO] Macro Sentry: Analyzing inflation data...</p>
                    <p>[INFO] CIO: Evaluating risk parameters...</p>
                </div>
            </div>
        </div>
    );
}
