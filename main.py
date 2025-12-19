from engine.generator import generate_content
from engine.poster import post_content


def main() -> None:
    """Entry point for the AI Influencer Factory pipeline."""
    generated = generate_content()
    post_content(generated)


if __name__ == "__main__":
    main()
