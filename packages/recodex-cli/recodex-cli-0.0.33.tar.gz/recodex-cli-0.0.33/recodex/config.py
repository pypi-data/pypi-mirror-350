from functools import lru_cache

import jwt
from ruamel.yaml import YAML
from typing import NamedTuple, Optional
from datetime import datetime, timezone
from pathlib import Path


class UserContext(NamedTuple):
    api_url: Optional[str] = None
    api_token: Optional[str] = None

    @property
    @lru_cache()
    def token_data(self):
        if self.api_token is None:
            raise RuntimeError("The API token is not set")

        return jwt.decode(self.api_token, options={"verify_signature": False})

    @property
    def user_id(self):
        return self.token_data["sub"]

    def is_token_almost_expired(self, threshold=0.5) -> bool:
        """
        Returns true if the token is about to expire
        :param threshold: A number between 0 and 1. If less than (threshold * token validity period) is left until
                          expiration, the method will return True.
        """

        validity_period = self.token_data["exp"] - self.token_data["iat"]
        time_until_expiration = self.token_data["exp"] - \
            datetime.now(timezone.utc).timestamp()
        return validity_period * threshold > time_until_expiration

    @property
    def is_token_expired(self) -> bool:
        return self.token_data["exp"] <= datetime.now(timezone.utc).timestamp()

    def replace_token(self, new_token) -> 'UserContext':
        return self._replace(api_token=new_token)

    @classmethod
    def load(cls, config_path: Path):
        yaml = YAML(typ="safe")
        config = yaml.load(config_path.open("r")) or {}
        return cls(**config)

    def store(self, config_path: Path):
        config_path.parent.mkdir(parents=True, exist_ok=True)
        yaml = YAML(typ="safe")
        with config_path.open("w") as fp:
            yaml.dump(dict(self._asdict()), fp)
