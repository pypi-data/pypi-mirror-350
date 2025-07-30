"""
Model class for the chatbot which is pushed to the chatbot webservice.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Union

import pytz
from dataclasses_json import config, dataclass_json

from aistudio_cognition.km.genai.models.genai_settings import GenAI
from aistudio_cognition.km.qnamaker.models.qnamaker_settings import QnAMaker
from aistudio_cognition.nlu.luis.models.luis_settings import LUIS

logger = logging.getLogger(__name__)


def validate_timezone(value):
    if value not in pytz.all_timezones:
        raise ValueError(f"'{value}' is not a valid timezone.")


""" Enumerations
"""


class ConnectionType(Enum):
    AISTUDIO = "AISTUDIO"
    AUTOMATIONEDGE = "AUTOMATIONEDGE"


class MessageType(Enum):
    TEXT = "text"
    ADAPTIVE_CARD = "adaptivecard"
    DIALOG = "dialog"
    NONE = ""


class CustomTriggerOrder(Enum):
    FIRST = 1
    LAST = 2
    NONE = None


class DialogElementType(Enum):
    MESSAGE = "message"
    INPUT = "input"
    FORM = "form"
    CARD = "card"
    ACTION = "action"
    BRANCH = "branch"
    FILE_INPUT = "file_input"
    SET_STATE = "set_state"
    GROUP = "group"


class InputType(Enum):
    TEXT = "text"
    CHOICE = "choice"
    NUMBER = "number"
    DATE = "date"
    TIME = "time"


class CardType(Enum):
    HERO = "Hero"
    ADAPTIVE = "Adaptive"
    ADAPTIVE_LIST = "Adaptive List"
    WHATSAPP_FLOWS = "WhatsApp Flows"


class ActionType(Enum):
    PYTHON = "python"
    AE_WORKFLOW = "ae_workflow"


class AIStudioParamType(Enum):
    INPUT = "input"
    FILE = "file"
    CREDENTIAL = "credential"
    FUNCTION = "function"
    AIS_CREDENTIAL = "ais_credential"
    NONE = ""


class OutputType(Enum):
    TEXT = "Text"
    CARD = "Card"


class State(Enum):
    DIALOG = "dialog"
    CONVERSATION = "conversation"
    USER = "user"


class SetStateVariableValueType(Enum):
    NUMBER = "number"
    DICTIONARY = "dictionary"
    STRING = "string"


class TriggerType(Enum):
    REGEX = "regex"
    NLU = "nlu"


class ChoiceStyle(Enum):
    HERO_CARD = "hero_card"
    SUGGESTED_ACTION = "suggested_action"
    IN_LINE = "in_line"
    LIST_STYLE = "list_style"
    CHANNEL_SPECIFIC = "auto"


class NLUType(Enum):
    LUIS = "LUIS"
    DELTA = "DELTA"


class KMType(Enum):
    QNAMAKER = "QNAMAKER"
    GENAI = "GENAI"


class ScheduleTrigger(Enum):
    TRIGGER_INTERVAL = "interval"
    TRIGGER_CRON = "cron"
    TRIGGER_DATE = "date"

    @classmethod
    def from_str(cls, trigger):
        if trigger.lower() == "interval":
            return cls.TRIGGER_INTERVAL
        elif trigger.lower() == "cron":
            return cls.TRIGGER_CRON
        elif trigger.lower() == "date":
            return cls.TRIGGER_DATE


class OutputFilesOrder(Enum):
    BEFORE = 1
    AFTER = 2


"""Chatbot configuration dataclasses
"""


@dataclass_json
@dataclass
class Connection:
    """Project level connections, AIStudio and AutomationEdge."""

    name: str
    type: ConnectionType
    url: str
    username: str
    password: str
    tenant_orgcode: str


@dataclass_json
@dataclass
class Credential:
    """Project level credentials"""

    name: str
    value1: str
    value2: Optional[str] = None
    value3: Optional[str] = None
    value4: Optional[str] = None
    value5: Optional[str] = None
    value6: Optional[str] = None


@dataclass_json
@dataclass
class AIStudioProject:
    """Skill level connections, NLU and KM"""

    project_name: str
    connection_name: str
    connection_type: ConnectionType


@dataclass_json
@dataclass
class AIStudioNLU:
    """NLU details used in the cognibot project"""

    project_name: str
    connection_name: str
    nlu_type: NLUType
    # Once DELTA also is moved to aistudio-cognition, the expected value for nlu_details : Union [LUIS, DELTA]
    nlu_details: LUIS


@dataclass_json
@dataclass
class AIStudioKM:
    """KM details used in the cognibot project"""

    project_name: str
    connection_name: str
    km_type: KMType
    km_details: Union[QnAMaker, GenAI]


@dataclass_json
@dataclass
class WelcomeMessage:
    type: MessageType
    message: str
    enabled: bool


@dataclass_json
@dataclass
class BroadcastMessage:
    type: MessageType
    message: str
    start: str
    end: str
    enabled: bool


@dataclass_json
@dataclass
class CancelMessage:
    type: MessageType
    message: str
    pattern: list[str]


@dataclass_json
@dataclass
class Handoff:
    agents: list[str] = field(default_factory=list)
    enabled: Optional[bool] = False
    triggers: Optional[list[str]] = field(default_factory=list)


@dataclass_json
@dataclass
class Feedback:
    enabled: bool = False
    dialog: str = ""
    rating: str = ""
    feedback: str = ""


@dataclass_json
@dataclass
class CustomTrigger:
    enabled: bool
    function: str = ""
    order: CustomTriggerOrder = field(default=CustomTriggerOrder.NONE)


@dataclass_json
@dataclass
class I18nSettings:
    default_language: str = "en"
    enabled: Optional[bool] = True
    triggers: Optional[list[str]] = field(default_factory=list)


@dataclass_json
@dataclass
class Schedule:
    is_local_schedule: bool
    function: str
    name: str
    # fields for interval trigger
    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    # fields for cron trigger
    year: Optional[str] = None
    month: Optional[str] = None
    day: Optional[str] = None
    week: Optional[str] = None
    day_of_week: Optional[str] = None
    hour: Optional[str] = None
    minute: Optional[str] = None
    second: Optional[str] = None
    # field for date trigger
    run_date: Optional[datetime] = None
    # common attributes
    # following two are not valid for date trigger
    start_date: datetime = datetime.now()
    end_date: Optional[datetime] = None
    max_instances: int = 1
    trigger: ScheduleTrigger = field(default=ScheduleTrigger.TRIGGER_INTERVAL)
    timezone: str = field(default="UTC", metadata=dict(validate=validate_timezone))

    def __post_init__(self):
        # While converting to json from dataclass, dataclasses-json
        # converts the timezone-naive object to timestamp, and while
        # converting back to dataclass, it converts it to timezone-aware
        # object (i.e. adds UTC as timezone), which we don't want.
        # TODO; revisit this and think of a better approach,
        self.start_date = self.start_date.replace(tzinfo=None)
        if self.end_date:
            self.end_date = self.end_date.replace(tzinfo=None)
        if self.run_date:
            self.run_date = self.run_date.replace(tzinfo=None)


"""Dialog Elements
"""


@dataclass_json
@dataclass
class Message:
    message: str
    element_condition: str = "True"
    type: DialogElementType = DialogElementType.MESSAGE


@dataclass_json
@dataclass
class Input:
    input_type: InputType
    id: str
    message: str
    state: State
    nlu_response_state: State = State.DIALOG
    nlu_response_id: str = ""
    call_nlu: bool = False
    retry_message: Optional[str] = None
    max_attempts: int = 0
    is_required: bool = False
    label: str = ""
    input_choices: Optional[str] = None
    choice_style: Optional[ChoiceStyle] = ChoiceStyle.HERO_CARD
    default_value: Union[str, int, None] = None
    min: Union[str, int, None] = None
    max: Union[str, int, None] = None
    regex: Optional[str] = None
    ignore_case: Optional[bool] = None  # only for type: regex
    function: Optional[str] = None
    nlu_entity: Optional[str] = None
    element_condition: str = "True"
    type: DialogElementType = DialogElementType.INPUT

    def __post_init__(self):
        if not self.retry_message:
            self.retry_message = self.message


@dataclass_json
@dataclass
class Form:
    title: str
    adaptive_card: bool
    confirm_on_submit: bool = False
    # instead of default [], we use field(default_factory=list)
    # else, it throws error
    elements: list[Input] = field(default_factory=list)
    element_condition: str = "True"
    type: DialogElementType = DialogElementType.FORM


@dataclass_json
@dataclass
class Card:
    card_type: CardType
    card_data: str
    has_input: bool = False
    list_variable: Optional[str] = None
    response_variable: Optional[str] = None
    response_variable_state: Optional[State] = None
    element_condition: str = "True"
    type: DialogElementType = DialogElementType.CARD
    retry_message: Optional[str] = None
    max_attempts: int = 0


@dataclass_json
@dataclass
class ActionResponse:
    wait_for_response: bool = False
    timeout_in_seconds: Optional[float] = None
    wait_message: Optional[str] = None
    timeout_message: Optional[str] = None
    variable_name: Optional[str] = None
    variable_state: Optional[State] = None


@dataclass_json
@dataclass
class ActionOutputFormat:
    condition: str
    output_type: OutputType
    message: Optional[str] = None
    card_type: Optional[CardType] = None
    card_data: Optional[str] = None
    list_variable: Optional[str] = None
    files_order: OutputFilesOrder = field(default=OutputFilesOrder.BEFORE)


@dataclass_json
@dataclass
class AIStudioParam:
    """Details entered by the chatbot designer for AE workflow parameter"""

    value: str
    type: AIStudioParamType


@dataclass_json
@dataclass
class WorkflowParam:
    """AE Workflow parameter details"""

    name: str
    type: str
    order: int
    secret: bool
    optional: bool
    displayName: str
    aistudio: AIStudioParam
    poolCredential: bool = False
    defaultValue: Optional[str] = None
    extension: Optional[str] = None
    listOfValues: Optional[str] = field(default_factory=list)
    valueSeparator: Optional[str] = ","


@dataclass_json
@dataclass
class Workflow:
    """AE Workflow details"""

    id: int
    workflow_name: str = field(metadata=config(field_name="workflowName"))
    description: str = ""
    inputAttributesEnabled: bool = False
    inputAttribute1: Optional[str] = None
    inputAttribute2: Optional[str] = None
    inputAttribute3: Optional[str] = None
    inputAttribute4: Optional[str] = None
    inputAttribute5: Optional[str] = None
    inputAttribute6: Optional[str] = None
    params: list[WorkflowParam] = field(default_factory=list)


@dataclass_json
@dataclass
class ActionCondition:
    action_name: str
    value: str
    action_type: ActionType
    response: ActionResponse
    output_format: list[ActionOutputFormat] = field(default_factory=list)
    message: str = ""
    function: Optional[str] = None  # only for action_type: python
    connection_name: Optional[str] = None  # only for action_type: ae_workflow
    workflow: Optional[Workflow] = None  # only for action_type: ae_workflow


@dataclass_json
@dataclass
class Action:
    conditions: list[ActionCondition]
    element_condition: str = "True"
    type: DialogElementType = DialogElementType.ACTION


@dataclass_json
@dataclass
class BranchCondition:
    value: str
    target: str


@dataclass_json
@dataclass
class Branch:
    conditions: list[BranchCondition]
    element_condition: str = "True"
    type: DialogElementType = DialogElementType.BRANCH


@dataclass_json
@dataclass
class FileInput:
    id: str
    state: State
    message: str = ""
    retry_message: Optional[str] = ""
    max_attempts: int = 0
    extensions: str = ""
    size: Optional[int] = None
    optional: bool = False
    element_condition: str = "True"
    type: DialogElementType = DialogElementType.FILE_INPUT

    def __post_init__(self):
        if not self.retry_message:
            self.retry_message = self.message


@dataclass_json
@dataclass
class SetStateVariable:
    type: State
    key: int
    value_type: SetStateVariableValueType
    value: Union[str, float] = ""


@dataclass_json
@dataclass
class SetState:
    set_state_variables: list[SetStateVariable]
    element_condition: str = "True"
    type: DialogElementType = DialogElementType.SET_STATE


@dataclass_json
@dataclass
class Group:
    elements: list[
        Union[Message, Input, Form, Card, Action, Branch, FileInput, SetState]
    ]
    element_condition: str = "True"
    type: DialogElementType = DialogElementType.GROUP

    def __post_init__(self):
        """
        Apparently, Dialog.from_dict() does not deserialize individual dialog elements.
        This is a workaround to deserialize every element in the Dialog manually.
        """

        elements_deserialized = []
        for element_dict in self.elements:
            DialogElement = DIALOG_TYPE_MAPPING[element_dict["type"]]
            elements_deserialized.append(DialogElement.from_dict(element_dict))

        self.elements = elements_deserialized


DIALOG_TYPE_MAPPING = {
    DialogElementType.MESSAGE.value: Message,
    DialogElementType.INPUT.value: Input,
    DialogElementType.FORM.value: Form,
    DialogElementType.CARD.value: Card,
    DialogElementType.ACTION.value: Action,
    DialogElementType.BRANCH.value: Branch,
    DialogElementType.FILE_INPUT.value: FileInput,
    DialogElementType.SET_STATE.value: SetState,
    DialogElementType.GROUP.value: Group,
}


""" Dialog designer details
"""


@dataclass_json
@dataclass
class Dialog:
    name: str
    elements: list[
        Union[Message, Input, Form, Card, Action, Branch, FileInput, SetState, Group]
    ]
    description: str = ""
    has_feedback: bool = False

    def __post_init__(self):
        """
        Apparently, Dialog.from_dict() does not deserialize individual dialog elements.
        This is a workaround to deserialize every element in the Dialog manually.
        """

        elements_deserialized = []
        for element_dict in self.elements:
            DialogElement = DIALOG_TYPE_MAPPING[element_dict["type"]]
            elements_deserialized.append(DialogElement.from_dict(element_dict))

        self.elements = elements_deserialized


@dataclass_json
@dataclass
class Trigger:
    type: TriggerType
    target_name: str
    order: int
    regex: Optional[str] = None
    ignore_case: Optional[bool] = None  # only for type: regex
    intent: Optional[str] = None  # only for type: nlu


@dataclass_json
@dataclass
class DialogDesigner:
    dialogs: list[Dialog] = field(default_factory=list)
    triggers: list[Trigger] = field(default_factory=list)

    def __post_init__(self):
        self.triggers.sort(key=lambda x: x.order)


"""Settings, project and skill level
"""


@dataclass_json
@dataclass
class SkillSettings:
    triggers: list[str]


@dataclass_json
@dataclass
class CognibotSettings:
    """Project level common settings"""

    webservice_url: str = ""
    skill_settings: SkillSettings = field(
        default_factory=lambda: SkillSettings(triggers=[])
    )
    connector_url: str = ""
    token: str = ""
    speech_subscription_key: str = ""
    cancel_message: CancelMessage = field(
        default_factory=CancelMessage(
            type=MessageType.TEXT, message="Cancel Message", pattern=["cancel"]
        )
    )
    broadcast_message: BroadcastMessage = field(
        default_factory=lambda: BroadcastMessage(
            type=MessageType.NONE, message="", start="", end="", enabled=False
        )
    )
    handoff: Handoff = field(
        default_factory=lambda: Handoff(enabled=False, triggers=[], agents=[])
    )
    welcome_message: WelcomeMessage = field(
        default_factory=lambda: WelcomeMessage(
            type=MessageType.TEXT, message="Hi I am Cognibot.", enabled=True
        )
    )
    i18n: I18nSettings = field(
        default_factory=lambda: I18nSettings(
            default_language="en", enabled=True, triggers=["lang", "language"]
        )
    )


"""Project and skill details
"""


@dataclass_json
@dataclass
class Skill:
    name: str
    nlu: list[AIStudioProject]
    km: list[AIStudioProject]
    dialog_designer: DialogDesigner
    is_default: bool = False
    nlu_enabled: bool = False
    km_enabled: bool = False
    welcome_message: WelcomeMessage = field(
        default_factory=lambda: WelcomeMessage(
            type=MessageType.NONE, message="", enabled=False
        )
    )
    custom_trigger: CustomTrigger = field(
        default_factory=lambda: CustomTrigger(
            enabled=False, order=CustomTriggerOrder.NONE, function=""
        )
    )
    handoff: Handoff = field(
        default_factory=lambda: Handoff(
            agents=[],
            enabled=None,
            triggers=None,
        )
    )
    feedback: Feedback = field(
        default_factory=lambda: Feedback(
            enabled=False, dialog="", rating="", feedback=""
        )
    )


@dataclass_json
@dataclass
class Cognibot:
    cognibot_settings: CognibotSettings
    version: str
    skills: list[Skill]
    connections: list[Connection] = field(default_factory=list)
    credentials: list[Credential] = field(default_factory=list)
    nlu_settings: list[AIStudioNLU] = field(default_factory=list)
    km_settings: list[AIStudioKM] = field(default_factory=list)
    schedules: list[Schedule] = field(default_factory=list)


@dataclass_json
@dataclass
class CognibotJsonEnvelope:
    cognibot_json: str
    signature: str
    keygen: str
    key: str
