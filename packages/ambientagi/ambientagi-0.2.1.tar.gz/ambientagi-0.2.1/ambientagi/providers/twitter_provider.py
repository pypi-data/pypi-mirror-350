import os
import time
from typing import Any, Dict, Optional

import requests  # type: ignore
from requests_oauthlib import OAuth1Session  # type: ignore

from ambientagi.config.settings import settings
from ambientagi.utils.http_client import HttpClient


class TwitterService:

    def __init__(self, agent: dict):
        """
        Initialize the TwitterService with an instance of AmbientAgentService.
        """
        default_headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        self.agent = agent
        self.agent_id = agent["agent_id"]
        self.client = HttpClient(
            base_url=settings.MAIN_API_BASE_URL,
            api_key=None,
            default_headers=default_headers,
        )
        self.twitter_handle = agent.get("twitter_handle", None)
        self.api_key = agent.get("api_key", None)
        self.api_secret = agent.get("api_secret", None)
        self.access_token = agent.get("access_token", None)
        self.access_secret = agent.get("access_secret", None)
        self.twitter = OAuth1Session(
            self.api_key, self.api_secret, self.access_token, self.access_secret
        )

    def update_twitter_credentials(
        self,
        twitter_handle: str,
        api_key: str,
        api_secret: str,
        access_token: str,
        access_secret: str,
    ):
        """
        Update the Twitter credentials for an existing Twitter-enabled agent.

        :param agent_id: ID of the agent.
        :param twitter_handle: Twitter handle for the agent.
        :param api_key: Twitter API key.
        :param api_secret: Twitter API secret.
        :param access_token: Twitter access token.
        :param access_secret: Twitter access secret.
        :return: Response from the API.
        """
        payload = {
            "twitter_handle": twitter_handle,
            "api_key": api_key,
            "api_secret": api_secret,
            "access_token": access_token,
            "access_secret": access_secret,
        }
        # Update instance variables
        self.twitter_handle = twitter_handle
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_secret = access_secret

        return self.client.post(
            f"/ambient-agents/{self.agent_id}/update",
            json=payload,
            headers={"Content-Type": "application/json"},
        )

    def reply_to_tweet(self, tweet_id, reply_text):
        url = "https://api.twitter.com/2/tweets"

        payload = {"text": reply_text, "reply": {"in_reply_to_tweet_id": tweet_id}}
        response = self.twitter.post(url, json=payload)
        if response.status_code != 201:
            raise Exception(f"Error: {response.status_code} {response.text}")

        return response.json()

    def post_quote_tweet(self, tweet_id, quote_text):
        url = "https://api.twitter.com/2/tweets"
        payload = {
            "text": quote_text.replace("**Tweet:**", ""),
            "quote_tweet_id": tweet_id,
        }
        response = self.twitter.post(url, json=payload)
        if response.status_code != 201:
            raise Exception(f"Error: {response.status_code} {response.text}")

        return response.json()

    def post_tweet(self, tweet_text):
        url = "https://api.twitter.com/2/tweets"
        payload = {"text": tweet_text}
        response = self.twitter.post(url, json=payload)
        if response.status_code != 201:
            raise Exception(f"Error: {response.status_code} {response.text}")

        return response.json()

    def upload_media(self, media_path):
        url = "https://upload.twitter.com/1.1/media/upload.json"

        # Open media file in binary mode
        with open(media_path, "rb") as media_file:
            files = {"media": media_file}
            response = self.twitter.post(url, files=files)

        return response.json()["media_id"]

    def upload_video(self, video_path):
        """
        Upload video using Twitter's chunked upload approach
        """
        # Twitter's upload endpoints
        MEDIA_ENDPOINT_URL = "https://upload.twitter.com/1.1/media/upload.json"

        # Get video size
        video_size = os.path.getsize(video_path)

        # INIT phase
        init_params = {
            "command": "INIT",
            "media_type": "video/mp4",
            "total_bytes": video_size,
            "media_category": "tweet_video",
        }

        init_response = self.twitter.post(MEDIA_ENDPOINT_URL, data=init_params)
        media_id = init_response.json()["media_id"]

        # APPEND phase
        segment_id = 0
        bytes_sent = 0
        with open(video_path, "rb") as video_file:
            while bytes_sent < video_size:
                chunk = video_file.read(4 * 1024 * 1024)  # 4MB chunks

                append_params = {
                    "command": "APPEND",
                    "media_id": media_id,
                    "segment_index": segment_id,
                }

                files = {"media": chunk}

                self.twitter.post(MEDIA_ENDPOINT_URL, data=append_params, files=files)

                segment_id += 1
                bytes_sent = video_file.tell()

                # Print progress
                print(f"Uploading chunk {segment_id}, {bytes_sent}/{video_size} bytes")

        # FINALIZE phase
        finalize_params = {"command": "FINALIZE", "media_id": media_id}

        finalize_response = self.twitter.post(MEDIA_ENDPOINT_URL, data=finalize_params)
        print(finalize_response.json())

        # Check processing status
        status_params = {"command": "STATUS", "media_id": media_id}

        processing = True
        while processing:
            status_response = self.twitter.get(MEDIA_ENDPOINT_URL, params=status_params)
            state = status_response.json().get("processing_info", {}).get("state")

            if state == "succeeded":
                processing = False
            elif state == "failed":
                raise Exception("Video processing failed")
            else:
                time.sleep(3)  # Wait 3 seconds before checking again

        return media_id

    def upload_media_from_url(self, image_url):
        url = "https://upload.twitter.com/1.1/media/upload.json"

        # Download image from URL
        response = requests.get(image_url)
        if response.status_code != 200:
            raise Exception(f"Error downloading image: {response.status_code}")

        # Upload image data directly
        files = {"media": response.content}
        upload_response = self.twitter.post(url, files=files)

        if upload_response.status_code != 200:
            raise Exception(f"Error uploading media: {upload_response.status_code}")

        return upload_response.json()["media_id"]

    def post_with_media(
        self, tweet_text, media_path=None, media_url=None, media_type=None
    ):

        if media_path:
            if media_type == "image":
                media_id = self.upload_media(media_path)
            elif media_type == "video":
                media_id = self.upload_video(media_path)
        elif media_url:
            media_id = self.upload_media_from_url(media_url)
        else:
            raise Exception("No media provided")

        url = "https://api.twitter.com/2/tweets"

        payload = {"text": tweet_text, "media": {"media_ids": [str(media_id)]}}
        response = self.twitter.post(url, json=payload)
        if response.status_code != 201:
            raise Exception(f"Error: {response.status_code} {response.text}")

        return response.json()

    def reply_with_media(self, tweet_id, media_id, tweet_text: Optional[str] = None):
        url = "https://api.twitter.com/2/tweets"

        payload: Dict[str, Any] = {
            "media": {"media_ids": [str(media_id)]},
            "reply": {"in_reply_to_tweet_id": tweet_id},
        }

        if tweet_text:
            payload["text"] = tweet_text  # Just assign normally

        response = self.twitter.post(url, json=payload)
        if response.status_code != 201:
            raise Exception(f"Error: {response.status_code} {response.text}")

        return response.json()

    def interactive_mode(self):
        """
        Start an interactive command session for Twitter interactions.
        Allows continuous input of commands until 'exit' is typed.
        """
        # First check if credentials are available
        # Check if credentials are available, if not try getting from env
        if not all(
            [
                self.api_key,
                self.api_secret,
                self.access_token,
                self.access_secret,
                self.twitter_handle,
            ]
        ):
            # Try getting from environment variables
            self.api_key = self.api_key or os.getenv("X_API_KEY")
            self.api_secret = self.api_secret or os.getenv("X_API_SECRET")
            self.access_token = self.access_token or os.getenv("X_ACCESS_TOKEN")
            self.access_secret = self.access_secret or os.getenv(
                "X_ACCESS_TOKEN_SECRET"
            )
            self.twitter_handle = self.twitter_handle or os.getenv("X_HANDLE")

            # If still missing credentials, prompt user
            if not all(
                [
                    self.api_key,
                    self.api_secret,
                    self.access_token,
                    self.access_secret,
                    self.twitter_handle,
                ]
            ):
                print("X credentials not found. Please provide them:")
                self.twitter_handle = self.twitter_handle or input("X handle: ")
                self.api_key = self.api_key or input("API key: ")
                self.api_secret = self.api_secret or input("API secret: ")
                self.access_token = self.access_token or input("Access token: ")
                self.access_secret = self.access_secret or input(
                    "Access token secret: "
                )

                # Update credentials
                self.update_twitter_credentials(
                    self.twitter_handle,
                    self.api_key,
                    self.api_secret,
                    self.access_token,
                    self.access_secret,
                )

        print(f"\nX Interactive Mode - Logged in as {self.twitter_handle}")
        print("Available commands:")
        print(
            "  post <text> | [media_path] [media_type]    - Post a tweet with optional media"
        )
        print(
            "  post <text> | [media_url]                  - Post a tweet with media from URL"
        )
        print(
            "  reply <tweet_id> <text> | [media_info]     - Reply to a tweet with optional media"
        )
        print("  exit                                       - Exit interactive mode")
        print("\nExample commands:")
        print("  post Hello World!")
        print("  post Check out this image! | photo.jpg image")
        print("  post New video! | video.mp4 video")
        print("  reply 123456789 Thanks! | reaction.gif")
        print("\n")

        while True:
            try:
                # Get command input
                command = input("X > ").strip()

                # Check for exit command
                if command.lower() == "exit":
                    print("Exiting X interactive mode...")
                    break

                if not command:
                    continue

                # Parse command
                parts = command.split(" ", 1)
                if len(parts) < 2:
                    print(
                        "Error: Invalid command format. Must include action and content."
                    )
                    continue

                action = parts[0].lower()
                content = parts[1]

                # Handle different commands
                if action == "post":
                    # Check if content contains media info
                    if "|" in content:
                        text, media_info = content.split("|")
                        media_info = media_info.strip()

                        print(f"Posting tweet: {text.strip()}")
                        print(f"With media: {media_info}")

                        if media_info.startswith("http"):
                            self.post_with_media(
                                tweet_text=text.strip(), media_url=media_info
                            )
                        else:
                            media_parts = media_info.split()
                            media_path = media_parts[0]
                            media_type = (
                                media_parts[1] if len(media_parts) > 1 else "image"
                            )

                            self.post_with_media(
                                tweet_text=text.strip(),
                                media_path=media_path,
                                media_type=media_type,
                            )
                    else:
                        print(f"Posting tweet: {content}")
                        self.post_tweet(content)

                    print("Tweet posted successfully!")

                elif action == "reply":
                    parts = content.split(" ", 1)
                    if len(parts) < 2:
                        print("Error: Reply command must include tweet_id and content")
                        continue

                    tweet_id = parts[0]
                    reply_content = parts[1]

                    print(f"Replying to tweet {tweet_id}")

                    if "|" in reply_content:
                        text, media_info = reply_content.split("|")
                        print(f"With text: {text.strip()}")
                        print(f"And media: {media_info.strip()}")

                        # Upload media first
                        if media_info.strip().startswith("http"):
                            media_id = self.upload_media_from_url(media_info.strip())
                        else:
                            media_parts = media_info.strip().split()
                            media_path = media_parts[0]
                            media_type = (
                                media_parts[1] if len(media_parts) > 1 else "image"
                            )
                            if media_type == "video":
                                media_id = self.upload_video(media_path)
                            else:
                                media_id = self.upload_media(media_path)

                        self.reply_with_media(tweet_id, media_id, text.strip())
                    else:
                        print(f"With text: {reply_content}")
                        self.reply_to_tweet(tweet_id, reply_content)

                    print("Reply posted successfully!")

                else:
                    print(f"Error: Unknown action '{action}'")
                    continue

            except Exception as e:
                print(f"Error: {str(e)}")
                print("Please try again.")
                continue
