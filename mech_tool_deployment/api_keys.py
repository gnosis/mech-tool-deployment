import typing as t

from prediction_market_agent_tooling.config import APIKeys
from prediction_market_agent_tooling.tools.utils import check_not_none
from pydantic import SecretStr


class MechAPIKeys(APIKeys):
    TAVILY_API_KEY: t.Optional[SecretStr] = None

    @property
    def tavily_api_key(self) -> SecretStr:
        return check_not_none(
            self.TAVILY_API_KEY, "OPENAI_API_KEY missing in the environment."
        )
