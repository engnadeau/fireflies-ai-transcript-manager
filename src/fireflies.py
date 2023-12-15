import concurrent.futures
import json
import logging
from datetime import datetime
from pathlib import Path

import fire
import requests
from slugify import slugify

from src.config import settings


class FirefliesTranscriptManager:
    def __init__(self):
        self.api_token = settings.API_TOKEN
        if not self.api_token:
            raise ValueError("Please set the API_TOKEN config variable.")
        self.url = "https://api.fireflies.ai/graphql"
        self.headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Connection": "keep-alive",
            "DNT": "1",
            "Origin": "https://api.fireflies.ai",
            "Authorization": f"Bearer {self.api_token}",
        }
        self.folder = Path(settings.OUTPUT_DIR)

    def fetch(self):
        # define the query and make the request
        query = {
            "query": """
                {
                    transcripts {
                        id
                        title
                        date
                        sentences {
                            index
                            text
                            raw_text
                            start_time
                            end_time
                            speaker_id
                            speaker_name
                        }
                        host_email
                        organizer_email
                        user {
                            user_id
                            email
                            name
                            num_transcripts
                            recent_transcript
                            minutes_consumed
                            is_admin
                            integrations
                        }
                        fireflies_users
                        participants
                        transcript_url
                        audio_url
                        duration
                    }
                }
            """
        }
        response = requests.post(self.url, headers=self.headers, json=query)

        # check if the request was successful
        if response.status_code == 200:
            transcripts = response.json().get("data", {}).get("transcripts", [])
            logging.info(f"Fetched {len(transcripts)} transcripts")
            self._save_transcripts(transcripts)
        else:
            logging.error(
                f"Failed to fetch data: {response.status_code} {response.text}"
            )

    def _save_transcripts(self, transcripts):
        # create the output folder if it doesn't exist
        self.folder.mkdir(parents=True, exist_ok=True)

        # save each transcript to a file
        logging.info(f"Saving transcripts to {self.folder}...")
        for transcript in transcripts:
            date_str = datetime.fromtimestamp(int(transcript["date"]) / 1000).strftime(
                "%Y-%m-%d"
            )
            title = slugify(transcript["title"])
            transcript_id = transcript["id"]
            # include transcript_id to ensure uniqueness
            filename = self.folder / f"{date_str}_{title}_{transcript_id}.json"

            logging.info(f"Saving transcript: {filename}")
            with open(filename, "w") as file:
                json.dump(transcript, file, indent=4)
            logging.info(f"Transcript saved: {filename}")

    def delete(self):
        # check if the output folder exists
        if not self.folder.exists():
            logging.error(f"No local transcripts found in {self.folder}")
            return

        # get the list of transcripts
        transcripts = list(self.folder.glob("*.json"))
        logging.info(f"Deleting {len(transcripts)} transcripts...")

        # delete each transcript in the cloud in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for transcript_file in transcripts:
                with open(transcript_file, "r") as file:
                    transcript = json.load(file)
                    transcript_id = transcript.get("id")
                    if transcript_id:
                        logging.info(
                            f"Queueing deletion for transcript {transcript_file.name} with ID {transcript_id}"
                        )
                        futures.append(
                            executor.submit(self._delete_transcript, transcript_id)
                        )
                    else:
                        logging.error(f"Failed to queue deletion: {transcript_file}")

            for future in concurrent.futures.as_completed(futures):
                future.result()

    def _delete_transcript(self, transcript_id):
        # define the query and make the request
        mutation = {
            "query": """
                mutation deleteTranscript($id: String!){
                  deleteTranscript(id: $id){
                    id
                  }
                }
            """,
            "variables": {"id": transcript_id},
        }
        logging.info(f"Deleting transcript with ID: {transcript_id}")
        response = requests.post(self.url, headers=self.headers, json=mutation)

        # check if the request was successful
        if response.status_code == 200:
            logging.info(f"Deleted transcript with ID: {transcript_id}")
        else:
            logging.error(
                f"Failed to delete transcript: {transcript_id} - {response.status_code} {response.text}"
            )


def main():
    fire.Fire(FirefliesTranscriptManager)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
