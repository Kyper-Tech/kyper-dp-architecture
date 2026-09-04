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
    fm = p.read_text().split("---")[1]
    for kid in re.findall(r"KYP-[A-Z]-[A-Z]+(?:-\d{2})?|KYP-[CFSTE]\b", fm):
        if kid not in ids and kid not in {"KYP-C", "KYP-F", "KYP-S", "KYP-T", "KYP-E"}: errors.append(f"{adr} affects unknown {kid}")
    # amends: every amended ADR must exist and reference the amender back
    m = re.search(r"^amends:\s*\[([^\]]*)\]", fm, re.M)
    for target in (t.strip() for t in m.group(1).split(",") if t.strip()) if m else []:
        if target not in adrs: errors.append(f"{adr} amends missing {target}")
        elif adr not in adrs[target].read_text(): errors.append(f"{target} does not reference its amender {adr}")
# cross-environment rule (ADR-0006): an env-scoped area may reach a mediating
# service or a per-env store, never a store marked shared 'across-envs'.
env_areas, shared_stores, relations = set(), set(), []
for p in (root/"architecture/model").rglob("*.likec4"):
    txt = p.read_text(); plane = re.search(r"^\s*(\w+)\s*=\s*plane\b", txt, re.M)
    if not plane: continue
    pl = plane.group(1)
    for m in re.finditer(r"(\w+)\s*=\s*area\s+'[^']*'\s*\{(.*?)(?=\n\s*\w+\s*=\s*(?:service|store|registry|boundary)\b)", txt, re.S):
        if "envScoped 'true'" in m.group(2): env_areas.add(f"{pl}.{m.group(1)}")
    for m in re.finditer(r"(\w+)\s*=\s*store\s+'[^']*'\s*\{([^}]*)\}", txt):
        if "shared 'across-envs'" in m.group(2): shared_stores.add((pl, m.group(1)))
    relations += re.findall(r"^\s*([\w.]+)\s*-\[\w+\]->\s*([\w.]+)", txt, re.M)
for s, t in relations:
    if ".".join(s.split(".")[:2]) in env_areas and (t.split(".")[0], t.split(".")[-1]) in shared_stores:
        errors.append(f"cross-env violation: {s} reaches shared store {t} directly")
print("\n".join(errors) or "gate: ok"); sys.exit(1 if errors else 0)
