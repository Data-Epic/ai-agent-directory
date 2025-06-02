https://www.youtube.com/watch?v=DBlmF91Accg
https://blog.devops.dev/level-up-your-development-workflow-with-pre-commit-and-github-actions-23b13f5efd6e


## Folde Structure
.
├── Dockerfile
├── Readme.md
├── __init__.py
├── __pycache__
│   └── __init__.cpython-39.pyc
├── alembic
│   ├── README
│   ├── __pycache__
│   │   └── env.cpython-39.pyc
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       ├── 0bf8ae238247_add_default_0_to_trending.py
│       ├── 210296102845_update.py
│       ├── 48fcc7f42a09_update.py
│       ├── 9fc7de7517f6_change_trending_to_boolean.py
│       └── __pycache__
│           ├── 0bf8ae238247_add_default_0_to_trending.cpython-39.pyc
│           ├── 210296102845_update.cpython-39.pyc
│           ├── 48fcc7f42a09_update.cpython-39.pyc
│           └── 9fc7de7517f6_change_trending_to_boolean.cpython-39.pyc
├── alembic.ini
├── app
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-39.pyc
│   │   └── app.cpython-39.pyc
│   ├── api
│   │   ├── ── __init__.py
│   │   ├── __pycache__
│   │   │   └── __init__.cpython-39.pyc
│   │   ├── route
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-39.pyc
│   │   │   │   ├── agent.cpython-39.pyc
│   │   │   │   ├── highlight.cpython-39.pyc
│   │   │   │   ├── rating.cpython-39.pyc
│   │   │   │   ├── review.cpython-39.pyc
│   │   │   │   └── user.cpython-39.pyc
│   │   │   ├── agent.py
│   │   │   ├── highlight.py
│   │   │   ├── review.py
│   │   │   └── user.py
│   │   └── utils
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       │   ├── __init__.cpython-39.pyc
│   │       │   ├── create_admin.cpython-39.pyc
│   │       │   └── create_initial_admin.cpython-39.pyc
│   │       └── create_initial_admin.py
│   ├
│   ├── auth
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-39.pyc
│   │   │   ├── auth.cpython-39.pyc
│   │   │   ├── bearer.cpython-39.pyc
│   │   │   └── dependency.cpython-39.pyc
│   │   ├── auth.py
│   │   ├── bearer.py
│   │   └── dependency.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-39.pyc
│   │   │   └── database.cpython-39.pyc
│   │   ├── database.py
│   │   └── models
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       │   ├── __init__.cpython-39.pyc
│   │       │   ├── agent.cpython-39.pyc
│   │       │   ├── highlight.cpython-39.pyc
│   │       │   ├── rating.cpython-39.pyc
│   │       │   ├── review.cpython-39.pyc
│   │       │   └── user.cpython-39.pyc
│   │       ├── agent.py
│   │       ├── highlight.py
│   │       ├── review.py
│   │       └── user.py
│   ├── schema
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-39.pyc
│   │   │   ├── agent.cpython-39.pyc
│   │   │   ├── highlight.cpython-39.pyc
│   │   │   ├── rating.cpython-39.pyc
│   │   │   ├── review.cpython-39.pyc
│   │   │   └── user.cpython-39.pyc
│   │   ├── agent.py
│   │   ├── highlight.py
│   │   ├── review.py
│   │   └── user.py
│   └── tests
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-39.pyc
│       │   ├── test_db.cpython-39-pytest-8.3.5.pyc
│       │   ├── test_dummy.cpython-39-pytest-8.3.5.pyc
│       │   ├── test_models.cpython-39-pytest-8.3.5.pyc
│       │   └── test_routes.cpython-39-pytest-8.3.5.pyc
│       ├── test_dummy.py
│       └── test_models.py
├── docker-compose.yml
├── poetry.lock
├── pyproject.toml
└── pytest.ini
