#!/usr/bin/env python3
"""Derive the cross-environment access whitelist from the model (ADR-0006).

A cross-environment path is a relation whose source is in an env-scoped area
and whose target is outside every env-scoped area. Such a path may target a
mediating service, a registry, or a per-environment store — never a store
marked shared 'across-envs'. The table this prints is the only network reach
a non-production environment has into shared data; paste it into the brief
between the cross-env markers, never hand-edit it.

Usage:  python3 scripts/render_cross_env_paths.py [--model-json model.json]
"""
import argparse, json, pathlib, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_model(path):
    if path:
        return json.loads(pathlib.Path(path).read_text())
    with tempfile.TemporaryDirectory() as td:
        out = pathlib.Path(td) / "model.json"
        subprocess.run(["npx", "likec4", "export", "json", "-o", str(out), "architecture/model"],
                       cwd=ROOT, check=True, capture_output=True)
        return json.loads(out.read_text())


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--model-json"); a = ap.parse_args()
    j = load_model(a.model_json); E = j["elements"]
    meta = lambda i: E[i].get("metadata", {})
    area = lambda i: ".".join(i.split(".")[:2])
    env_areas = {i for i in E if meta(i).get("envScoped") == "true"}
    shared = {i for i in E if meta(i).get("shared") == "across-envs"}

    rows, violations = [], []
    for r in j["relations"].values():
        s, t = r["source"]["model"], r["target"]["model"]
        if area(s) in env_areas and area(t) not in env_areas:
            if t in shared:
                violations.append(f"{s} -> {t} targets a shared store directly")
            rows.append((E[area(s)]["title"], E[t]["title"], E[t]["kind"], r.get("kind", "")))

    print("| From (per-environment area) | May reach | Target kind | Relation |")
    print("|---|---|---|---|")
    for src, tgt, kind, rel in sorted(set(rows)):
        print(f"| {src} | {tgt} | {kind} | {rel} |")
    print()
    print("Shared stores reachable directly from any per-environment area: "
          + (", ".join(sorted(violations)) if violations else "none"))
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
