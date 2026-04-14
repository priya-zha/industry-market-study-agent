import json
from pathlib import Path
from typing import Dict, Any, List


def load_sample_data(industry: str) -> Dict[str, Any]:
    data_path = Path(__file__).parent / "data" / f"sample_{industry.lower()}.json"
    if data_path.exists():
        return json.loads(data_path.read_text())
    raise FileNotFoundError(f"No sample data for industry '{industry}' at {data_path}. Add a sample_{industry}.json file.")


def format_multiples(multiples: Dict[str, Any]) -> str:
    lines = []
    for bracket, stats in multiples.items():
        lines.append(f"- {bracket}: range {stats.get('range')}x, median {stats.get('median')}x, deals {stats.get('count')}")
    return "\n".join(lines)


def format_transactions(transactions: List[Dict[str, Any]]) -> str:
    lines = []
    for t in transactions:
        buyer = t.get("buyer")
        target = t.get("target")
        notes = t.get("notes", "")
        source = t.get("source", "")
        lines.append(f"- {buyer} acquired {target} — {notes} ({source})")
    return "\n".join(lines)


def generate_report(industry: str, data: Dict[str, Any]) -> str:
    title = f"Market Study — {industry.title()}"
    sections = []

    sections.append(f"# {title}\n")

    # Executive summary
    exec_sum = data.get("executive_summary", "No executive summary available.")
    sections.append("## Executive Summary\n" + exec_sum + "\n")

    # EBITDA Multiples
    multiples = data.get("ebitda_multiples", {})
    sections.append("## EBITDA Multiples by Deal Size\n" + format_multiples(multiples) + "\n")

    # Value Drivers
    value_drivers = data.get("value_drivers", [])
    sections.append("## Value Drivers\n" + "\n".join([f"- {v}" for v in value_drivers]) + "\n")

    # Recent Transactions
    transactions = data.get("recent_transactions", [])
    sections.append("## Recent Transactions\n" + (format_transactions(transactions) or "No recent transactions available.") + "\n")

    # Ideal Buyers
    ideal = data.get("ideal_buyers", [])
    sections.append("## Ideal Buyers\n" + "\n".join([f"- {b}: {r}" for b, r in ((d.get('name'), d.get('rationale')) for d in ideal)]) + "\n")

    # Possible Buyers
    possible = data.get("possible_buyers", [])
    sections.append("## Possible Buyers\n" + "\n".join([f"- {p}" for p in possible]) + "\n")

    # Appendix / Sources
    sources = data.get("sources", [])
    sections.append("## Sources\n" + "\n".join([f"- {s}" for s in sources]) + "\n")

    return "\n".join(sections)


def save_report(content: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content)


if __name__ == "__main__":
    # simple smoke test
    d = load_sample_data("hvac")
    report = generate_report("HVAC", d)
    print(report[:500])
