import pandas as pd
from enum import Enum
from .base import BaseDTO
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from .datasets import DatasetConfig
from .models import ModelConfig


@dataclass
class RedteamHealthResponse(BaseDTO):
    status: str
    _extra_fields: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RedteamHealthResponse":
        return cls(
            status=data.get("status", "")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status
        }


@dataclass
class RedTeamResponse(BaseDTO):
    status: Optional[str] = None
    task_id: Optional[str] = None
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    _extra_fields: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict) -> "RedTeamResponse":
        return cls(
            task_id=data.get("task_id"),
            message=data.get("message"),
            data=data.get("data"),
        )
    
    def to_dict(self) -> Dict:
        return super().to_dict()


@dataclass
class RedTeamTaskStatus(BaseDTO):
    status: Optional[str] = None


@dataclass
class RedTeamTaskDetails(BaseDTO):
    created_at: Optional[str] = None
    model_name: Optional[str] = None
    status: Optional[str] = None
    test_name: Optional[str] = None
    task_id: Optional[str] = None


@dataclass
class StatisticItem(BaseDTO):
    success_percentage: float
    total: int
    _extra_fields: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict) -> "StatisticItem":
        return cls(
            success_percentage=data.get("success(%)", 0.0), total=data.get("total", 0)
        )

    def to_dict(self) -> Dict:
        d = super().to_dict()
        # Special handling for success percentage key
        d["success(%)"] = d.pop("success_percentage")
        return d


@dataclass
class StatisticItemWithTestType(BaseDTO):
    success_percentage: float
    total: int
    test_type: Optional[str] = None
    _extra_fields: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict) -> "StatisticItemWithTestType":
        return cls(
            success_percentage=data.get("success(%)", 0.0),
            total=data.get("total", 0),
            test_type=data.get("test_type", None),
        )

    def to_dict(self) -> Dict:
        d = super().to_dict()
        # Special handling for success percentage key
        d["success(%)"] = d.pop("success_percentage")
        return d


@dataclass
class ResultSummary(BaseDTO):
    test_date: str
    test_name: str
    dataset_name: str
    model_endpoint_url: str
    model_source: str
    model_provider: str
    risk_score: float
    model_name: Optional[str]
    test_type: Dict[str, StatisticItem]
    nist_category: Dict[str, StatisticItem]
    scenario: Dict[str, StatisticItem]
    category: Dict[str, StatisticItemWithTestType]
    attack_method: Dict[str, StatisticItem]
    _extra_fields: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict) -> "ResultSummary":
        def convert_stat_list(stat_list: List[Dict]) -> Dict[str, StatisticItem]:
            result = {}
            for item in stat_list:
                for key, value in item.items():
                    result[key] = StatisticItem.from_dict(value)
            return result
        
        def convert_stat_test_type_list(stat_list: List[Dict]) -> Dict[str, StatisticItemWithTestType]:
            result = {}
            for item in stat_list:
                for key, value in item.items():
                    result[key] = StatisticItemWithTestType.from_dict(value)
            return result

        return cls(
            test_date=data.get("test_date", ""),
            test_name=data.get("test_name", ""),
            dataset_name=data.get("dataset_name", ""),
            model_name=data.get("model_name", ""),
            model_endpoint_url=data.get("model_endpoint_url", ""),
            model_source=data.get("model_source", ""),
            model_provider=data.get("model_provider", ""),
            risk_score=data.get("risk_score", 0.0),
            test_type=convert_stat_list(data.get("test_type", [])),
            nist_category=convert_stat_list(data.get("nist_category", [])),
            scenario=convert_stat_list(data.get("scenario", [])),
            category=convert_stat_test_type_list(data.get("category", [])),
            attack_method=convert_stat_list(data.get("attack_method", [])),
        )

    def to_dict(self) -> Dict:
        def convert_stat_dict(stat_dict: Dict[str, StatisticItem]) -> List[Dict]:
            return [{key: value.to_dict()} for key, value in stat_dict.items()]
        
        def convert_stat_test_type_dict(stat_dict: Dict[str, StatisticItemWithTestType]) -> List[Dict]:
            return [{key: value.to_dict()} for key, value in stat_dict.items()]

        d = super().to_dict()
        # Convert stat dictionaries to lists of dictionaries
        d["test_type"] = convert_stat_dict(self.test_type)
        d["nist_category"] = convert_stat_dict(self.nist_category)
        d["scenario"] = convert_stat_dict(self.scenario)
        d["category"] = convert_stat_test_type_dict(self.category)
        d["attack_method"] = convert_stat_dict(self.attack_method)
        return d


@dataclass
class RedTeamResultSummary(BaseDTO):
    summary: ResultSummary
    task_status: Optional[str] = None
    _extra_fields: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict) -> "RedTeamResultSummary":
        if not data or "summary" not in data:
            return cls(summary=ResultSummary.from_dict({}))
        
        if "task_status" in data:
            return cls(summary=ResultSummary.from_dict({}), task_status=data["task_status"])

        return cls(summary=ResultSummary.from_dict(data["summary"]))

    def to_dict(self) -> Dict:
        return {"summary": self.summary.to_dict()}


@dataclass
class TestEvalTokens(BaseDTO):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    _extra_fields: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TestResult(BaseDTO):
    prompt: str
    category: str
    test_type: str
    nist_category: str
    source: str
    attack_method: str
    jailbreak_prompt: str
    response: str
    success: str
    reasoning: str
    detected_language: str
    eval_latency: float
    eval_tokens: TestEvalTokens
    test_name: str
    _extra_fields: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RedTeamResultDetails(BaseDTO):
    details: List[TestResult]
    task_status: Optional[str] = None
    _extra_fields: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict) -> "RedTeamResultDetails":
        if not data or "details" not in data:
            return cls(details=[])
        
        if "task_status" in data:
            return cls(details=[], task_status=data["task_status"])

        # details = []
        # for result in data["details"]:
            # Convert eval_tokens dict to TestEvalTokens object
            # eval_tokens = TestEvalTokens(**result["eval_tokens"])

            # Create a copy of the result dict and replace eval_tokens
            # result_copy = dict(result["details"])
            # result_copy["eval_tokens"] = eval_tokens

            # Create TestResult object
            # test_result = TestResult(**result_copy)
            # details.append(test_result)

        return cls(details=data["details"])

    def to_dict(self) -> Dict:
        return {
            # "details": [
            #     {**result.to_dict(), "eval_tokens": result.eval_tokens.to_dict()}
            #     for result in self.details
            # ]
            "details": self.details
        }

    # def to_dataframe(self) -> pd.DataFrame:
    #     data = [
    #         {**result.to_dict(), "eval_tokens": result.eval_tokens.to_dict()}
    #         for result in self.details
    #     ]
    #     return pd.DataFrame(data)


@dataclass
class AttackMethods(BaseDTO):
    basic: List[str] = field(default_factory=lambda: ["basic"])
    # advanced: Dict[str, List[str]] = field(
    #     default_factory=lambda: {"static": ["single_shot"], "dynamic": ["iterative"]}
    # )
    advanced: Dict[str, List[str]] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class TestConfig(BaseDTO):
    sample_percentage: int = 5
    attack_methods: AttackMethods = field(default_factory=AttackMethods)

    def to_dict(self) -> dict:
        return {
            "sample_percentage": self.sample_percentage,
            "attack_methods": self.attack_methods.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict):
        attack_methods = AttackMethods.from_dict(data.pop("attack_methods", {}))
        return cls(**data, attack_methods=attack_methods)


@dataclass
class RedTeamTestConfigurations(BaseDTO):
    # Basic tests
    bias_test: TestConfig = field(default=None)
    cbrn_test: TestConfig = field(default=None)
    insecure_code_test: TestConfig = field(default=None)
    toxicity_test: TestConfig = field(default=None)
    harmful_test: TestConfig = field(default=None)
    # Advanced tests
    adv_info_test: TestConfig = field(default=None)
    adv_bias_test: TestConfig = field(default=None)
    adv_command_test: TestConfig = field(default=None)
    custom_test: TestConfig = field(default=None)
    _extra_fields: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**{k: TestConfig.from_dict(v) for k, v in data.items()})


class InputModality(str, Enum):
    text = "text"
    image = "image"
    audio = "audio"
    # video = "video"
    # code = "code"


class OutputModality(str, Enum):
    text = "text"
    # image = "image"
    # audio = "audio"
    # video = "video"
    # code = "code"


@dataclass
class CustomHeader(BaseDTO):
    key: str
    value: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CustomHeader":
        return cls(
            key=data.get("key", ""),
            value=data.get("value", "")
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "value": self.value
        }
    

@dataclass
class TargetModelConfiguration(BaseDTO):
    testing_for: str = "foundationModels"
    system_prompt: str = ""
    model_source: str = ""
    model_provider: str = "openai"
    model_endpoint_url: str = "https://api.openai.com/v1/chat/completions"
    rate_per_min: int = 20
    model_name: Optional[str] = "gpt-4o-mini"
    model_version: Optional[str] = None
    model_api_key: Optional[str] = None
    input_modalities: List[InputModality] = field(default_factory=list)
    output_modalities: List[OutputModality] = field(default_factory=list)
    custom_curl_command: Optional[str] = None
    custom_headers: List[CustomHeader] = field(default_factory=list)
    custom_payload: Dict[str, Any] = field(default_factory=dict)
    custom_response_content_type: Optional[str] = ""
    custom_response_format: Optional[str] = ""
    _extra_fields: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict):
        data = data.copy()
        if "custom_headers" in data:
            data["custom_headers"] = [CustomHeader.from_dict(header) for header in data["custom_headers"]]
        return cls(**data)
    
    def to_dict(self) -> dict:
        d = asdict(self)
        d["custom_headers"] = [header.to_dict() for header in self.custom_headers]
        return d


@dataclass
class RedTeamModelHealthConfig(BaseDTO):
    target_model_configuration: TargetModelConfiguration = field(
        default_factory=TargetModelConfiguration
    )

    def to_dict(self) -> dict:
        d = asdict(self)
        d["target_model_configuration"] = self.target_model_configuration.to_dict()
        return d

    @classmethod
    def from_dict(cls, data: dict):
        data = data.copy()
        target_config = TargetModelConfiguration.from_dict(
            data.pop("target_model_configuration", {})
        )
        return cls(
            # **data,
            target_model_configuration=target_config,
        )


@dataclass
class RedteamModelHealthResponse(BaseDTO):
    status: str
    message: str
    error: str
    data: Optional[Dict[str, Any]] = field(default_factory=dict)
    _extra_fields: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RedteamModelHealthResponse":
        return cls(
            status=data.get("status", ""),
            message=data.get("message", ""),
            data=data.get("data", {}),
            error=data.get("error", "")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data,
            "error": self.error
        }


@dataclass
class RedTeamConfig(BaseDTO):
    test_name: str = "Test Name"
    dataset_name: str = "standard"

    redteam_test_configurations: RedTeamTestConfigurations = field(
        default_factory=RedTeamTestConfigurations
    )
    target_model_configuration: TargetModelConfiguration = field(
        default_factory=TargetModelConfiguration
    )

    _extra_fields: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["redteam_test_configurations"] = self.redteam_test_configurations.to_dict()
        d["target_model_configuration"] = self.target_model_configuration.to_dict()
        return d

    @classmethod
    def from_dict(cls, data: dict):
        data = data.copy()
        test_configs = RedTeamTestConfigurations.from_dict(
            data.pop("redteam_test_configurations", {})
        )
        target_config = TargetModelConfiguration.from_dict(
            data.pop("target_model_configuration", {})
        )
        return cls(
            **data,
            redteam_test_configurations=test_configs,
            target_model_configuration=target_config,
        )


@dataclass
class RedTeamConfigWithSavedModel(BaseDTO):
    test_name: str = "Test Name"
    dataset_name: str = "standard"
    model_saved_name: str = "gpt-4o-mini"
    model_version: str = "v1"

    redteam_test_configurations: RedTeamTestConfigurations = field(
        default_factory=RedTeamTestConfigurations
    )

    _extra_fields: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["redteam_test_configurations"] = self.redteam_test_configurations.to_dict()
        return d

    @classmethod
    def from_dict(cls, data: dict):
        data = data.copy()
        test_configs = RedTeamTestConfigurations.from_dict(
            data.pop("redteam_test_configurations", {})
        )
        return cls(
            **data,
            redteam_test_configurations=test_configs,
        )


@dataclass
class RedTeamCustomConfig(BaseDTO):
    test_name: str = "Test Name"

    redteam_test_configurations: RedTeamTestConfigurations = field(
        default_factory=RedTeamTestConfigurations
    )
    dataset_configuration: DatasetConfig = field(
        default_factory=DatasetConfig
    )
    endpoint_configuration: ModelConfig = field(
        default_factory=ModelConfig
    )

    _extra_fields: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["redteam_test_configurations"] = self.redteam_test_configurations.to_dict()
        d["dataset_configuration"] = self.dataset_configuration.to_dict()
        d["endpoint_configuration"] = self.endpoint_configuration.to_dict()
        return d

    @classmethod
    def from_dict(cls, data: dict):
        data = data.copy()
        test_configs = RedTeamTestConfigurations.from_dict(
            data.pop("redteam_test_configurations", {})
        )
        dataset_config = DatasetConfig.from_dict(
            data.pop("dataset_configuration", {})
        )
        endpoint_config = ModelConfig.from_dict(
            data.pop("endpoint_configuration", {})
        )
        return cls(
            **data,
            redteam_test_configurations=test_configs,
            dataset_configuration=dataset_config,
            endpoint_configuration=endpoint_config,
        )

@dataclass
class RedTeamCustomConfigWithSavedModel(BaseDTO):
    test_name: str = "Test Name"

    redteam_test_configurations: RedTeamTestConfigurations = field(
        default_factory=RedTeamTestConfigurations
    )
    dataset_configuration: DatasetConfig = field(
        default_factory=DatasetConfig
    )

    _extra_fields: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["redteam_test_configurations"] = self.redteam_test_configurations.to_dict()
        d["dataset_configuration"] = self.dataset_configuration.to_dict()
        return d

    @classmethod
    def from_dict(cls, data: dict):
        data = data.copy()
        test_configs = RedTeamTestConfigurations.from_dict(
            data.pop("redteam_test_configurations", {})
        )
        dataset_config = DatasetConfig.from_dict(
            data.pop("dataset_configuration", {})
        )
        return cls(
            **data,
            redteam_test_configurations=test_configs,
            dataset_configuration=dataset_config,
        )


@dataclass
class RedTeamTaskList(BaseDTO):
    tasks: List[RedTeamTaskDetails] = field(default_factory=list)

    def to_dataframe(self) -> pd.DataFrame:
        data = [task for task in self.tasks]
        return pd.DataFrame(data)


# Default configurations
DEFAULT_REDTEAM_CONFIG = RedTeamConfig()
DEFAULT_REDTEAM_CONFIG_WITH_SAVED_MODEL = RedTeamConfigWithSavedModel()

DEFAULT_CUSTOM_REDTEAM_CONFIG = RedTeamCustomConfig()
DEFAULT_CUSTOM_REDTEAM_CONFIG_WITH_SAVED_MODEL = RedTeamCustomConfigWithSavedModel()
