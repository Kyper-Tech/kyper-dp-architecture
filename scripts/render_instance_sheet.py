#!/usr/bin/env python3
"""Generate a developer instance sheet for one tenant x environment (ADR-0013).

Joins three sources, each authoritative for one thing:
  - the model (structure, names, contracts)      architecture/model/  via likec4 export json
  - bindings (product per tenant class)          architecture/bindings/storage.yaml
  - a tenant registry record (instance facts)    --record

Sheets are build artifacts: never authored, never committed.

Usage:
  python3 scripts/render_instance_sheet.py --record architecture/tenant-registry/example-acme.yaml \
      --env nonprod [--model-json model.json] [--out sheet.md]
"""
import argparse, json, pathlib, subprocess, sys, tempfile
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_model(model_json: str | None) -> dict:
    if model_json:
        return json.loads(pathlib.Path(model_json).read_text())
    with tempfile.TemporaryDirectory() as td:
        out = pathlib.Path(td) / "model.json"
        subprocess.run(
            ["npx", "likec4", "export", "json", "-o", str(out), "architecture/model"],
            cwd=ROOT, check=True, capture_output=True,
        )
        return json.loads(out.read_text())


def by_kyp_id(model: dict) -> dict:
    out = {}
    for el in model["elements"].values():
        kid = (el.get("metadata") or {}).get("kypId")
        if kid:
            out[kid] = el
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--record", required=True)
    ap.add_argument("--env", required=True)
    ap.add_argument("--model-json")
    ap.add_argument("--bindings", default=str(ROOT / "architecture/bindings/storage.yaml"))
    ap.add_argument("--out")
    a = ap.parse_args()

    record = yaml.safe_load(pathlib.Path(a.record).read_text())
    bindings = yaml.safe_load(pathlib.Path(a.bindings).read_text())
    model = load_model(a.model_json)
    elements = by_kyp_id(model)

    tclass = record["tenantClass"]
    env = record["environments"].get(a.env)
    if env is None:
        sys.exit(f"environment '{a.env}' not in record (has: {list(record['environments'])})")

    L = []
    L.append(f"# {record['tenant']} — {a.env} instance sheet")
    L.append("")
    L.append("Generated (ADR-0013). Do not edit; regenerate from the tenant registry record.")
    L.append("")
    L.append(f"- tenant class: **{tclass}** · availability: {record.get('availabilityPosture', '-')}")
    L.append(f"- ingestion mode: {record.get('ingestionMode', '-')} · modules: {', '.join(record.get('enabledModules', []))}")
    pins = record.get("versionPins", {})
    L.append(f"- version pins: {', '.join(f'{k} {v}' for k, v in pins.items()) or '-'}")
    sites = record.get("sites", [])
    if sites:
        site_list = ", ".join("{} ({})".format(s["site"], s["siteClass"]) for s in sites)
        L.append(f"- sites: {site_list}")
    L.append("")

    L.append("## Your endpoints")
    L.append("")
    L.append("| Component | KYP-ID | URL |")
    L.append("|---|---|---|")
    for kid, url in env.get("endpoints", {}).items():
        el = elements.get(kid)
        name = el["title"] if el else "!! unknown KYP-ID"
        L.append(f"| {name} | {kid} | {url} |")
    L.append("")

    L.append("## Resolved products (per tenant class, from bindings)")
    L.append("")
    L.append("| Component | KYP-ID | Contract | Product | Posture |")
    L.append("|---|---|---|---|---|")
    for kid, entry in bindings.items():
        if not isinstance(entry, dict) or "contract" not in entry:
            continue  # skips contract-profiles
        el = elements.get(kid)
        name = el["title"] if el else "!! unknown KYP-ID"
        b = entry["bindings"].get(tclass, {})
        L.append(f"| {name} | {kid} | {entry['contract']} | {b.get('product', '?')} | {b.get('posture', '?')} |")
    L.append("")

    quotas = env.get("quotas", {})
    if quotas:
        L.append("## Quotas")
        L.append("")
        L.append(", ".join(f"{k}: {v}" for k, v in quotas.items()))
        L.append("")

    L.append("## Rules in this environment")
    L.append("")
    if a.env == "prod":
        L.append("- Only the prod orchestration identity writes the curated zone (ADR-0006).")
        L.append("- Runtimes accept only signed, promoted artifacts and models (admission; ADR-0004).")
    else:
        L.append("- Read curated/raw per data classification, via the catalog only (ADR-0006).")
        L.append("- Write only to your environment's sandbox zone (ADR-0006).")
    L.append("- Dev workspace publishes only to source/artifact repos; curated data scope (ADR-0012).")
    L.append("- ML workspace publishes only to model registry + experiments; raw reads audited (ADR-0012).")
    L.append("- Nothing durable in workspaces: losing one costs only uncommitted work (ADR-0004).")
    L.append("")

    text = "\n".join(L)
    if a.out:
        pathlib.Path(a.out).write_text(text)
        print(f"wrote {a.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
