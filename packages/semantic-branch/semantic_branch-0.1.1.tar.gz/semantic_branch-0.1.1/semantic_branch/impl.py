# -*- coding: utf-8 -*-

"""
This module provides a comprehensive system for working with semantic git branch names.
Semantic branches follow a structured naming convention that helps indicate the purpose
and type of work being done on a branch, enabling both developers and CI/CD systems
to understand and process branches appropriately.

Semantic Git Branch Name Format

semantic git branch name format::

    ${semantic_name}-${optional_marker}/${description}/${more_slash_is_ok}

Sample valid semantic git branch name syntax::

    main
    feature
    feature/add-this-feature
    feature-123/description
    release/1.2.3

Usage example::

    import fixa.semantic_branch as sem_branch

    _ = sem_branch.InvalidSemanticNameError
    _ = sem_branch.SemanticBranchEnum
    _ = is_valid_semantic_name
    _ = ensure_is_valid_semantic_name
    _ = sem_branch.is_certain_semantic_branch
    _ = sem_branch.is_main_branch
    _ = sem_branch.is_feature_branch
    _ = sem_branch.is_build_branch
    _ = sem_branch.is_doc_branch
    _ = sem_branch.is_fix_branch
    _ = sem_branch.is_release_branch
    _ = sem_branch.is_cleanup_branch
    _ = sem_branch.is_sandbox_branch
    _ = sem_branch.is_develop_branch
    _ = sem_branch.is_test_branch
    _ = sem_branch.is_int_branch
    _ = sem_branch.is_staging_branch
    _ = sem_branch.is_qa_branch
    _ = sem_branch.is_preprod_branch
    _ = sem_branch.is_prod_branch
    _ = sem_branch.is_blue_branch
    _ = sem_branch.is_green_branch
    _ = sem_branch.SemanticBranchRule
"""

import typing as T
import enum
import string
import dataclasses
from functools import cache


class InvalidSemanticNameError(ValueError):
    """
    Exception raised when a semantic name doesn't meet validation requirements.
    """


lower_case_charset = set(string.ascii_lowercase)
semantic_name_charset = set(string.ascii_lowercase + string.digits)


def is_valid_semantic_name(name: str) -> bool:
    """
    Check if a name is a valid semantic name.

    A valid semantic name must:

    1. Not be empty
    2. Start with a lowercase letter (a-z)
    3. Contain only lowercase letters and digits

    :param name: The name to validate

    Examples::

        # Valid semantic names
        assert is_valid_semantic_name("feature") is True
        assert is_valid_semantic_name("feat") is True
        assert is_valid_semantic_name("test123") is True
        assert is_valid_semantic_name("build2") is True

        # Invalid semantic names
        assert is_valid_semantic_name("") is False  # Empty
        assert is_valid_semantic_name("Feature") is False  # Uppercase
        assert is_valid_semantic_name("123test") is False  # Starts with digit
        assert is_valid_semantic_name("feature-123") is False  # Contains dash:return: True if the name is valid, False otherwise
    """
    if len(name) == 0:
        return False
    if name[0] not in lower_case_charset:
        return False
    return len(set(name).difference(semantic_name_charset)) == 0


def ensure_is_valid_semantic_name(name: str) -> str:  # pragma: no cover
    """
    Validate a semantic name and raise an exception if invalid.

    This function performs the same validation as :func:`is_valid_semantic_name`
    but raises an :class:`InvalidSemanticNameError` if the name is invalid,
    otherwise returns the name unchanged.
    """
    if is_valid_semantic_name(name) is False:
        raise InvalidSemanticNameError(f"{name!r} is not a valid semantic name")
    return name


def is_certain_semantic_branch(name: str, stubs: T.List[str]) -> bool:
    """
    Test if a branch name matches any of the provided semantic stubs.

    This function extracts the semantic portion from a branch name by removing
    everything after the first occurrence of separators (``-``, ``_``, ``@``, ``+``, ``/``),
    then checks if it matches any of the provided semantic stubs.

    The matching is case-insensitive and handles leading/trailing whitespace.
    All provided stubs must be valid semantic names (validated automatically).

    :param name: The git branch name to test
    :param stubs: List of valid semantic stub names to match against

    :return: True if the branch name matches any stub, False otherwise

    :raises InvalidSemanticNameError: If any stub in the list is invalid

    Examples::

        # Basic matching
        assert is_certain_semantic_branch("feature", ["feat", "feature"]) is True
        assert is_certain_semantic_branch("feat", ["feat", "feature"]) is True

        # Case insensitive matching
        assert is_certain_semantic_branch("FEATURE", ["feat", "feature"]) is True
        assert is_certain_semantic_branch("Feat", ["feat", "feature"]) is True

        # Separator handling
        assert is_certain_semantic_branch("feature-123", ["feat", "feature"]) is True
        assert is_certain_semantic_branch("feature/add-login", ["feat", "feature"]) is True
        assert is_certain_semantic_branch("feature_test", ["feat", "feature"]) is True
        assert is_certain_semantic_branch("feature@urgent", ["feat", "feature"]) is True
        assert is_certain_semantic_branch("feature+new", ["feat", "feature"]) is True

        # Combined separators (processed in order)
        assert is_certain_semantic_branch("feature-123/description", ["feat", "feature"]) is True

        # Whitespace handling
        assert is_certain_semantic_branch(" feature ", ["feat", "feature"]) is True

        # No match
        assert is_certain_semantic_branch("main", ["feat", "feature"]) is False

        # Invalid stub raises exception
        try:
            is_certain_semantic_branch("feature", ["Feature"])  # Invalid: uppercase
        except InvalidSemanticNameError:
            print("Invalid stub provided")
    """
    name = name.lower().strip()
    name = name.split("/")[0]
    name = name.split("-")[0]
    name = name.split("_")[0]
    name = name.split("@")[0]
    name = name.split("+")[0]
    stubs = set([ensure_is_valid_semantic_name(stub.lower().strip()) for stub in stubs])
    return name in stubs


class SemanticStubEnum(str, enum.Enum):
    """
    Enumeration of all supported semantic branch stub names.

    This enum defines all the standard semantic stub names that can be used
    to identify different types of branches. Each stub is a short, lowercase
    string that represents a specific branch purpose or environment.
    """

    # Essential stubs
    main = "main"
    master = "master"

    # Use case based stubs
    feat = "feat"
    feature = "feature"
    build = "build"
    doc = "doc"
    fix = "fix"
    hotfix = "hotfix"
    rls = "rls"
    release = "release"
    clean = "clean"
    cleanup = "cleanup"

    # Environment based stubs
    sbx = "sbx"
    sandbox = "sandbox"
    dev = "dev"
    develop = "develop"
    tst = "tst"
    test = "test"
    int = "int"
    stg = "stg"
    stage = "stage"
    staging = "staging"
    qa = "qa"
    preprod = "preprod"
    prd = "prd"
    prod = "prod"
    blue = "blue"
    green = "green"


@dataclasses.dataclass
class SemanticBranch:
    """
    Data class representing a semantic branch type with its associated stub names.

    This class encapsulates a semantic branch type by combining a canonical name
    with a list of stub names that can be used to identify branches of this type.
    It provides a convenient interface for testing whether a given branch name
    matches this semantic branch type.

    :param name: The canonical name of this semantic branch type
    :param stubs: List of semantic stub names that identify this branch type
    """
    name: str = dataclasses.field()
    stubs: list[str] = dataclasses.field()

    def __post_init__(self):
        self.name = ensure_is_valid_semantic_name(self.name)
        self.stubs = [
            ensure_is_valid_semantic_name(stub)
            for stub in self.stubs
        ]

    def is_match(self, git_branch_name: str) -> bool:
        """
        Test if a git branch name matches this semantic branch type.

        This method uses the :func:`is_certain_semantic_branch` function
        to determine if the provided branch name matches any of the stubs
        associated with this semantic branch type.

        :param git_branch_name: The git branch name to test

        :return: True if the branch name matches this semantic type, False otherwise

        :raises InvalidSemanticNameError: If any of the stubs are invalid
        """
        return is_certain_semantic_branch(
            name=git_branch_name,
            stubs=self.stubs,
        )


class SemanticBranchEnum(enum.Enum):
    """
    Enumeration of all standard semantic branch types.

    This enum provides pre-configured :class:`SemanticBranch` instances for all
    standard semantic branch types. Each enum value contains a SemanticBranch
    object with the appropriate canonical name and list of semantic stubs.

    This enum serves as the primary interface for semantic branch detection,
    providing a convenient way to access standardized semantic branch
    configurations without having to manually create SemanticBranch instances.
    """
    main = SemanticBranch(
        name="main",
        stubs=[
            SemanticStubEnum.main.value,
            SemanticStubEnum.master.value,
        ],
    )
    feature = SemanticBranch(
        name="feature",
        stubs=[
            SemanticStubEnum.feat.value,
            SemanticStubEnum.feature.value,
        ],
    )
    build = SemanticBranch(
        name="build",
        stubs=[
            SemanticStubEnum.build.value,
        ],
    )
    doc = SemanticBranch(
        name="doc",
        stubs=[
            SemanticStubEnum.doc.value,
        ],
    )
    fix = SemanticBranch(
        name="fix",
        stubs=[
            SemanticStubEnum.fix.value,
            SemanticStubEnum.hotfix.value,
        ],
    )
    release = SemanticBranch(
        name="release",
        stubs=[
            SemanticStubEnum.rls.value,
            SemanticStubEnum.release.value,
        ],
    )
    cleanup = SemanticBranch(
        name="cleanup",
        stubs=[
            SemanticStubEnum.clean.value,
            SemanticStubEnum.cleanup.value,
        ],
    )
    sandbox = SemanticBranch(
        name="sandbox",
        stubs=[
            SemanticStubEnum.sbx.value,
            SemanticStubEnum.sandbox.value,
        ],
    )
    develop = SemanticBranch(
        name="develop",
        stubs=[
            SemanticStubEnum.dev.value,
            SemanticStubEnum.develop.value,
        ],
    )
    test = SemanticBranch(
        name="test",
        stubs=[
            SemanticStubEnum.tst.value,
            SemanticStubEnum.test.value,
        ],
    )
    int = SemanticBranch(
        name="int",
        stubs=[
            SemanticStubEnum.int.value,
        ],
    )
    staging = SemanticBranch(
        name="staging",
        stubs=[
            SemanticStubEnum.stg.value,
            SemanticStubEnum.stage.value,
            SemanticStubEnum.staging.value,
        ],
    )
    qa = SemanticBranch(
        name="qa",
        stubs=[
            SemanticStubEnum.qa.value,
        ],
    )
    preprod = SemanticBranch(
        name="preprod",
        stubs=[
            SemanticStubEnum.preprod.value,
        ],
    )
    prod = SemanticBranch(
        name="prod",
        stubs=[
            SemanticStubEnum.prd.value,
            SemanticStubEnum.prod.value,
        ],
    )
    blue = SemanticBranch(
        name="blue",
        stubs=[
            SemanticStubEnum.blue.value,
        ],
    )
    green = SemanticBranch(
        name="green",
        stubs=[
            SemanticStubEnum.green.value,
        ],
    )
