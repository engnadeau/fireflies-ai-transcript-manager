# Fireflies AI Transcript Manager

![Notetaking](cover.jpg)

## Description

`Fireflies AI Transcript Manager` is a versatile tool designed to automate the management of meeting transcripts from Fireflies.ai.
It streamlines the workflow by offering functionalities to fetch, save, delete, and organize transcripts efficiently, thereby enhancing the experience of handling meeting documentation.

## Features

- **Fetch Transcripts**: Automatically retrieve transcripts from your Fireflies.ai account.
- **Save Transcripts Locally**: Save transcripts in a structured format within a designated folder for easy access and organization.
- **Delete Transcripts**: Efficiently delete transcripts from the cloud using local transcript data, utilizing parallel processing for faster execution.
- **Parallel Processing**: Leverages concurrent threads for rapid deletion of multiple transcripts, enhancing performance and efficiency.
- **Logging**: Detailed logging of all operations, providing insights into the process and aiding in troubleshooting.

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

- **Fetching Transcripts**:

   ```bash
   make fetch
   ```

   Transcripts will be saved in the `transcripts` folder within the project directory.

- **Deleting Transcripts**:

   ```bash
   make delete
   ```

   This will delete transcripts from the cloud that are already downloaded locally.

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

Photo by [David Travis](https://unsplash.com/@dtravisphd?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash) on [Unsplash](https://unsplash.com/photos/brown-fountain-pen-on-notebook-5bYxXawHOQg?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash)
