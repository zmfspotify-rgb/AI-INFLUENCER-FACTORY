# AI Influencer Factory

Local-first automation scaffold for generating influencer content (scripts, prompts, and posting plan) from configurable personas.

## What it does
- Loads influencers from `influencers/<name>` folders with `persona.json`, `style.json`, and `platforms.json`.
- Creates prompt packs for script, image, video, and voice using the rules outlined in the problem statement (imperfect speech, realistic visuals, vertical video style, XTTS v2 voice guidance).
- Writes a platform-specific plan to `outputs/<name>/plan.json`.
- Simulates scheduling by generating `outputs/posting_log.txt`.

## Tech stack (all local-friendly)
- Python 3 (standard library only for this scaffold)
- Extensible to SDXL, ControlNet/IP-Adapter, Stable Video Diffusion/AnimateDiff, XTTS v2, SadTalker/Wav2Lip, FFmpeg, and Playwright automation.

## Project layout
```
.
├── engine/
│   ├── generator.py   # builds prompts and plans
│   └── poster.py      # simulates scheduling/uploads
├── influencers/
│   └── luna/          # sample influencer
│       ├── persona.json
│       ├── style.json
│       ├── platforms.json
│       ├── face_refs/
│       └── voice.wav  # placeholder for XTTS v2 input
├── outputs/           # generated at runtime (ignored)
├── main.py            # pipeline entrypoint
└── launch_ai_influencer.bat
```

## Usage
Create a virtual environment and run the pipeline:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```
Generated assets live under `outputs/<influencer>/`:
- `plan.json` – platform-level prompts (script, image, video, voice)
- `script_prompt.txt`, `image_prompt.txt`, `video_prompt.txt`, `voice_prompt.txt`
- `posting_log.txt` – simulated scheduler log

### Adding a new influencer
1. Copy `influencers/luna` to a new folder name.
2. Update `persona.json`, `style.json`, and `platforms.json` to match the new persona.
3. Add `face_refs/` images and `voice.wav` for XTTS v2.
4. Run `python main.py` to generate prompts and posting plan.

## Tests
Run targeted tests with:
```bash
python -m unittest
```
