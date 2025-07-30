from typing import List

from whiskerrag_types.interface import BaseDecomposer
from whiskerrag_types.model.knowledge import (
    GithubRepoSourceConfig,
    Knowledge,
    KnowledgeSourceEnum,
    KnowledgeTypeEnum,
    YuqueSourceConfig,
)
from whiskerrag_utils.helper.yuque import ExtendedYuqueLoader
from whiskerrag_utils.loader.github.repo_loader import (
    GitFileElementType,
    GithubRepoLoader,
)
from whiskerrag_utils.registry import RegisterTypeEnum, register


@register(RegisterTypeEnum.DECOMPOSER, KnowledgeTypeEnum.FOLDER)
class FolderDecomposer(BaseDecomposer):
    async def decompose(self) -> List[Knowledge]:
        results = []
        if self.knowledge.source_type == KnowledgeSourceEnum.GITHUB_REPO:
            results = await self.get_knowledge_list_from_github_repo(self.knowledge)
        if self.knowledge.source_type == KnowledgeSourceEnum.YUQUE:
            results = await self.get_knowledge_list_from_yuque(self.knowledge)
        return results

    async def get_knowledge_list_from_github_repo(
        self,
        knowledge: Knowledge,
    ) -> List[Knowledge]:
        if isinstance(knowledge.source_config, GithubRepoSourceConfig):
            repo_name = knowledge.source_config.repo_name
        else:
            raise TypeError(
                "source_config must be of type GithubRepoSourceConfig to access repo_name"
            )
        auth_info = knowledge.source_config.auth_info
        branch_name = knowledge.source_config.branch
        github_loader = GithubRepoLoader(repo_name, branch_name, auth_info)
        file_list: List[GitFileElementType] = github_loader.get_file_list()
        github_repo_list: List[Knowledge] = []
        for file in file_list:
            if not file.path.endswith((".md", ".mdx")):
                continue
            else:
                child_knowledge = Knowledge(
                    **knowledge.model_dump(
                        exclude={
                            "source_type",
                            "knowledge_type",
                            "knowledge_name",
                            "source_config",
                            "tenant_id",
                            "file_size",
                            "file_sha",
                            "metadata",
                            "parent_id",
                            "enabled",
                        }
                    ),
                    source_type=KnowledgeSourceEnum.GITHUB_FILE,
                    knowledge_type=KnowledgeTypeEnum.MARKDOWN,
                    knowledge_name=f"{file.repo_name}/{file.path}",
                    source_config={
                        **knowledge.source_config.model_dump(),
                        "path": file.path,
                    },
                    tenant_id=knowledge.tenant_id,
                    file_size=file.size,
                    file_sha=file.sha,
                    metadata={},
                    parent_id=knowledge.knowledge_id,
                    enabled=True,
                )
                github_repo_list.append(child_knowledge)
        return github_repo_list

    async def get_knowledge_list_from_yuque(
        self,
        knowledge: Knowledge,
    ) -> List[Knowledge]:
        source_config = knowledge.source_config
        if not isinstance(source_config, YuqueSourceConfig):
            raise TypeError("source_config must be of type YuqueSourceConfig")
        knowledge_list: List[Knowledge] = []
        document_id = source_config.document_id
        group_login = source_config.group_login
        book_slug = source_config.book_slug
        loader = ExtendedYuqueLoader(
            access_token=source_config.auth_info,
            api_url=source_config.api_url,
        )
        try:
            # Case 1: If document_id is provided, create single knowledge
            if document_id:
                if not book_slug:
                    raise ValueError("book_id is required when document_id is provided")
                doc_detail = loader.get_doc_detail(group_login, book_slug, document_id)
                knowledge_list.append(
                    Knowledge(
                        space_id=knowledge.space_id,
                        source_type=KnowledgeSourceEnum.YUQUE,
                        knowledge_type=KnowledgeTypeEnum.YUQUEDOC,
                        knowledge_name=doc_detail["title"],
                        split_config=knowledge.split_config.model_dump(),
                        source_config=source_config,
                        tenant_id=knowledge.tenant_id,
                        file_size=doc_detail.get(
                            "word_count"
                        ),  # You might want to calculate actual size
                        file_sha="",  # You might want to calculate actual sha
                        metadata={
                            "document_id": doc_detail.get("id"),
                            "format": doc_detail.get("format"),
                            "word_count": doc_detail.get("word_count"),
                        },
                        parent_id=knowledge.knowledge_id,
                        enabled=True,
                    )
                )

            # Case 2: If only book_id is provided, create knowledge for each document in the book
            elif book_slug:
                book_toc = loader.get_book_documents_by_path(group_login, book_slug)
                for doc_detail in book_toc:
                    doc_id = doc_detail.get("slug")
                    if doc_id is None:
                        continue
                    knowledge_list.append(
                        Knowledge(
                            space_id=knowledge.space_id,
                            source_type=KnowledgeSourceEnum.YUQUE,
                            knowledge_type=KnowledgeTypeEnum.YUQUEDOC,
                            knowledge_name=doc_detail.get("title", doc_id),
                            source_config=YuqueSourceConfig(
                                api_url=source_config.api_url,
                                group_login=group_login,
                                book_slug=book_slug,
                                document_id=doc_id,
                                auth_info=source_config.auth_info,
                            ),
                            split_config=knowledge.split_config.model_dump(),
                            tenant_id=knowledge.tenant_id,
                            file_size=0,
                            file_sha="",
                            metadata={"document_id": doc_id},
                            parent_id=knowledge.knowledge_id,
                            enabled=True,
                        )
                    )

            # Case 3: If only group_id is provided, get all books and their documents
            else:
                books = loader.get_books(user_id=loader.get_user_id())
                for book in books:
                    book_slug = book.get("slug")
                    if book_slug is None:
                        raise Exception(
                            f"can not get book slug   from knowledge:{knowledge.source_config}"
                        )
                    book_toc = loader.get_book_documents_by_path(group_login, book_slug)
                for doc_detail in book_toc:
                    doc_id = doc_detail.get("slug")
                    if doc_id is None:
                        continue
                    knowledge_list.append(
                        Knowledge(
                            space_id=knowledge.space_id,
                            source_type=KnowledgeSourceEnum.YUQUE,
                            knowledge_type=KnowledgeTypeEnum.YUQUEDOC,
                            knowledge_name=doc_detail.get("title", doc_id),
                            source_config=YuqueSourceConfig(
                                api_url=source_config.api_url,
                                group_login=group_login,
                                book_slug=book_slug,
                                document_id=doc_id,
                                auth_info=source_config.auth_info,
                            ),
                            split_config=knowledge.split_config.model_dump(),
                            tenant_id=knowledge.tenant_id,
                            file_size=0,
                            file_sha="",
                            metadata={"document_id": doc_id},
                            parent_id=knowledge.knowledge_id,
                            enabled=True,
                        )
                    )

            return knowledge_list

        except Exception as e:
            raise Exception(f"Failed to get knowledge list from Yuque: {e}")
