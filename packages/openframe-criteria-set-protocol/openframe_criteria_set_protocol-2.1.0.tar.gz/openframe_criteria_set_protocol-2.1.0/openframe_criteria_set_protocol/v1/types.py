import datetime
import typing
from abc import ABC
from dataclasses import dataclass, field
from typing import Optional

from typing_extensions import deprecated

CertificationDefinitionType = typing.Literal['number', 'percentage']


@dataclass(slots=True)
class CertificationDefinition(ABC):
    code: str
    type: str
    name: str
    rules: Optional[ABC] = None
    rulesText: Optional[str] = None
    icon: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None


@dataclass(slots=True)
class NumberBasedCertificationDefinitionRules(ABC):
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    exclusiveMinimum: Optional[float] = None
    exclusiveMaximum: Optional[float] = None


PercentageBasedCertificationDefinitionRules = NumberBasedCertificationDefinitionRules


@dataclass(slots=True)
class NumberBasedCertificationDefinition(CertificationDefinition):
    type: CertificationDefinitionType = field(init=False, default='number')
    rules: NumberBasedCertificationDefinitionRules


@dataclass(slots=True)
class PercentageBasedCertificationDefinition(CertificationDefinition):
    type: CertificationDefinitionType = field(init=False, default='percentage')
    rules: PercentageBasedCertificationDefinitionRules


@dataclass(slots=True)
class RgbColor:
    red: int
    green: int
    blue: int


Color = typing.Union[RgbColor, str]


@dataclass(slots=True)
class ThemeStyle:
    primaryColor: Color
    secondaryColor: Color


@dataclass(slots=True)
class DocumentationItem(ABC):
    type: str
    label: str
    text: str
    url: Optional[str] = None


@dataclass(slots=True)
class PdfDocumentationItem(DocumentationItem):
    type: str = field(init=False, default='pdf')


@dataclass(slots=True)
class InlineDocumentationItem(DocumentationItem):
    type: str = field(init=False, default='text')


@dataclass(slots=True)
class LinkDocumentationItem(DocumentationItem):
    type: str = field(init=False, default='link')


TaskItemScalarValue = typing.Union[str, float, bool, None]
TaskItemValue = typing.Union[TaskItemScalarValue, list[TaskItemScalarValue]]
DefinitionType = typing.Literal['select-single', 'select-multiple', 'number', 'boolean']
TaskItemValueMap = dict[str, TaskItemValue]


@dataclass(slots=True)
class PointOption:
    value: TaskItemScalarValue
    text: str
    id: Optional[str] = None
    intro: Optional[str] = None
    outro: Optional[str] = None


@dataclass(slots=True)
class BaseTaskItemDefinition(ABC):
    type: DefinitionType = field(init=True)


@dataclass(slots=True)
class SelectSingleType(BaseTaskItemDefinition):
    type: DefinitionType = field(init=False, default='select-single')
    options: list[PointOption]
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    label: Optional[str] = None
    readOnly: Optional[bool] = None
    defaultValue: Optional[str] = None


@dataclass(slots=True)
class SelectMultipleType(BaseTaskItemDefinition):
    type: DefinitionType = field(init=False, default='select-multiple')
    options: list[PointOption]
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    label: Optional[str] = None
    readOnly: Optional[bool] = None
    defaultValue: Optional[list[str]] = None


@dataclass(slots=True)
class NumberType(BaseTaskItemDefinition):
    type: DefinitionType = field(init=False, default='number')
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    step: Optional[float] = None
    label: Optional[str] = None
    readOnly: Optional[bool] = None
    defaultValue: Optional[float] = None


@dataclass(slots=True)
class BooleanType(BaseTaskItemDefinition):
    type: DefinitionType = field(init=False, default='boolean')
    labels: Optional[dict[str, str]] = None
    label: Optional[str] = None
    readOnly: Optional[bool] = None
    defaultValue: Optional[bool] = None


TaskItemDefinition = typing.Union[SelectSingleType, SelectMultipleType, NumberType, BooleanType]
CriteriaTreeElementType = typing.Literal['theme', 'criterion', 'task-group', 'task', 'task-item']


@dataclass(slots=True)
class ThemeOptions:
    # @deprecated Use breadcrumbTextFormat instead, where
    # breadcrumbTextFormat = ':code:' if hideCode == False else ':title:'
    hideCode: Optional[bool] = None

    # @deprecated Use hideFromBreadcrumbs, hideFromDocumentTree and hideCodeInReport instead
    hideFromHierarchy: Optional[bool] = None

    # The format of the breadcrumb text, use ':code:' and ':title:' to define
    # where the code and/or title should be inserted
    breadcrumbTextFormat: Optional[str] = ":title:"

    # Whether to hide the theme from the breadcrumbs
    hideFromBreadcrumbs: Optional[bool] = False

    # Whether to hide the theme from the document tree structure
    hideFromDocumentTree: Optional[bool] = False

    # Whether to hide the theme code in the generated PDF report
    hideCodeInReport: Optional[bool] = False


@dataclass(slots=True)
class CriterionOptions:
    # @deprecated Use breadcrumbTextFormat instead, where
    # breadcrumbTextFormat = ':code:' if hideCode == False else ':title:'
    hideCode: Optional[bool] = None

    # @deprecated Use hideFromBreadcrumbs, hideFromDocumentTree and hideCodeInReport instead
    hideFromHierarchy: Optional[bool] = None

    # The format of the breadcrumb text, use ':code:' and ':title:' to define
    # where the code and/or title should be inserted
    breadcrumbTextFormat: Optional[str] = ":title:"

    # Whether to hide the criterion from the breadcrumbs
    hideFromBreadcrumbs: Optional[bool] = False

    # Whether to hide the criterion from the document tree structure
    hideFromDocumentTree: Optional[bool] = False

    # Whether to hide the criterion code in the generated PDF report
    hideCodeInReport: Optional[bool] = False


@dataclass(slots=True)
class TaskGroupOptions:
    # deprecated never used
    hideCode: Optional[bool] = None
    # deprecated never used
    hideFromHierarchy: Optional[bool] = None


@dataclass(slots=True)
class TaskOptions:
    # @deprecated use breadcrumbTextFormat instead, where
    # breadcrumbTextFormat = ':code:' if hideCode == False else ':title:', and
    # showCodeAsIndicatorTaskViewTitle, where showCodeAsIndicatorTaskViewTitle = not hideCode
    hideCode: Optional[bool] = None

    # The format of the breadcrumb text, use ':code:' and ':title:' to define where the code and/or title
    # should be inserted
    breadcrumbTextFormat: Optional[str] = ":title:"

    # Whether the title of the indicator task view should show the task code, or the hardcoded description text
    showCodeAsIndicatorTaskViewTitle: Optional[bool] = False


@dataclass(slots=True)
class TaskItemOptions:
    # Whether to exclude this task item from the targets page altogether
    excludeFromTargets: Optional[bool] = None



class ElementData(typing.TypedDict):
    value: Optional[TaskItemValue]
    text: Optional[str]
    type: Optional[typing.Literal['number', 'percentage']]
    text: Optional[str]
    maximumValue: Optional[float]
    minimumValue: Optional[float]
    exclusiveMaximum: Optional[float]
    exclusiveMinimum: Optional[float]
    step: Optional[float]
    total: Optional[float]
    readOnly: Optional[bool]


class TaskItemData(ElementData):
    valueReference: Optional[TaskItemValue]


@dataclass(slots=True)
class TaskItem:
    type: CriteriaTreeElementType = field(init=False, default='task-item')
    code: str
    definition: TaskItemDefinition
    tags: Optional[list] = None
    documentation: Optional[list[DocumentationItem]] = None
    description: Optional[str] = None
    data: Optional[TaskItemData] = None
    sortOrder: Optional[int] = None
    options: Optional[TaskItemOptions] = None


@dataclass(slots=True)
class Task:
    type: CriteriaTreeElementType = field(init=False, default='task')
    code: str
    title: str
    longFormTitle: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[list] = None
    documentation: Optional[list[DocumentationItem]] = None
    description: Optional[str] = None
    items: list[TaskItem] = field(default_factory=list)
    data: Optional[ElementData] = None
    sortOrder: Optional[int] = None
    options: Optional[TaskOptions] = None


@dataclass(slots=True)
class TaskGroup:
    type: CriteriaTreeElementType = field(init=False, default='task-group')
    code: str
    title: str
    longFormTitle: Optional[str] = None
    tags: Optional[list] = None
    documentation: Optional[list[DocumentationItem]] = None
    description: Optional[str] = None
    items: list[Task] = field(default_factory=list)
    data: Optional[ElementData] = None
    sortOrder: Optional[int] = None
    options: Optional[TaskGroupOptions] = None


@dataclass(slots=True)
class Criterion:
    type: CriteriaTreeElementType = field(init=False, default='criterion')
    code: str
    title: str
    longFormTitle: Optional[str] = None
    tags: Optional[list] = None
    documentation: Optional[list[DocumentationItem]] = None
    items: list[TaskGroup] = field(default_factory=list)
    data: Optional[ElementData] = None
    sortOrder: Optional[int] = None
    options: Optional[CriterionOptions] = None


@dataclass(slots=True)
class Theme:
    type: CriteriaTreeElementType = field(init=False, default='theme')
    code: str
    title: str = None
    longFormTitle: Optional[str] = None
    tags: Optional[list] = None
    documentation: Optional[list[DocumentationItem]] = None
    items: list[Criterion] = field(default_factory=list)
    data: Optional[ElementData] = None
    style: Optional[ThemeStyle] = None
    sortOrder: Optional[int] = None
    options: Optional[ThemeOptions] = None


@dataclass(slots=True)
class CriteriaTree:
    version: str
    themes: list[Theme] = field(init=False, default_factory=list)
    result: any = None
    certifications: Optional[list[str]] = None
    certificationDefinitions: Optional[list[CertificationDefinition]] = None


CriteriaTreeElement = typing.Union[Theme, Criterion, TaskGroup, Task, TaskItem]


SchemaDefinition = dict[str, typing.Any]


@dataclass(slots=True)
class SchemaDefinitions:
    parameters: Optional[SchemaDefinition] = None
    result: Optional[SchemaDefinition] = None


@dataclass(slots=True)
class Metadata:
    id: str
    version: str
    date: datetime.datetime
    name: str
    description: str
    documentation: str
    locales: Optional[list[str]] = None
    defaultLocale: Optional[str] = None
    schemas: Optional[SchemaDefinitions] = None


@dataclass(slots=True)
class DataMap:
    version: str
    elements: dict[str, any]
    result: any = None
    certifications: Optional[list[str]] = None


MetadataResponse = Metadata
DataMapResponse = DataMap
CriteriaSetsAndVersions = dict[str, list[Metadata]]


@dataclass
class CriteriaTreeResponse(CriteriaTree):
    pass


@dataclass(slots=True)
class StreamMatrixResponse:
    filename: str
    content_type: str
    path: str


@dataclass(slots=True)
class CriteriaSetOptions:
    renderDetailedViewInDashboard: Optional[bool] = None
