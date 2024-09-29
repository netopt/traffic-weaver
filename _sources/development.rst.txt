Development
============

Install dependencies.

.. code-block:: shell

    make build-requirements
    make build

Enable commit hooks.

.. code-block:: shell

    npm install -g @commitlint/cli @commitlint/config-conventional @commitlint/cz-commitlint
    npm install -g commitizen
    pre-commit install --hook-type pre-commit
    pre-commit install --hook-type commit-msg





