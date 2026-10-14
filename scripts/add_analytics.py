"""Mesure d'audience du site (Cloudflare Web Analytics, sans cookies) : ajoute le script de Cloudflare dans le <head>
de chaque page, entre deux repères, ou le retire si aucun jeton n'est donné. Idempotent.
Jeton (public : il est dans le code des pages) dans scripts/analytics.json, {"cloudflare_token": "..."}.
À relancer après make_en.py / make_windows.py / make_android.py (ils réécrivent les pages)."""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
START, END = "<!-- cf-analytics -->", "<!-- /cf-analytics -->"
# Redirection pure : pas de visite à compter.
SKIP = {"privacy/index.html"}


def token() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1].strip()
    f = ROOT / "scripts" / "analytics.json"
    return json.loads(f.read_text()).get("cloudflare_token", "").strip() if f.exists() else ""


def run() -> None:
    t = token()
    block = (
        f"{START}\n<script defer src=\"https://static.cloudflareinsights.com/beacon.min.js\" "
        f"data-cf-beacon='{{\"token\": \"{t}\"}}'></script>\n{END}\n"
        if t else ""
    )
    for page in sorted(ROOT.rglob("*.html")):
        rel = page.relative_to(ROOT).as_posix()
        if rel in SKIP or rel.startswith((".git/", "node_modules/")):
            continue
        s = page.read_text(encoding="utf-8")
        s2 = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", s, flags=re.S)
        if block:
            s2 = s2.replace("</head>", block + "</head>", 1)
        if s2 != s:
            page.write_text(s2, encoding="utf-8")
            print(("ajouté : " if block else "retiré : ") + rel)


if __name__ == "__main__":
    run()
