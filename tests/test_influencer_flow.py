import json
import shutil
import unittest
from pathlib import Path

from engine.generator import generate_content
from engine.poster import post_content


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = PROJECT_ROOT / "outputs"


class InfluencerFlowTest(unittest.TestCase):
    def setUp(self) -> None:
        if OUTPUTS.exists():
            shutil.rmtree(OUTPUTS)

    def tearDown(self) -> None:
        if OUTPUTS.exists():
            shutil.rmtree(OUTPUTS)

    def test_generate_and_post_creates_plan_and_log(self) -> None:
        generated = generate_content()
        self.assertTrue(generated, "No influencers were generated")

        # Validate plan.json contents
        plan_path = OUTPUTS / "luna" / "plan.json"
        self.assertTrue(plan_path.exists(), "plan.json was not created")
        with plan_path.open("r", encoding="utf-8") as handle:
            plan = json.load(handle)

        self.assertEqual(plan.get("influencer"), "luna")
        self.assertTrue(plan.get("platforms"), "Platforms missing from plan")
        first_platform = plan["platforms"][0]
        self.assertIn("script_prompt", first_platform)
        self.assertIn("image_prompt", first_platform)
        self.assertIn("video_prompt", first_platform)
        self.assertIn("voice_prompt", first_platform)

        # Simulate posting
        post_content(generated)
        log_path = OUTPUTS / "posting_log.txt"
        self.assertTrue(log_path.exists(), "Posting log was not created")
        contents = log_path.read_text(encoding="utf-8")
        self.assertIn("luna", contents)


if __name__ == "__main__":
    unittest.main()
