# Contributing to python-agent-template

<!-- Portions inspired by Microsoft's agent-framework CONTRIBUTING.md (MIT): https://github.com/microsoft/agent-framework/blob/main/CONTRIBUTING.md -->

Thank you for your interest in contributing to the `python-agent-template` project! We welcome contributions from the community to help improve and enhance this project. You can contribute in various ways, including reporting issues, suggesting new features and improvements, or submitting code changes through pull requests.



## Community guidelines

To keep the project safe and welcoming:

- Please review our [Code of Conduct](CODE_OF_CONDUCT.md) before you start interacting with the community.

- For security-sensitive findings, follow the [Security Policy](SECURITY.md) and do not open public issues or pull requests.

## Reporting Issues and Suggesting new Features/Improvements

Your feedback is invaluable to us. If you encounter any bugs or have ideas for new features or improvements, please open an issue on our GitHub repository.

### How to Report an Issue

All issues should be reported on the [GitHub Issues page](https://github.com/pmalarme/python-agent-template/issues).

Before submitting a new issue, please check the existing issues to see if your concern/proposal has already been addressed. If you find a similar issue, feel free to add any additional information or context that may help us resolve it. You can also upvote existing issues by adding a 👍 reaction.

There are several templates available to help you report issues effectively. Please choose the appropriate template based on the nature of your issue.

As a general guideline, be detailed and specific when describing the issue, the improvement, or the new feature you are proposing. Fill out all relevant sections of the template to provide us with the necessary context.

>[!IMPORTANT]
> Please do not report security vulnerabilities through GitHub Issues. Instead, refer to our [Security Policy](SECURITY.md) for instructions on how to report security issues responsibly.
>
> If you want to get in touch for other reasons, please use the [Discussions](https://github.com/pmalarme/python-agent-template/discussions) section of our repository. You can always discuss ideas, ask questions, or seek help there. This is a great way to engage with the community and get feedback on your thoughts before submitting formal issues or pull requests.

### Writing a Good Bug Report

To accelerate the resolution of bugs, please do not hesitate to include as much relevant information as possible, including:

- A clear description of the problem.
- The complete list of steps to reproduce the issue.
- The expected and actual results.
- Any relevant logs or error messages.
- The version of the template you are using.
- Your operating system and environment details.

## Contributing Code Changes

Code contributions are more than welcome! The maintainers of this project appreciate your efforts to help improve the codebase. They will review your pull requests and provide feedback as needed. If your changes are accepted, they will merged them into the main codebase.

These are the do and don'ts for contributing code changes:

### Do

- **DO** follow the [coding standards and conventions](CODING_STANDARDS.md) used in this project
- **DO** setup the pre-commit hooks as described in the [Development Setup Guide](DEVELOPMENT.md)
- **DO** read the [development guidelines](DEVELOPMENT.md) to understand how to set up your development environment and how this template works.
- **DO** write tests for any new features or bug fixes you implement.
- **DO** write clear and concise commit messages prefixing them with the relevant type:
  - `feat:` A new feature
  - `fix:` A bug fix
  - `docs:` Documentation changes
  - `style:` Code style changes (formatting, missing semi-colons, etc.)
  - `refactor:` Code refactoring without changing functionality
  - `test:` Adding or updating tests
  - `chore:` Maintenance tasks (build process, dependencies, etc.)
- **DO** ensure that all checks and tests pass before submitting your pull request.
- **DO** provide a clear description of the changes you have made in your pull request.
- **DO** do state your intentions to work on an issue by leaving a comment on the issue before you start working on it. This helps avoid duplicate efforts.
- **DO** keep your fork and branch up to date with the main repository to avoid merge conflicts.
- **DO** be respectful and considerate in all your interactions with the community.
- **DO** share your contributions and improvements with your network to help grow the community.

### Don't

- **DON'T** submit large, monolithic pull requests that are difficult to review. Break your changes into smaller, manageable pieces.
- **DON'T** include unrelated changes in your pull request. Keep your changes focused on a single issue or feature.
- **DON'T** submit code that does not adhere to the project's coding standards and conventions.
- **DON'T** submit PR's with change in the licensing files or header without prior discussion with the maintainers.
- **DON'T** be discouraged if your pull request is not accepted immediately. The maintainers may request changes or provide feedback to help improve your contribution.
- **DON'T** submit pull requests without an issue. If there is no issue, please create one first to discuss your proposed changes.
- **DON'T** include proprietary or third-party code in your pull request without proper authorization and without prior discussion with the maintainers.
- **DON'T** don't push code you didn't write yourself. Always ensure you have the right to submit the code you are contributing.

### Proposed Workflow for Contributing Code Changes

1. Create a new issue or ask to be assigned to an existing issue
    - Even for trivial changes, it's best to have an issue to track the work.
    - If you want to work on an existing issue, wait to have it assigned to you before starting work.
2. Fork the repository and clone it to your local machine.

3. Create a new branch for your changes using the conventions below (use them even on forks):
    - `feature/<short-summary>` for new features
    - `bugfix/<short-summary>` for bug fixes
    - `hotfix/<short-summary>` for urgent fixes to `main`
    - `docs/<short-summary>` for documentation-only changes
    - `chore/<short-summary>` for maintenance tasks

      ```bash
      git checkout -b feature/my-change
      ```

4. Make your changes, ensuring you follow the coding standards and conventions.
5. Write tests for your changes.
6. Run the tests to ensure everything is working correctly.
7. Commit your changes with a clear and concise commit message prefixed with the relevant type.
8. Push your changes to your forked repository.
9. Create a pull request against the `python-agent-template` repository `main` branch.
    - Provide a clear description of the changes you have made and reference the relevant issue.
10. Ensure that all the checks and tests pass. If there are any issues, address them promptly.
11. Engage in the review process by responding to comments and making any requested changes.
12. Once your pull request is approved, it will be merged into the main codebase.

>[!NOTE]
> For direct contributions to the repository by maintainers, the same guidelines apply. Maintainers should follow these guidelines when creating branches in `python-agent-template` repository:
> - Create a `feature/` branch for new features.
> - Create a `bugfix/` branch for bug fixes.
> - Create a `hotfix/` branch for urgent fixes to the main branch.
> - Create a `docs/` branch for documentation changes only.
> - Create a `chore/` branch for maintenance tasks.
> This helps maintain a clear and organized workflow for all contributions.
