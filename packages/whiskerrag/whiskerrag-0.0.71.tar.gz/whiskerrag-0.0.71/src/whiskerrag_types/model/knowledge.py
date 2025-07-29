from datetime import datetime
from enum import Enum
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
    model_validator,
)

from whiskerrag_types.model.splitter import (
    BaseCharSplitConfig,
    GeaGraphSplitConfig,
    JSONSplitConfig,
    MarkdownSplitConfig,
    PDFSplitConfig,
    TextSplitConfig,
)
from whiskerrag_types.model.timeStampedModel import TimeStampedModel
from whiskerrag_types.model.utils import calculate_sha256


class MetadataSerializer:
    @staticmethod
    def deep_sort_dict(data: Union[Dict, List, Any]) -> Union[Dict, List, Any]:
        if isinstance(data, dict):
            return {
                k: MetadataSerializer.deep_sort_dict(data[k])
                for k in sorted(data.keys())
            }
        elif isinstance(data, list):
            return [MetadataSerializer.deep_sort_dict(item) for item in data]
        return data

    @staticmethod
    @lru_cache(maxsize=1024)
    def serialize(metadata: Optional[Dict]) -> Optional[Dict]:
        if metadata is None:
            return None
        sorted_metadata = MetadataSerializer.deep_sort_dict(metadata)
        return sorted_metadata if isinstance(sorted_metadata, dict) else None


class KnowledgeSourceEnum(str, Enum):
    """
    Specifies the source of knowledge, which influences the behavior of the resource loader
    """

    GITHUB_REPO = "github_repo"
    GITHUB_FILE = "github_file"
    USER_INPUT_TEXT = "user_input_text"
    CLOUD_STORAGE_TEXT = "cloud_storage_text"
    CLOUD_STORAGE_IMAGE = "cloud_storage_image"
    YUQUE = "yuque"


class GithubRepoSourceConfig(BaseModel):
    repo_name: str = Field(..., description="github repo url")
    branch: Optional[str] = Field(None, description="branch name of the repo")
    commit_id: Optional[str] = Field(None, description="commit id of the repo")
    auth_info: Optional[str] = Field(None, description="authentication information")


class GithubFileSourceConfig(GithubRepoSourceConfig):
    path: str = Field(..., description="path of the file in the repo")


class S3SourceConfig(BaseModel):
    bucket: str = Field(..., description="s3 bucket name")
    key: str = Field(..., description="s3 key")
    version_id: Optional[str] = Field(None, description="s3 version id")
    region: Optional[str] = Field(None, description="s3 region")
    access_key: Optional[str] = Field(None, description="s3 access key")
    secret_key: Optional[str] = Field(None, description="s3 secret key")
    auth_info: Optional[str] = Field(None, description="s3 session token")


class OpenUrlSourceConfig(BaseModel):
    url: str = Field(..., description="cloud storage url, such as oss, cos, etc.")


class OpenIdSourceConfig(BaseModel):
    id: str = Field(..., description="cloud storage file id, used for afts")


class YuqueSourceConfig(BaseModel):
    api_url: str = Field(
        default="https://www.yuque.com",
        description="the yuque api url",
    )
    group_login: str = Field(..., description="the yuque group id")
    book_slug: Optional[str] = Field(
        default=None,
        description="the yuque book id, if not set, will use the group all book",
    )
    document_id: Optional[Union[str, int]] = Field(
        default=None,
        description="the yuque document id in book, if not set, will use the book all doc",
    )
    auth_info: str = Field(..., description="authentication information")


class TextSourceConfig(BaseModel):
    text: str = Field(
        default="",
        min_length=1,
        max_length=30000,
        description="Text content, length range 1-30000 characters",
    )


class KnowledgeTypeEnum(str, Enum):
    """
    mime type of the knowledge. If multiple files are included and require a decomposer, please set the type to 'folder'
    """

    TEXT = "text"
    IMAGE = "image"
    MARKDOWN = "markdown"
    JSON = "json"
    DOCX = "docx"
    PDF = "pdf"
    QA = "qa"
    YUQUEDOC = "yuquedoc"
    FOLDER = "folder"


class EmbeddingModelEnum(str, Enum):
    OPENAI = "openai"
    # 轻量级
    ALL_MINILM_L6_V2 = "sentence-transformers/all-MiniLM-L6-v2"
    # 通用性能
    all_mpnet_base_v2 = "sentence-transformers/all-mpnet-base-v2"
    # 多语言
    PARAPHRASE_MULTILINGUAL_MINILM_L12_V2 = (
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    # 中文
    TEXT2VEC_BASE_CHINESE = "shibing624/text2vec-base-chinese"


KnowledgeSplitConfig = Union[
    BaseCharSplitConfig,
    MarkdownSplitConfig,
    TextSplitConfig,
    JSONSplitConfig,
    PDFSplitConfig,
    GeaGraphSplitConfig,
]

KnowledgeSourceConfig = Union[
    GithubRepoSourceConfig,
    GithubFileSourceConfig,
    S3SourceConfig,
    OpenUrlSourceConfig,
    TextSourceConfig,
    YuqueSourceConfig,
]


class Knowledge(TimeStampedModel):
    knowledge_id: str = Field(
        default_factory=lambda: str(uuid4()), description="knowledge id"
    )
    space_id: str = Field(
        ...,
        description="the space of knowledge, example: petercat bot id, github repo name",
    )
    tenant_id: str = Field(..., description="tenant id")
    knowledge_type: KnowledgeTypeEnum = Field(
        KnowledgeTypeEnum.TEXT, description="type of knowledge resource"
    )
    knowledge_name: str = Field(
        ..., max_length=255, description="name of the knowledge resource"
    )
    source_type: KnowledgeSourceEnum = Field(
        KnowledgeSourceEnum.USER_INPUT_TEXT, description="source type"
    )
    source_config: KnowledgeSourceConfig = Field(
        ...,
        description="source config of the knowledge",
    )
    embedding_model_name: Union[EmbeddingModelEnum, str] = Field(
        EmbeddingModelEnum.OPENAI,
        description="name of the embedding model. you can set any other model if target embedding service registered",
    )
    split_config: KnowledgeSplitConfig = Field(
        ...,
        description="configuration for splitting the knowledge",
    )
    file_sha: Optional[str] = Field(None, description="SHA of the file")
    file_size: Optional[int] = Field(None, description="size of the file")
    metadata: dict = Field({}, description="additional metadata, user can update it")
    retrieval_count: int = Field(default=0, description="count of the retrieval")
    parent_id: Optional[str] = Field(None, description="parent knowledge id")
    enabled: bool = Field(True, description="is knowledge enabled")

    model_config = ConfigDict(
        populate_by_name=True,
    )

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if (
            self.source_type == KnowledgeSourceEnum.USER_INPUT_TEXT
            and isinstance(self.source_config, TextSourceConfig)
            and self.source_config.text is not None
            and self.file_sha is None
        ):
            self.file_sha = calculate_sha256(self.source_config.text)
            self.file_size = len(self.source_config.text.encode("utf-8"))

    def update(self, **kwargs: Dict[str, Any]) -> "Knowledge":
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.now()
        return self

    @field_validator("enabled", mode="before")
    @classmethod
    def convert_tinyint_to_bool(cls, v: Any) -> bool:
        return bool(v)

    @model_validator(mode="before")
    def pre_process_data(cls, data: dict) -> dict:
        for field, value in data.items():
            if isinstance(value, UUID):
                data[field] = str(value)
        if isinstance(data, dict) and not data.get("knowledge_id"):
            data["knowledge_id"] = str(uuid4())

        return data

    @field_serializer("metadata")
    def serialize_metadata(self, metadata: dict) -> Optional[dict]:
        if metadata is None:
            return None
        sorted_metadata = MetadataSerializer.deep_sort_dict(metadata)
        return sorted_metadata if isinstance(sorted_metadata, dict) else None

    @field_serializer("knowledge_type")
    def serialize_knowledge_type(
        self, knowledge_type: Union[KnowledgeTypeEnum, str]
    ) -> str:
        if isinstance(knowledge_type, KnowledgeTypeEnum):
            return knowledge_type.value
        return str(knowledge_type)

    @field_serializer("source_type")
    def serialize_source_type(
        self, source_type: Union[KnowledgeSourceEnum, str]
    ) -> str:
        if isinstance(source_type, KnowledgeSourceEnum):
            return source_type.value
        return str(source_type)

    @field_serializer("embedding_model_name")
    def serialize_embedding_model_name(
        self, embedding_model_name: Union[EmbeddingModelEnum, str]
    ) -> str:
        if isinstance(embedding_model_name, EmbeddingModelEnum):
            return embedding_model_name.value
        return str(embedding_model_name)
