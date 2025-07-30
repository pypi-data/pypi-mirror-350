import os
from google.auth import default
from google.oauth2.service_account import Credentials
from pathlib import Path
from typing import Optional, Union

class GoogleCredentialsLoader:
    @staticmethod
    def load(credentials_path:Optional[Union[Path, str]] = None) -> Credentials:
        if credentials_path is None:
            credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
        else:
            credentials_path = credentials_path
        try:
            if credentials_path is not None:
                credentials_path = Path(credentials_path)
                if credentials_path.exists() or credentials_path.is_file():
                    credentials = Credentials.from_service_account_file(
                        filename=str(credentials_path)
                    )
            else:
                credentials, _ = default()
            return credentials
        except Exception as e:
            raise ValueError(f"Failed to initialize credentials: {str(e)}")