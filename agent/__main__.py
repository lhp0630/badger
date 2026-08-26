import random
import sys
from pathlib import Path

import fire
import uvicorn
from dotenv import find_dotenv, load_dotenv

from . import PlaybookSpec, make_workflow_agent

SKILLS_DIR = Path(".agents")


def _load_playbooks():
    env_file = find_dotenv(usecwd=True)
    load_dotenv(env_file)

    file_paths: list[Path] = []

    for ext in [".yml", ".yaml"]:
        file_paths.extend(SKILLS_DIR.glob(f"*{ext}"))

    for path in file_paths:
        try:
            yield PlaybookSpec.from_yaml(path)
        except Exception as e:
            print(f"Error loading playbook spec {path}: {e}", file=sys.stderr)


def startup_web(name: str | None = None, host: str = "127.0.0.1", port: int = 8000):
    playbooks = [*_load_playbooks()]
    if not playbooks:
        print("No playbook found.", file=sys.stderr)
        raise SystemExit(1)

    selected_playbook = (
        random.choice(playbooks)
        if not name
        else next(spec for spec in playbooks if spec.name == name)
    )

    agent = make_workflow_agent(selected_playbook)
    app = agent.to_web()

    print(f"Serving {selected_playbook.name!r} at http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)


def main() -> None:
    fire.Fire(startup_web)


if __name__ == "__main__":
    main()
