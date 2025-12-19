import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


def _load_plan(plan_path: Path) -> Optional[dict]:
    if not plan_path.exists():
        return None
    try:
        with plan_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None


def _write_log(log_path: Path, entries: List[str]) -> None:
    log_path.write_text("\n".join(entries), encoding="utf-8")


def post_content(
    generated: Optional[Iterable[Dict[str, Any]]] = None, output_root: str = "outputs"
) -> None:
    """
    Simulate posting content by creating a scheduling log.
    In a full implementation this would automate Playwright uploads.
    """
    out_root = Path(output_root)
    if not out_root.exists():
        return

    log_entries: List[str] = []
    plans = generated or []
    if not plans:
        # Discover plans from disk if not provided
        for child in out_root.iterdir():
            if child.is_dir():
                plan_path = child / "plan.json"
                if plan_path.exists():
                    plans.append({"plan_path": str(plan_path), "slug": child.name})

    for plan_meta in plans:
        plan_path = Path(plan_meta["plan_path"])
        plan = _load_plan(plan_path)
        if not plan:
            continue

        influencer = plan.get("influencer", plan_meta.get("slug", "unknown"))
        for platform in plan.get("platforms", []):
            entry = (
                f"[SCHEDULED] {influencer} -> {platform.get('platform')} | "
                f"genre={platform.get('genre')} length={platform.get('length')}"
            )
            log_entries.append(entry)

    if log_entries:
        _write_log(out_root / "posting_log.txt", log_entries)
