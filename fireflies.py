import json
import logging
import os
from datetime import datetime
from pathlib import Path

import fire
import requests
from slugify import slugify


class FirefliesTranscriptManager:
    def __init__(self):
        self.api_token = os.getenv("FIREFLIES_AI_API_TOKEN")
        if not self.api_token:
            raise ValueError(
                "Please set the FIREFLIES_AI_API_TOKEN environment variable."
            )
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

    def fetch(self):
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

        if response.status_code == 200:
            transcripts = response.json().get("data", {}).get("transcripts", [])
            logging.info(f"Fetched {len(transcripts)} transcripts")
            self._save_transcripts(transcripts)
        else:
            logging.error(
                f"Failed to fetch data: {response.status_code} {response.text}"
            )

    def _save_transcripts(self, transcripts):
        folder = Path("transcripts")
        folder.mkdir(parents=True, exist_ok=True)

        logging.info(f"Saving transcripts to {folder}...")
        for transcript in transcripts:
            date_str = datetime.fromtimestamp(int(transcript["date"]) / 1000).strftime(
                "%Y-%m-%d"
            )
            title = slugify(transcript["title"])
            filename = folder / f"{date_str}_{title}.json"

            logging.info(f"Saving transcript: {filename}")
            with open(filename, "w") as file:
                json.dump(transcript, file, indent=4)
            logging.info(f"Transcript saved: {filename}")


def main():
    fire.Fire(FirefliesTranscriptManager)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
