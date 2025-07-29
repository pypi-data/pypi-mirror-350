import base64
from typing import List, Optional

from github import Github

from whiskerrag_types.interface.loader_interface import BaseLoader
from whiskerrag_types.model.knowledge import (
    GithubFileSourceConfig,
    Knowledge,
    KnowledgeSourceEnum,
)
from whiskerrag_types.model.multi_modal import Text
from whiskerrag_utils.registry import RegisterTypeEnum, register


@register(RegisterTypeEnum.KNOWLEDGE_LOADER, KnowledgeSourceEnum.GITHUB_FILE)
class GithubFileLoader(BaseLoader[Text]):
    """
    Load a file from a GitHub repository.
    """

    knowledge: Knowledge
    path: str
    mode: str
    url: str
    branch: str
    repo_name: str
    size: int
    sha: str
    commit_id: Optional[str]
    github: Github

    def __init__(
        self,
        knowledge: Knowledge,
    ):
        self.knowledge = knowledge
        if not isinstance(knowledge.source_config, GithubFileSourceConfig):
            raise ValueError("source_config should be GithubFileSourceConfig")
        source_config: GithubFileSourceConfig = knowledge.source_config
        self.github = (
            Github(source_config.auth_info) if source_config.auth_info else Github()
        )
        self.repo_name = source_config.repo_name
        self.repo = self.github.get_repo(source_config.repo_name)
        self.branch = source_config.branch or self.repo.default_branch
        self.commit_id = source_config.commit_id or self._get_commit_id_by_branch(
            self.branch
        )
        self.path = source_config.path

    def _get_commit_id_by_branch(self, branch: str) -> str:
        branch_info = self.repo.get_branch(branch)
        return branch_info.commit.sha

    def _get_file_content_by_path(
        self,
    ) -> Text:
        try:
            file_content = (
                self.repo.get_contents(self.path, ref=self.commit_id)
                if self.commit_id
                else self.repo.get_contents(self.path)
            )
        except Exception as e:
            print(f"Failed to get file content: {e}")
            raise ValueError(
                f"Failed to get file content from {self.repo_name} with path {self.path}。error: {e}"
            )
        if isinstance(file_content, list):
            print("[warn]file_content is a list")
            file_content = file_content[0]
        self.sha = file_content.sha
        self.size = file_content.size
        return Text(
            content=base64.b64decode(file_content.content).decode("utf-8"),
            metadata={
                "path": file_content.path,
                "url": file_content.url,
                "branch": self.branch,
                "repo_name": self.repo_name,
                "size": self.size,
                "sha": self.sha,
            },
        )

    async def load(self) -> List[Text]:
        content = self._get_file_content_by_path()
        return [content]
