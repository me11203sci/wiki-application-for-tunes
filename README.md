# Wiki Application For Tunes

[comment]: # (Todo. Add badges, particularlly build status, docs coverage and test coverage.)

`waft` facilitates the association of files in the [MP3](https://ossrs.io/lts/zh-cn/assets/files/ISO_IEC_13818-3-MP3-1997-8bbd47f7cd4e0325f23b9473f6932fa1.pdf) format with metadata according to the [ID3 standard](https://id3.org/id3v2.3.0).
## Installation
Todo. May look having user download repository or otherwise we may also opt to host the application as a website.
## Usage
Todo.
## Implementation Details
Todo. This section should contain an explanation of both the Entity Relation diagram of our database, as well as the implementation of the Elm design Pattern for our front end logic.
## Contribution Guide
In order to establish consistency among contributors and aid reviewers in evaluating contributions, below we detail standards to serve these ends.
### Developer Tool Chain Resources
It is imperative that a prospective contributor familiarize themselves with the tool chain and technological stack employed
during the development of this project. The proceeding is a list of these tools/frameworks/libraries, a brief commentary on
their usage in relation to this project, and links to their documentation:
- [Python](https://docs.python.org/3.13/): Python is a dynamic programming language with various advantages that make it a good choice for the development of our application, primarily its robust ecosystem of well maintained libraries. Additionally, most of the core team posses at least intermediate facility with it. While Python 3.14 is stable at the time of writing, [3.13](https://docs.python.org/3/whatsnew/3.13.html) was chosen as it is the first version to offer the ability to disable the [GIL](https://wiki.python.org/moin/GlobalInterpreterLock).
- [Mamba](https://mamba.readthedocs.io/en/latest/index.html): When attempting to develop in Python, it is important to keep package and library versions consistent across machines, for which [environment](https://docs.python.org/3/library/venv.html) managers are helpful.
    - [Textual](https://textual.textualize.io/): Textual is a Python framework that allows us to create a textual user interface using pre-made widget components, with great asynchronous support. Additionally, applications developed with Textual are rather readily converted into websites, furthering the accessibility of our application.
- [pudb](https://documen.tician.de/pudb/): A great and versatile step-by-step terminal debugger.
- [Black](https://black.readthedocs.io/en/stable/): Black is a code formatter that adheres to the Pythonic standard set out in [PEP 8](https://peps.python.org/pep-0008/).
- [mypy](https://mypy-lang.org/): `mypy` allows us to check for type consistency, letting us catch a whole swath of tricky runtime errors.
- [GitHub Actions](https://docs.github.com/en/actions): Actions workflows allow us to automate pull requests, code review tasks, deployments, documentation generation, etc. They are written in [YAML](https://yaml.org/).
- [MKDocs](https://www.mkdocs.org/): A static website generator that creates documentation from [markdown](https://www.markdownguide.org/) source files.
- [mkdocstrings](https://mkdocstrings.github.io/): An extension of MKDocs' capabilities, allowing us to collate inline documentation from Python source files directly.
### Opening an Issue
All features, enhancements, and bug reports **must** begin as a [Github Issue](https://docs.github.com/en/issues) submitted through our [Project Board](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects), in order to ensure that progress is visible and so and that work items can be prioritized and assigned efficiently. The steps for doing so as follows:
1. Begin by checking that a relevant issue does not already exist.
1. Make sure to provide it with a clear and descriptive title.
1. Select the appropriate label for your issue.
    1. Feature/enhancements **must** employ the User Story template.
1. Give it an appropriate priority level.
1. Estimate the number of story points according to the following table:
    |Points|Meaning|Example|
    |:----:|:-----:|:-----:|
    |1|Trivial change||
    |2|Small task||
    |3|Moderate|[#16](https://github.com/users/me11203sci/projects/3/views/1?pane=issue&itemId=134641535&issue=me11203sci%7Cwiki-application-for-tunes%7C16)|
    |5|Complex||
    |8|Large feature||
    |13+|Too large||
1. Assign yourself if you intend to work on the issue; otherwise leave it unassigned for triage.

After this, proceed to create a local working branch title composed of the your last name (lowercase) and a brief description of the issue you are working on (in [Pascal Case](https://wiki.c2.com/?PascalCase)), for example `dennison/SpotifyAPISearch`.
### Code Style Guide
Programming paradigm.

Adherence to design patterns.

Formatting using Black.

flake8. pylint.
### Commit Style Guide
For this project, we have attempted to follow the [guidance](https://cbea.ms/git-commit/) outlined by [cbeams](https://cbea.ms/author/cbeams/), which can be summarized in the following 7 rules:
1. Separate subject from body with a blank line.
2. Limit the subject line to 50 characters.
3. Capitalize the subject line.
4. Do not end the subject line with a period.
5. Use the [imperative mood](https://en.wikipedia.org/wiki/Imperative_mood) in the subject line.
6. Wrap the body at 72 characters.
7. Use the body to explain *what* the commit accomplishes and *why*.
### Pull Request Review
mypy.

Once code receives the manual approval of at least one other core team member, it is acceptable to merge onto the `master` branch.
## Core Development Team
**User Interface Design Lead:** [Melesio Albavera](https://github.com/me11203sci/)

**Back-End Development Lead:** [Luke Dennison](https://github.com/LukeDennison/)

**Application Logic Lead:** [Eli Wetzel](https://github.com/ejw255/)

**Emotional Support Expert (External Consultant):** [ChatGPT](https://chatgpt.com/)

> [!NOTE]
> All H6 headers will not be present in final version of this document, as they are scratch notes for the core team, but will hopefully be properly integrated into the rest of the document **before** the minimum viable product release.

###### Technological Stack
Database - MongoDB
Metadata - Spotify API
Audio Data Source - YouTube API
ytdlp - Obtaining Audio Data
Langauge - Python 3.13
    - id3tags: eye3D/music_tag
    - TUI: Textual
    - requests
Debug: pdb
Sound: pydub
CD/CI: Github Actions
Testing: pytest, hypothesis (?)
Code Style: https://github.com/whyjay17/Pyscent?tab=readme-ov-file#static-code-analysis-tools

###### Standards
Coding standards: pep 8, black
Documentation: https://numpydoc.readthedocs.io/en/latest/format.html#examples, https://peps.python.org/pep-0257/
Commit Standards: https://cbea.ms/git-commit/

###### Database Architecture (Entity Relations)
Mermaid diagram (Dennison Todo)

###### Application Logic
TEA - https://guide.elm-lang.org/architecture/
