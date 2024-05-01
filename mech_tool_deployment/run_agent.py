"""
Entrypoint for running the agent in GKE.
If the agent adheres to PMAT standard (subclasses DeployableAgent), 
simply add the agent to the `RunnableAgent` enum and then `RUNNABLE_AGENTS` dict.

Can also be executed locally, simply by running `python mech_tool_deployment/run_agent.py <agent> <market_type>`.
"""

from enum import Enum

import typer
from prediction_market_agent_tooling.markets.markets import MarketType

from mech_tool_deployment.agents.mech_agent.deploy import (
    DeployablePredictionOfflineAgent,
    DeployablePredictionOfflineSMEAgent,
    DeployablePredictionOnlineAgent,
    DeployablePredictionOnlineSMEAgent,
    DeployablePredictionRequestRAGAgent,
    DeployablePredictionRequestReasoningAgent,
    DeployablePredictionUrlCotAgent,
    DeployablePredictionWithResearchBoldAgent,
)


class RunnableAgent(str, Enum):
    mech_prediction_online = "mech_prediction-online"
    mech_prediction_offline = "mech_prediction-offline"
    mech_prediction_online_sme = "mech_prediction-online-sme"
    mech_prediction_offline_sme = "mech_prediction-offline-sme"
    mech_prediction_request_rag = "mech_prediction-request-rag"
    mech_prediction_request_reasoning = "mech_prediction-request-reasoning"
    mech_prediction_url_cot = "mech_prediction-url-cot"
    mech_prediction_with_research_bold = "mech_prediction-with-research-bold"


RUNNABLE_AGENTS = {
    RunnableAgent.mech_prediction_online: DeployablePredictionOnlineAgent,
    RunnableAgent.mech_prediction_offline: DeployablePredictionOfflineAgent,
    RunnableAgent.mech_prediction_online_sme: DeployablePredictionOnlineSMEAgent,
    RunnableAgent.mech_prediction_offline_sme: DeployablePredictionOfflineSMEAgent,
    RunnableAgent.mech_prediction_request_rag: DeployablePredictionRequestRAGAgent,
    RunnableAgent.mech_prediction_request_reasoning: DeployablePredictionRequestReasoningAgent,
    RunnableAgent.mech_prediction_url_cot: DeployablePredictionUrlCotAgent,
    RunnableAgent.mech_prediction_with_research_bold: DeployablePredictionWithResearchBoldAgent,
}


def main(agent: RunnableAgent, market_type: MarketType) -> None:
    RUNNABLE_AGENTS[agent]().run(market_type)


if __name__ == "__main__":
    typer.run(main)
