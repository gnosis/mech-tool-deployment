import json
import typing as t
from enum import Enum

from packages.napthaai.customs.prediction_request_rag import prediction_request_rag
from packages.napthaai.customs.prediction_request_reasoning import (
    prediction_request_reasoning,
)
from packages.napthaai.customs.prediction_url_cot import prediction_url_cot
from packages.nickcom007.customs.prediction_request_sme import prediction_request_sme
from packages.polywrap.customs.prediction_with_research_report import (
    prediction_with_research_report,
)
from packages.valory.customs.prediction_request import prediction_request
from prediction_market_agent_tooling.gtypes import Probability
from pydantic import BaseModel

from mech_tool_deployment.api_keys import MechAPIKeys


def completion_str_to_json(completion: str) -> dict[str, t.Any]:
    """
    Cleans completion JSON in form of a string:

    ```json
    {
        ...
    }
    ```

    into just { ... }
    ```
    """
    start_index = completion.find("{")
    end_index = completion.rfind("}")
    completion = completion[start_index : end_index + 1]
    completion_dict: dict[str, t.Any] = json.loads(completion)
    return completion_dict


class MechResponse(BaseModel):
    p_yes: Probability
    p_no: Probability
    confidence: Probability
    info_utility: Probability


class MechTool(str, Enum):
    PREDICTION_WITH_RESEARCH_REPORT = "prediction-with-research-conservative"
    PREDICTION_WITH_RESEARCH_REPORT_BOLD = "prediction-with-research-bold"
    PREDICTION_ONLINE = "prediction-online"
    PREDICTION_OFFLINE = "prediction-offline"
    PREDICTION_ONLINE_SME = "prediction-online-sme"
    PREDICTION_OFFLINE_SME = "prediction-offline-sme"
    PREDICTION_REQUEST_RAG = "prediction-request-rag"
    PREDICTION_REQUEST_REASONING = "prediction-request-reasoning"
    PREDICTION_URL_COT = "prediction-url-cot"


def mech_request_local(
    question: str,
    mech_tool: MechTool,
) -> MechResponse:
    keys = MechAPIKeys()
    if mech_tool in [
        MechTool.PREDICTION_WITH_RESEARCH_REPORT,
        MechTool.PREDICTION_WITH_RESEARCH_REPORT_BOLD,
    ]:
        response = prediction_with_research_report.run(
            tool=mech_tool.value,
            prompt=question,
            api_keys={
                "openai": keys.openai_api_key.get_secret_value(),
                "tavily": keys.tavily_api_key.get_secret_value(),
            },
        )
    elif mech_tool in [MechTool.PREDICTION_ONLINE, MechTool.PREDICTION_OFFLINE]:
        response = prediction_request.run(
            tool=mech_tool.value,
            prompt=question,
            api_keys={
                "openai": keys.openai_api_key.get_secret_value(),
                "google_api_key": keys.google_search_api_key.get_secret_value(),
                "google_engine_id": keys.google_search_engine_id.get_secret_value(),
            },
        )
    elif mech_tool in [MechTool.PREDICTION_ONLINE_SME, MechTool.PREDICTION_OFFLINE_SME]:
        response = prediction_request_sme.run(
            tool=mech_tool.value,
            prompt=question,
            api_keys={
                "openai": keys.openai_api_key.get_secret_value(),
                "google_api_key": keys.google_search_api_key.get_secret_value(),
                "google_engine_id": keys.google_search_engine_id.get_secret_value(),
            },
        )
    elif mech_tool == MechTool.PREDICTION_REQUEST_RAG:
        response = prediction_request_rag.run(
            tool=mech_tool.value,
            prompt=question,
            api_keys={
                "openai": keys.openai_api_key.get_secret_value(),
                "google_api_key": keys.google_search_api_key.get_secret_value(),
                "google_engine_id": keys.google_search_engine_id.get_secret_value(),
            },
        )
    elif mech_tool == MechTool.PREDICTION_REQUEST_REASONING:
        response = prediction_request_reasoning.run(
            tool=mech_tool.value,
            prompt=question,
            api_keys={
                "openai": keys.openai_api_key.get_secret_value(),
                "google_api_key": keys.google_search_api_key.get_secret_value(),
                "google_engine_id": keys.google_search_engine_id.get_secret_value(),
            },
        )
    elif mech_tool == MechTool.PREDICTION_URL_COT:
        response = prediction_url_cot.run(
            tool=mech_tool.value,
            prompt=question,
            api_keys={
                "openai": keys.openai_api_key.get_secret_value(),
                "google_api_key": keys.google_search_api_key.get_secret_value(),
                "google_engine_id": keys.google_search_engine_id.get_secret_value(),
            },
        )
    else:
        raise ValueError(f"Mech type '{mech_tool}' not supported")

    result = completion_str_to_json(str(response[0]))
    return MechResponse.model_validate(result)
