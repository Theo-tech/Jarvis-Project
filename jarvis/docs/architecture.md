jarvis-project/
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE.md
├── .venv/                    # (gitignored) virtualenv local
├── docs/
│   ├── architecture.md
│   └── usage.md
├── scripts/
│   └── run_assistant.py
├── jarvis/                   # package principal
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── assistant.py
│   │   ├── manager.py
│   │   └── handlers/
│   │       ├── __init__.py
│   │       ├── command_handler.py
│   │       └── nlp_handler.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_client.py
│   │   └── storage.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logging.py
│   │   └── config.py
│   └── cli.py
├── tests/
│   ├── test_assistant.py
│   └── test_integration.py
├── examples/
│   └── sample_session.txt
├── configs/
│   └── default.yaml
├── .gitignore
├── .env.example
├── pyproject.toml            # ou setup.cfg + setup.py
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── LICENSE
└── main.py
