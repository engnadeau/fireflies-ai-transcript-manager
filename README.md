# Fireflies AI Transcript Manager

![Notetaking](cover.jpg)

## Description

`Fireflies AI Transcript Manager` is a tool designed to automate the process of managing meeting transcripts from Fireflies.ai.
It simplifies the workflow by providing functionalities to fetch, save, and organize transcripts efficiently, enhancing the overall experience of handling meeting documentation.

## Features

- **Fetch Transcripts**: Automatically retrieve transcripts from your Fireflies.ai account.
- **Save Transcripts Locally**: Transcripts are saved in a structured format within a designated folder for easy access and organization.
- **Logging**: Detailed logging of operations, making it easier to track the process and troubleshoot any issues.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/engnadeau/fireflies-ai-transcript-manager.git
   ```

2. Navigate to the cloned repository.
3. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

## Usage

Set the `FIREFLIES_AI_API_TOKEN` environment variable with your [Fireflies.ai API token](https://app.fireflies.ai/integrations/custom/fireflies).

To fetch transcripts, run:

```bash
make fetch
```

Transcripts will be saved in the `transcripts` folder within the project directory.

## Development Commands

- **Formatting**:

    ```bash
    make format
    ```

- **Linting**:

    ```bash
    make lint
    ```

---

Photo by <a href="https://unsplash.com/@dtravisphd?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">David Travis</a> on <a href="https://unsplash.com/photos/brown-fountain-pen-on-notebook-5bYxXawHOQg?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>
