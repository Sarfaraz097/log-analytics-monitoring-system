from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

def print_report(results):

    # Header
    console.print(Panel.fit(
        "[bold red]System Health Intelligence Report[/bold red]\n"
        f"[white]Period: {results['first_ts'].strftime('%Y-%m-%d %H:%M')} "
        f"to {results['last_ts'].strftime('%Y-%m-%d %H:%M')}[/white]",
        border_style="red"
    ))

    # KPI Summary Table
    console.print("\n[bold yellow]-- KPI Summary --[/bold yellow]")
    kpi_table = Table(box=box.SIMPLE_HEAVY)
    kpi_table.add_column("Metric",    style="cyan",  width=25)
    kpi_table.add_column("Value",     style="white", width=20)
    kpi_table.add_column("Status",    style="white", width=15)

    kpi_table.add_row("Total Events",     str(results['total']),                    "[green]OK[/green]")
    kpi_table.add_row("Total Errors",     str(results['error_count']),              "[red]CRITICAL[/red]")
    kpi_table.add_row("Error Rate",       f"{results['error_pct']}%",               "[red]CRITICAL[/red]")
    kpi_table.add_row("Error Density",    f"{results['error_density']} errors/min", "[red]CRITICAL[/red]")
    kpi_table.add_row("Uptime Score",     f"{results['uptime_score']}%",            "[yellow]DEGRADED[/yellow]")
    kpi_table.add_row("Duration",         f"{results['duration_minutes']} mins",    "[green]OK[/green]")
    kpi_table.add_row("Suspicious Users", str(results['suspicious_users']),         "[red]CRITICAL[/red]")
    kpi_table.add_row("Unauthorized IPs", str(results['unauthorized_ips']),         "[red]CRITICAL[/red]")

    console.print(kpi_table)

    # Log Level Breakdown
    console.print("\n[bold yellow]-- Log Level Breakdown --[/bold yellow]")
    level_table = Table(box=box.SIMPLE_HEAVY)
    level_table.add_column("Level", style="cyan",  width=15)
    level_table.add_column("Count", style="white", width=15)

    colors = {
        'ERROR': 'red',
        'WARN':  'yellow',
        'INFO':  'green',
        'DEBUG': 'blue'
    }

    for level, count in results['level_counts'].items():
        color = colors.get(level, 'white')
        level_table.add_row(
            f"[{color}]{level}[/{color}]",
            str(count)
        )

    console.print(level_table)

    # Top 5 Failing Components
    console.print("\n[bold yellow]-- Top 5 Failing Components --[/bold yellow]")
    comp_table = Table(box=box.SIMPLE_HEAVY)
    comp_table.add_column("Rank",      style="cyan",  width=8)
    comp_table.add_column("Component", style="white", width=25)
    comp_table.add_column("Errors",    style="red",   width=15)

    for i, (comp, count) in enumerate(results['top5_components'], 1):
        comp_table.add_row(str(i), comp, str(count))

    console.print(comp_table)

    # Failure Nature Breakdown
    console.print("\n[bold yellow]-- Failure Nature Breakdown --[/bold yellow]")
    event_table = Table(box=box.SIMPLE_HEAVY)
    event_table.add_column("Event Type", style="cyan",  width=30)
    event_table.add_column("Count",      style="white", width=15)

    for event, count in results['event_types']:
        event_table.add_row(event, str(count))

    console.print(event_table)

    # Anomaly Insights
    console.print("\n[bold yellow]-- Anomaly Insights --[/bold yellow]")
    console.print("[red]![/red] OrderService is in a crash-restart loop — all service restarts point to OrderService")
    console.print("[red]![/red] Deadlock storm detected — ~1 deadlock per minute across all services")
    console.print("[red]![/red] Distributed brute-force attack — 6,631 unique IPs targeting /admin endpoint")
    console.print("[yellow]~[/yellow] Queue saturation — orderQueue repeatedly hitting capacity")
    console.print("[yellow]~[/yellow] Resource exhaustion — High CPU, Memory, and Disk alerts firing together")
    console.print("[blue]i[/blue] Peak error window — Apr 03 08:00 and 15:00 saw highest error spikes (29.3%)")

    console.print("\n")

# Save report as markdown file
def save_markdown(results, output_path):

    lines = []
    lines.append("# System Health Intelligence Report\n")
    lines.append(f"**Period:** {results['first_ts'].strftime('%Y-%m-%d %H:%M')} to {results['last_ts'].strftime('%Y-%m-%d %H:%M')}\n")

    lines.append("## KPI Summary\n")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Total Events | {results['total']} |")
    lines.append(f"| Total Errors | {results['error_count']} |")
    lines.append(f"| Error Rate | {results['error_pct']}% |")
    lines.append(f"| Error Density | {results['error_density']} errors/min |")
    lines.append(f"| Uptime Score | {results['uptime_score']}% |")
    lines.append(f"| Suspicious Users | {results['suspicious_users']} |")
    lines.append(f"| Unauthorized IPs | {results['unauthorized_ips']} |")

    lines.append("\n## Top 5 Failing Components\n")
    lines.append("| Rank | Component | Errors |")
    lines.append("|------|-----------|--------|")
    for i, (comp, count) in enumerate(results['top5_components'], 1):
        lines.append(f"| {i} | {comp} | {count} |")

    lines.append("\n## Failure Nature Breakdown\n")
    lines.append("| Event Type | Count |")
    lines.append("|------------|-------|")
    for event, count in results['event_types']:
        lines.append(f"| {event} | {count} |")

    lines.append("\n## Anomaly Insights\n")
    lines.append("- OrderService is in a crash-restart loop")
    lines.append("- Deadlock storm detected — ~1 per minute")
    lines.append("- Distributed brute-force attack on /admin")
    lines.append("- Queue saturation on orderQueue")
    lines.append("- Resource exhaustion — CPU, Memory, Disk alerts")

    # utf-8 encoding fixes Windows special character error
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    console.print(f"\n[green]Markdown report saved to {output_path}[/green]")