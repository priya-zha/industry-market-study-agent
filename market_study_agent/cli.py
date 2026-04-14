import argparse
from pathlib import Path
from . import generator


def main():
    p = argparse.ArgumentParser(description="Market Study Agent (MVP)")
    p.add_argument("--industry", required=True, help="Industry short name (e.g., hvac)")
    p.add_argument("--output", required=True, help="Output markdown file path")
    args = p.parse_args()

    industry = args.industry
    out_path = Path(args.output)

    try:
        data = generator.load_sample_data(industry)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 2

    report = generator.generate_report(industry, data)
    generator.save_report(report, out_path)
    print(f"Generated market study: {out_path}")


if __name__ == "__main__":
    raise SystemExit(main())
