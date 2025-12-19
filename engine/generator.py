import json
from pathlib import Path
from typing import Dict, List, Optional


BASE_IMAGE_PROMPT = (
    "Ultra-realistic photo of a young influencer, natural skin texture, imperfect lighting, "
    "candid expression, DSLR depth of field, realistic pores, cinematic lighting, not AI-looking, "
    "Instagram aesthetic"
)

BASE_VIDEO_PROMPT = (
    "Short vertical video, natural head movement, realistic blinking, subtle facial "
    "micro-expressions, hand gestures, casual posture, phone camera realism, TikTok style"
)


def _load_json(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _discover_influencers(influencer_root: Path) -> List[Dict]:
    influencers: List[Dict] = []
    if not influencer_root.exists():
        return influencers

    for child in influencer_root.iterdir():
        if not child.is_dir():
            continue

        persona_path = child / "persona.json"
        style_path = child / "style.json"
        platforms_path = child / "platforms.json"

        if not (persona_path.exists() and style_path.exists() and platforms_path.exists()):
            # skip incomplete influencer folders
            continue

        influencers.append(
            {
                "slug": child.name,
                "persona": _load_json(persona_path),
                "style": _load_json(style_path),
                "platforms": _load_json(platforms_path),
            }
        )
    return influencers


def _script_prompt(persona: Dict, platform: str, length: str, topic: str) -> str:
    catchphrases = ", ".join(persona.get("catchphrases", []))
    boundaries = ", ".join(persona.get("boundaries", []))
    return (
        "You are an AI influencer speaking naturally like a real human.\n"
        "Rules:\n"
        "- imperfect speech\n"
        "- short pauses\n"
        "- emotional reactions\n"
        "- casual phrasing\n"
        "- subtle personality quirks\n\n"
        f"Name: {persona.get('name')}\n"
        f"Vibe: {persona.get('vibe')}\n"
        f"Speech style: {persona.get('speech_style')}\n"
        f"Catchphrases: {catchphrases}\n"
        f"Boundaries: {boundaries}\n\n"
        f"Topic: {topic}\n"
        f"Platform: {platform}\n"
        f"Length: {length}\n\n"
        "Make it feel like a real person talking to a camera."
    )


def _voice_prompt(persona: Dict) -> str:
    return (
        "Voice generation using XTTS v2 (Coqui)\n"
        f"Desired vibe: {persona.get('vibe')}\n"
        f"Speech style: {persona.get('speech_style')}\n"
        "Include subtle breaths and natural imperfections. "
        "Do not generate robotic delivery."
    )


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def generate_content(
    influencer_root: str = "influencers",
    output_root: str = "outputs",
    topic: str = "Daily idea",
) -> List[Dict]:
    """Generate prompt packs for each influencer."""
    root_path = Path(influencer_root)
    out_root = Path(output_root)
    _ensure_dir(out_root)

    influencers = _discover_influencers(root_path)
    generated: List[Dict] = []

    for influencer in influencers:
        persona = influencer["persona"]
        slug = influencer["slug"]
        platforms = influencer["platforms"]
        style = influencer["style"]

        influencer_dir = out_root / slug
        _ensure_dir(influencer_dir)

        image_prompt = BASE_IMAGE_PROMPT + f", style: {style.get('visual', '')}"
        video_prompt = BASE_VIDEO_PROMPT + f", style: {style.get('video', '')}"
        voice_prompt = _voice_prompt(persona)

        platform_plans: List[Dict[str, Optional[str]]] = []
        for platform_name, meta in platforms.items():
            length = meta.get("length", "60s")
            platform_topic = meta.get("focus", topic)
            script_prompt = _script_prompt(persona, platform_name, length, platform_topic)
            platform_plans.append(
                {
                    "platform": platform_name,
                    "genre": meta.get("genre"),
                    "length": length,
                    "script_prompt": script_prompt,
                    "image_prompt": image_prompt,
                    "video_prompt": video_prompt,
                    "voice_prompt": voice_prompt,
                }
            )

        # Write consolidated plan
        plan_path = influencer_dir / "plan.json"
        with plan_path.open("w", encoding="utf-8") as handle:
            json.dump(
                {"influencer": slug, "platforms": platform_plans, "style": style},
                handle,
                indent=2,
            )

        # Also keep plain-text prompt files for quick copy
        script_text = (
            platform_plans[0]["script_prompt"]
            if platform_plans
            else "No platform prompts configured."
        )
        (influencer_dir / "script_prompt.txt").write_text(
            script_text, encoding="utf-8"
        )
        (influencer_dir / "image_prompt.txt").write_text(image_prompt, encoding="utf-8")
        (influencer_dir / "video_prompt.txt").write_text(video_prompt, encoding="utf-8")
        (influencer_dir / "voice_prompt.txt").write_text(voice_prompt, encoding="utf-8")

        generated.append({"slug": slug, "plan_path": str(plan_path)})

    return generated
