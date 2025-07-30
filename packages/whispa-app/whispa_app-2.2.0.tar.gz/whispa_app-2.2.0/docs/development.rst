Development Guide
================

This guide is for developers who want to contribute to Whispa App.

Setting Up Development Environment
-------------------------------

1. Clone the Repository
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    git clone https://github.com/yourusername/whispa-app.git
    cd whispa-app

2. Create Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows

3. Install Dependencies
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    pip install -r requirements-dev.txt

Project Structure
---------------

.. code-block:: text

    whispa-app/
    ├── docs/                   # Documentation
    ├── src/                    # Source code
    │   └── whispa_app/
    │       ├── ui/            # UI components
    │       ├── __init__.py
    │       ├── main.py        # Main application
    │       ├── transcription.py
    │       ├── translation.py
    │       └── utils.py
    ├── tests/                 # Test files
    ├── assets/                # Icons and resources
    ├── installer/             # Windows installer
    ├── requirements.txt       # Production dependencies
    └── requirements-dev.txt   # Development dependencies

Development Workflow
-----------------

1. Create Feature Branch
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    git checkout -b feature/your-feature-name

2. Make Changes
~~~~~~~~~~~~

- Follow PEP 8 style guide
- Add docstrings to new functions/classes
- Update tests as needed

3. Run Tests
~~~~~~~~~~

.. code-block:: bash

    pytest tests/

4. Build Documentation
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    cd docs
    make html

5. Submit Pull Request
~~~~~~~~~~~~~~~~~~~

1. Push changes to your fork
2. Create PR against main branch
3. Wait for review

Building the Application
---------------------

Windows Executable
~~~~~~~~~~~~~~~

.. code-block:: bash

    pyinstaller --name whispa-app --windowed --icon=assets/icon.ico run.py

Windows Installer
~~~~~~~~~~~~~~

1. Install Inno Setup
2. Run installer script:

.. code-block:: bash

    iscc installer/setup.iss

Python Package
~~~~~~~~~~~~

.. code-block:: bash

    python -m build

Release Process
-------------

1. Update Version
~~~~~~~~~~~~~~

- Update version in:
  - src/whispa_app/main.py
  - installer/setup.iss
  - docs/conf.py

2. Update Changelog
~~~~~~~~~~~~~~~~

Add entry to CHANGELOG.md:

.. code-block:: markdown

    ## [2.2.0] - YYYY-MM-DD
    ### Added
    - New feature 1
    - New feature 2
    
    ### Changed
    - Change 1
    - Change 2
    
    ### Fixed
    - Bug fix 1
    - Bug fix 2

3. Create Release
~~~~~~~~~~~~~~

.. code-block:: bash

    git tag v2.2.0
    git push origin v2.2.0

4. GitHub Actions
~~~~~~~~~~~~~~

The workflow will:
- Run tests
- Build executables
- Create GitHub release
- Publish to PyPI

Code Style Guide
--------------

General Guidelines
~~~~~~~~~~~~~~~

- Follow PEP 8
- Use type hints
- Write docstrings (Google style)
- Keep functions focused
- Use meaningful names

Example:

.. code-block:: python

    def process_audio(
        file_path: str,
        model_size: str = "small",
        vram_limit: int = 6
    ) -> str:
        """Process audio file and return transcription.
        
        Args:
            file_path: Path to audio file
            model_size: Whisper model size
            vram_limit: GPU memory limit in GB
            
        Returns:
            Transcribed text
            
        Raises:
            FileNotFoundError: If audio file doesn't exist
            ValueError: If model_size is invalid
        """
        # Implementation

Documentation
-----------

- Use RST format
- Include examples
- Document exceptions
- Keep API reference updated
- Add diagrams where helpful

Testing
------

- Write unit tests
- Use pytest fixtures
- Mock external services
- Test edge cases
- Maintain 80%+ coverage

Continuous Integration
-------------------

GitHub Actions handles:

- Running tests
- Building packages
- Creating releases
- Publishing documentation
- Code quality checks

Contributing Guidelines
--------------------

1. Check existing issues
2. Discuss big changes first
3. Follow code style
4. Add tests
5. Update docs
6. Keep PRs focused 