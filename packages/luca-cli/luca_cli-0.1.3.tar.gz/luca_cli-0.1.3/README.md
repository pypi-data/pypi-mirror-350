# LUCA CLI Client

## Overview

The LUCA CLI Client is a command-line interface for your LUCA assistant.

It allows you to interact with an assistant that lives in your terminal.
This is a non-intrusive user experience, that means you still have complete control over your terminal.
But the assistant is always a command away.

## Capabilities

We have designed the system to be able to:
 - Retrieve and search relevant research papers from ArXiv.
 - Retrieve experiments logged in a Weights & Biases project.
 - Generate and execute Python and bash commands.

With these capabilities, you can use the assistant to:
- Generate reports that theorize and summarize your research experiments.
- Generate a project plan to tackle a new research problem.
- Brainstorm, ideate generate new hypotheses based on your current experiments.

## Installation

```bash
pip install luca-cli
```

## Usage

```bash
luca --help
```
As soon as you pip install the package, the recommended first command to run is:
```bash
luca init
```
This will initialize the assistant and create a knowledge base.
This knowledge base will be updated with new information as you use the assistant.

After the initialization, you can start interacting with the assistant by just typing your prompt:
```bash
luca "Research papers on reinforcement learning."
```

We plan to significantly expand the set of capabilities of the assistant with each new release.
Please provide your unfiltered thoughts, suggestions and feedback to us by using the `luca feedback` command.

```bash
luca feedback "I love the assistant!"
```

Cheers,\
The LUCA team
