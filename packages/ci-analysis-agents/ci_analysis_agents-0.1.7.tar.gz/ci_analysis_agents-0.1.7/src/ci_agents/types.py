from enum import Enum
from pydantic import BaseModel
from typing import List, Any


class FailureType(str, Enum):
    LAB_ISSUE = "Lab_Issue"
    INFRA_ISSUE = "Infrastructure_Issue"
    THIRD_PARTY = "Third-Party_Issue"
    AT_SCRIPT = "AT_Script"


class Evidence(BaseModel):
    failure_type: FailureType
    related_components: List[str]
    confidence_score: float
    summary: str


class AIActionInsight(BaseModel):
    pass


class ENVIssueActionInsight(AIActionInsight):
    api_url: str
    http_status_code: int
    request_id: str
    detail_log: str

class InfraIssueActionInsight(AIActionInsight):
    device_udid: str
    device_host: str
    detail_log: str
    error_type: str


class AIResponse(BaseModel):
    root_cause_insight: str
    failure_type: FailureType = None
    action_insight: AIActionInsight

    def extract_failure_type(self) -> FailureType:
        if isinstance(self, ENVIssueAIResponse) and self.failed_by_env:
            return FailureType.LAB_ISSUE
        elif isinstance(self, InfraIssueAIResponse) and self.failed_by_infra:
            return FailureType.INFRA_ISSUE
        elif isinstance(self, ThirdPartyIssueAIResponse) and self.failed_by_third_party:
            return FailureType.THIRD_PARTY
        else:
            return FailureType.AT_SCRIPT


class ENVIssueAIResponse(AIResponse):
    failed_by_env: bool
    action_insight: ENVIssueActionInsight
    root_cause_insight: str

    def __init__(self, **data):
        super().__init__(**data)
        if self.failed_by_env:
            self.failure_type = FailureType.LAB_ISSUE


class InfraIssueAIResponse(AIResponse):
    failed_by_infra: bool
    action_insight: InfraIssueActionInsight
    root_cause_insight: str

    def __init__(self, **data):
        super().__init__(**data)
        if self.failed_by_infra:
            self.failure_type = FailureType.INFRA_ISSUE


class ThirdPartyIssueAIResponse(AIResponse):
    failed_by_third_party: bool


class ATScriptAIResponse(AIResponse):
    failed_by_at_script: bool


class AnalysisContext(BaseModel):
    test_id:str = ""
    backend_api_log: str = ""
    app_log: str = ""
    appium_log: str = ""
    device_log: str = ""
    failure_log: str = ""
    failed_thread_log: str = ""
    env_issue_response: ENVIssueAIResponse = None
    infra_issue_response: InfraIssueAIResponse = None
    third_party_issue_response: ThirdPartyIssueAIResponse = None
    at_script_issue_response: ATScriptAIResponse = None
    beats_metadata: Any = None


def save_response_to_context(context: AnalysisContext, output: Any) -> None:
    if isinstance(output, ENVIssueAIResponse):
        print(f"save_response_lab_to_context: {output}")
        context.env_issue_response = output
    elif isinstance(output, InfraIssueAIResponse):
        print(f"save_response_infra_to_context: {output}")
        context.infra_issue_response = output
    elif isinstance(output, ThirdPartyIssueAIResponse):
        context.third_party_issue_response = output
    elif isinstance(output, ATScriptAIResponse):
        context.at_script_issue_response = output


def dispatch_ai_response(response: AIResponse, context: AnalysisContext) -> AIResponse:
    # fixme: combine the original response with the context response
    if context.env_issue_response and context.env_issue_response.failed_by_env:
        response = context.env_issue_response
    elif context.infra_issue_response and context.infra_issue_response.failed_by_infra:
        response = context.infra_issue_response
    elif context.third_party_issue_response and context.third_party_issue_response.failed_by_third_party:
        response = context.third_party_issue_response
    elif context.at_script_issue_response and context.at_script_issue_response.failed_by_at_script:
        response = context.at_script_issue_response
    else:
        response = response
    response.failure_type = response.extract_failure_type()
    return response
