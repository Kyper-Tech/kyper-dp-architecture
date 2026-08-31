#!/usr/bin/env python3
"""Gate: KYP-ID uniqueness, ADR references resolve, store.class in vocabulary, ADR affects resolve."""
import re, sys, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
model = "\n".join(p.read_text() for p in (root/"architecture/model").rglob("*.likec4"))
adrs = {re.search(r"id:\s*(ADR-\d{4})", p.read_text()).group(1): p for p in (root/"adr").glob("0*.md")}
errors = []
ids = re.findall(r"kypId '([^']+)'", model)
dupes = {i for i in ids if ids.count(i) > 1}
if dupes: errors.append(f"duplicate kypId: {sorted(dupes)}")
for ref in {r for group in re.findall(r"adr '([^']+)'", model) for r in group.split(",")}:
    if ref.strip() not in adrs: errors.append(f"model references missing {ref.strip()}")
classes = re.findall(r"= store [^{]*\{[^}]*class '([^']+)'", model)
for c in classes:
    if c not in {"analytical", "operational", "online"}: errors.append(f"unknown store.class '{c}'")
stores = len(re.findall(r"= store ", model))
if stores != len(classes): errors.append(f"{stores - len(classes)} store(s) missing metadata.class")
for adr, p in adrs.items():
    for kid in re.findall(r"KYP-[A-Z]-[A-Z]+(?:-\d{2})?|KYP-[CTE]\b", p.read_text().split("---")[1]):
        if kid not in ids and kid not in {"KYP-C", "KYP-T", "KYP-E"}: errors.append(f"{adr} affects unknown {kid}")
print("\n".join(errors) or "gate: ok"); sys.exit(1 if errors else 0)
