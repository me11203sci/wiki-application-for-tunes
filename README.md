# Wiki Application For Tunes

`waft` facilitates the association of files in the [Moving Picture Experts Group Audio Layer III (MP3)](https://ossrs.io/lts/zh-cn/assets/files/ISO_IEC_13818-3-MP3-1997-8bbd47f7cd4e0325f23b9473f6932fa1.pdf) format with metadata according to the [ID3](https://id3.org/id3v2.3.0) standard.

## Installation
Todo. May look at either bundler like Nuitka or just having user download repository.

## Usage
Todo.

## Contribution Guide
Todo.

## Core Development Team
**Melesio Albavera - User Interface Design Lead**
**Luke Dennison - Backend Development Lead**
**Eli Wetzel - Applicaiton Logic Lead**
**ChatGPT - Emotional Support Expert (External Consultant)**

> [!NOTE]
> All H4 headers will not be present in final version of this document, as they are scratch notes for the core team, but will hopefully be properly integrated into the rest of the document **before** the minimum viable product release.

#### Technological Stack
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

#### Standards
Coding standards: pep 8, black
Documentation: https://numpydoc.readthedocs.io/en/latest/format.html#examples, https://peps.python.org/pep-0257/
Commit Standards: https://cbea.ms/git-commit/

#### Database Architecture (Entity Relations)
Mermaid diagram (Dennison Todo)

#### Application Logic
TEA - https://guide.elm-lang.org/architecture/

