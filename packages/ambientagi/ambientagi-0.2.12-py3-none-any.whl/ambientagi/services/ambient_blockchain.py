import json
import logging
import os
from typing import Optional

import requests  # type: ignore

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class BlockchainService:
    def __init__(self, agent: dict):
        """
        Initialize BlockchainService with API clients for Solana, Ethereum, and AgentService.

        :param agent: Agent to manage (dict).
        """
        self.agent = agent
        self.agent_id = agent["agent_id"]

        # Solana API client
        self.solana_api = "https://api-solana.ambientagi.ai"
        # Ethereum API client
        self.eb_base_url = "https://api-eth.ambientagi.ai"

    # ---------------------------
    # 0) Create a new Solana Wallet
    # ---------------------------
    def create_solana_wallet(self):
        """
        Calls /pump/createWallet to generate a new Solana wallet (public/private key).
        Returns the JSON response, e.g.:
          {
            "apiKey": "...",            # Possibly
            "walletPublicKey": "...",
            "privateKey": "..."
          }
        """
        response = self.solana_api.get("/pump/createWallet")
        # The endpoint typically returns a new wallet's pubkey + private key
        return response

    # -------------------------------------------------------
    # 2) All-In-One Solana Token Creation (New Wallet)
    # -------------------------------------------------------
    def create_solana_token(
        self,
        funder_private_key: str,
        amount_sol: float,
        token_name: str,
        token_symbol: str,
        token_description: str,
        twitter: str,
        telegram: str,
        website: str,
        image_path: Optional[str] = None,
        dev_buy: float = 0.001,
        use_new_wallet: bool = False,  # Determines whether to create a new wallet first
    ):
        """
        Creates a Solana token using either:
        1) The funder's wallet directly (default)
        2) A newly created wallet that first receives SOL from the funder

        :param funder_private_key: The base58 private key of the funder wallet
        :param amount_sol: SOL amount to transfer (only used if creating a new wallet)
        :param token_name: Token name (e.g., "MySolToken")
        :param token_symbol: Token symbol (e.g., "MST")
        :param token_description: Description (e.g., "Created by agent xyz")
        :param twitter: Twitter link or handle
        :param telegram: Telegram link or group
        :param website: Website for the token project
        :param image_path: Path to the token image file (optional)
        :param dev_buy: Amount of SOL for dev buy (default = 0.001)
        :param use_new_wallet: If True, a new wallet will be created first before minting
        :return: Response JSON from API
        """

        endpoint = (
            f"{self.solana_api}/pump/new-wallet-create"
            if use_new_wallet
            else f"{self.solana_api}/pump/funder-create"
        )

        # Set up logging
        logging.basicConfig(level=logging.INFO)
        logging.info("🛠️ Starting to create Solana token...")

        files_data = {}
        if image_path and os.path.isfile(image_path):
            logging.info(f"📸 Uploading image from {image_path}...")
            files_data["file"] = (
                "logo.png",
                open(image_path, "rb"),
                "image/webp",
            )  # WebP format

        # Prepare data fields
        data_fields = {
            "funderPrivateKey": funder_private_key,
            "tokenName": token_name,
            "tokenSymbol": token_symbol,
            "tokenDescription": token_description,
            "twitter": twitter,
            "telegram": telegram,
            "website": website,
            "devBuy": str(dev_buy),
        }

        if use_new_wallet:
            data_fields["amountSol"] = str(
                amount_sol
            )  # Required only for new-wallet method

        logging.info(
            f"🚀 Sending request to {endpoint} to create token {token_name} ({token_symbol}) with {amount_sol} SOL..."
        )

        response = requests.post(endpoint, data=data_fields, files=files_data)

        # Handle the response
        response_json = response.json()
        token_result = response_json.get("tokenResult", {})
        token_mint = token_result.get("mint")

        if token_mint:
            logging.info(
                f"🎉 Token {token_name} created successfully with mint address {token_mint}."
            )
            # self.update_agent_token_data(solana_token_address=token_mint)
        else:
            logging.error(f"❌ Failed to create token. API Response: {response_json}")

        return response_json

    def create_eth_token(
        self,
        privateKey: str,
        token_name: str,
        symbol: str,
        decimals: int = 18,
        buy_value_eth: float = 0.01,
        image_path: Optional[str] = None,
        websiteUrl: Optional[str] = None,
        twitterUrl: Optional[str] = None,
        telegramUrl: Optional[str] = None,
    ):
        """
        Create an Ethereum token using the provided private key and token details.
        :param privateKey: The private key of the wallet creating the token.
        :param token_name: The name of the token.
        :param symbol: The symbol of the token.
        :param decimals: The number of decimals for the token (default is 18).
        :param buy_value_eth: The buy value in ETH (default is 0.01).
        :param image_path: Optional path to the token logo image.
        :param websiteUrl: Optional website URL for the token.
        :param twitterUrl: Optional Twitter URL for the token.
        :param telegramUrl: Optional Telegram URL for the token.
        :return: The response from the API.
        """
        # 0) Validate inputs
        url = f"{self.eb_base_url}/createSale"

        # 1) Initialize `files_data` so we can safely add to it if there's an image:
        files_data = {}

        # 2) If an image is provided, open it and add to files_data
        if image_path and os.path.isfile(image_path):
            files_data["logoUrl"] = (
                os.path.basename(image_path),
                open(image_path, "rb"),
                "image/png",  # Or "image/webp", etc.
            )

        # 3) Prepare form (text) data (Ensure exact field names match your cURL)
        form_data = {
            "privateKey": privateKey,
            "tokenName": token_name,
            "tokenSymbol": symbol,
            "description": f"Created by agent {self.agent_id}",
            "buyValue": "{:.6f}".format(buy_value_eth),
            "websiteUrl": websiteUrl or "https://example.com",
            "twitterUrl": twitterUrl or "https://twitter.com/MyEtherFunToken",
            "telegramUrl": telegramUrl or "https://t.me/MyEtherFunToken",
        }

        # 4) Debug logging
        logging.info(
            f"📤 Sending request to /createSale with data: {json.dumps(form_data, indent=4)}"
        )
        if files_data:
            logging.info(
                f"📂 Sending file with name: {list(files_data.keys())} -> {files_data['logoUrl'][0]}"
            )

        try:
            # 5) Make the request
            response = requests.post(url, data=form_data, files=files_data, timeout=30)

            # 6) Log response
            logging.info(f"✅ Status Code: {response.status_code}")
            logging.info(f"✅ Response Text: {response.text}")

            # Attempt to parse JSON response if available
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"status": response.status_code, "body": response.text}

        except Exception as e:
            logging.error(f"❌ API Request Failed: {e}")
            return {"error": str(e)}
