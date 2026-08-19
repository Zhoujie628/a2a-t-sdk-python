"""Sample scenario input data for the subscribe_incident e2e flow.

Contains the scenario tag, agent_card_query, subscription_filter, and
diagnosis_context used by the sample client.
"""

from __future__ import annotations

# Hard-coded Chinese natural language input used for prompt generation.
NATURAL_LANGUAGE_PROMPT_INPUT = (
    "请生成一个Incident事件订阅任务：通知主题为Incident，"
    "订阅条件为订阅级别为critical的ETH-LOS的故障，上报通知数据格式为DataPart"
)


def build_subscription_request() -> dict[str, object]:
    """Build the sample subscription request input (scenario + agent query + filters)."""
    return {
        "scenario": "create incident subscription",
        "agent_card_query": {
            "name": "SPN Domain Agent",
            "organization": "Huawei",
        },
        "subscription_filter": {
            "alarm_type": "flash",
            "severity": "critical",
            "province": "fujian",
        },
        "diagnosis_context": {
            "domain": "spn",
            "source": "transport_workbench",
        },
    }
