import random
import sys
from pathlib import Path

import fire
import uvicorn
from dotenv import find_dotenv, load_dotenv

from .builder import AGENTS_DIR, build_agent
from .models import SUPPORTED_EXTENSIONS, PlaybookSpec


def _load_playbooks() -> list[PlaybookSpec]:
    env_file = find_dotenv(usecwd=True)
    load_dotenv(env_file)

    playbook_specs: list[PlaybookSpec] = []

    spec_files: list[Path] = []
    for ext in SUPPORTED_EXTENSIONS:
        spec_files.extend(AGENTS_DIR.glob(f"*{ext}"))

    for spec_file in spec_files:
        try:
            playbook_spec = PlaybookSpec.from_yaml(spec_file)
            playbook_specs.append(playbook_spec)
        except Exception as e:
            print(f"Error loading playbook spec {spec_file}: {e}", file=sys.stderr)

    return playbook_specs


def run(name: str | None = None, host: str = "127.0.0.1", port: int = 8000) -> None:
    playbooks = _load_playbooks()
    if not playbooks:
        print("No playbook found.", file=sys.stderr)
        raise SystemExit(1)

    if not name:
        playbook = random.choice(playbooks)
    else:
        playbook = next((spec for spec in playbooks if spec.name == name), None)
        if not playbook:
            print(f"Playbook not found: {name}", file=sys.stderr)
            print(
                f"Available: {', '.join(sorted(spec.name for spec in playbooks))}",
                file=sys.stderr,
            )
            raise SystemExit(1)

    agent = build_agent(playbook)
    app = agent.to_web()

    print(f"Serving {playbook.name!r} at http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)


def main() -> None:
    fire.Fire(run)


if __name__ == "__main__":
    main()
