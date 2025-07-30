# Contributing

We welcome contributions to this project! Please follow these guidelines:

## How to Contribute

1. **Fork the repository:** Create your own fork of the project on GitHub.

2. **Create a branch:** Make your changes in a new git branch, based off the `develop` branch:

    ```bash
    # Ensure you are on the develop branch and up-to-date
    git checkout develop
    git pull origin develop

    # Create your feature branch
    git checkout -b my-fix-branch
    ```

3. **Set up the development environment:** Run this step from the root of the repository. This will create a virtual environment (`.venv`) using `uv` and install all necessary dependencies, including development tools.

    ```bash
    # Run from the project root directory
    make bootstrap
    ```

4. **Activate the virtual environment:** Before running any project commands, activate the environment:

    ```bash
    source .venv/bin/activate
    ```

5. **Make changes:** Implement your fix or feature.

6. **Test your changes:** Run the test suite using `pytest`. You can also use the VS Code task "Run Test Suite". Tests are automatically run via GitHub Actions (`tests.yml`) when you open a pull request.

    ```bash
    make test
    ```

7. **Check code style:** Ensure your code adheres to the project's style guidelines by running the linters (`ruff` and `pylint`). You can also use the VS Code task "Run Linter". Linting is automatically checked via GitHub Actions (`tests.yml`) when you open a pull request.

    ```bash
    make lint
    ```

8. **Commit your changes:** Commit your changes with a clear commit message following conventional commit standards if possible:

    ```bash
    git commit -am 'feat: Add some feature'
    # or
    git commit -am 'fix: Resolve issue #123'
    ```

9. **Push to the branch:** Push your changes to your fork:

    ```bash
    git push origin my-fix-branch
    ```

10. **Submit a pull request:**

    Open a pull request from your fork's branch to the `develop` branch of the main project repository. Ensure the pull request description clearly explains the changes and references any relevant issues.

    > NOTE: The PR *must* be based off `develop`. The `main` branch is our stable branch and
    `develop` is for fixes and new features. Any pull request based on `main` will be auto-rejected
    by our CI/CD pipeline.

### Details about the CI/CD Pipeline

There are two Rulesets that are enabled:

#### Main branch deletion protection

```plaintext
Main Branch
ID: 5272788
Source: ksylvan/python-project-template (Repository)
Enforcement: Active
You can bypass: never

Bypass List
This ruleset cannot be bypassed

Conditions
- ref_name: [exclude: []] [include: [refs/heads/main]]

Rules
- deletion
- non_fast_forward
- required_status_checks: [do_not_enforce_on_create: false] [required_status_checks: [map[context:tests (3.11) integration_id:15368] map[context:tests (3.12) integration_id:15368] map[context:Check PR Source Branch integration_id:15368]]] [strict_required_status_checks_policy: true]

```

#### Merge into Develop

```plaintext

Merge Into Develop
ID: 5259640
Source: ksylvan/fabric-mcp (Repository)
Enforcement: Active
You can bypass: never

Bypass List
This ruleset cannot be bypassed

Conditions
- ref_name: [exclude: []] [include: [refs/heads/develop]]

Rules
- deletion
- non_fast_forward
- pull_request: [allowed_merge_methods: [merge squash rebase]] [automatic_copilot_code_review_enabled: false] [dismiss_stale_reviews_on_push: false] [require_code_owner_review: false] [require_last_push_approval: false] [required_approving_review_count: 0] [required_review_thread_resolution: true]
- required_status_checks: [do_not_enforce_on_create: false] [required_status_checks: [map[context:tests (3.11) integration_id:15368] map[context:tests (3.12) integration_id:15368]]] [strict_required_status_checks_policy: false]
```

## Code Style

Please follow the existing code style. We use `ruff` for formatting and quick linting, and `pylint` for more thorough static analysis. We also use `pyright` with `strict` level type checking.

Configuration can be found in `pyproject.toml`.

Ensure you run the linters before committing (see step 7 above).

Also, the test suite implements code coverage and is set up to fail with a 90% threshold.

## Fast MCP inspector

You can run the `fastmcp` inspector to test the server:

```bash
fastmcp dev ./fabric_mcp/server_stdio.py
2025-05-03 21:46:21,457 - server_stdio - INFO - Starting server with log level DEBUG
Starting MCP inspector...
⚙️ Proxy server listening on port 6277
🔍 MCP Inspector is up and running at http://127.0.0.1:6274 🚀
```

Then you can browse to the localhost port and interact with the MCP server.

## Reporting Bugs

If you find a bug, please open an issue on GitHub. Provide:

* Detailed steps to reproduce the bug.
* The version of the tool you are using.
* Your operating system and Python version.
* Any relevant error messages or logs.

## GitHub Actions

We use GitHub Actions (`.github/workflows/`) to automate testing (`tests.yml`) and publishing (`publish.yml`).

Pull requests must pass the checks defined in `tests.yml` before they can be merged.

Thank you for contributing!
