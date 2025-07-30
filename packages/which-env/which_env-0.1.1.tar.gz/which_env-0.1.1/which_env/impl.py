# -*- coding: utf-8 -*-

"""
Multi-Environment Deployment Strategy Management.

This module provides a comprehensive framework for managing multi-environment
deployment strategies in Python applications. It enables developers to define
custom environment enumerations and automatically detect the current runtime
environment based on various runtime contexts and environment variables.

- 🔧 **devops**: Foundation environment for building code, conducting unit tests,
    and creating artifacts. Not used for application deployment.
- 🧰 **sbx101, 102, 103**: Sandbox environments for temporary development/testing,
    allowing multiple engineers to work on different branches concurrently without
    interference. Named with convention 'sbx-${number}' for easy provisioning/destruction.
- 💻 **dev**: Development environment for active development work.
- 🧪 **tst**: Durable test environment for integration and end-to-end testing,
    including high-risk tests like load/stress testing that could compromise
    system integrity.
- 🎸 **stg**: Staging environment mirroring production conditions for QA testing
    under realistic workloads. Outputs captured for analysis, not visible to end users.
- 👮 **qa**: Isolated environment allowing external QA collaborators to work on
    testing without affecting other environments or having access to sensitive systems.
- 🚦 **preprd**: Pre-production environment with production data but isolated from
    end user traffic, enabling high-risk changes and debugging with real data.
- 🏭 **prd**: Production environment serving end-users directly, with immutable
    artifact versioning for quick rollbacks.
"""

import typing as T
import os
import string

from which_runtime.api import Runtime, runtime as runtime_
from enum_mate.api import BetterStrEnum


USER_ENV_NAME = "USER_ENV_NAME"
ENV_NAME = "ENV_NAME"

LOWER_CASE_CHARSET = set(string.ascii_lowercase)
ENV_NAME_CHARSET = set(string.ascii_lowercase + string.digits)


class EnvNameValidationError(ValueError):
    """
    Raised when an environment name fails validation rules.
    """


def validate_env_name(env_name: str):  # pragma: no cover
    """
    Validate environment name against naming conventions.

    Environment names must follow specific naming conventions:

    - First character must be lowercase letter (a-z)
    - Remaining characters can be lowercase letters or digits (a-z, 0-9)
    - No special characters, spaces, or uppercase letters allowed

    :param env_name: The environment name to validate

    :raises EnvNameValidationError: If the environment name violates naming rules
    """
    if env_name[0] not in LOWER_CASE_CHARSET:
        raise EnvNameValidationError(
            f"{env_name!r} is an invalid env name, "
            f"first letter of env_name has to be a-z!"
        )
    if len(set(env_name).difference(ENV_NAME_CHARSET)):
        raise EnvNameValidationError(
            f"{env_name!r} is an invalid env name, " f"env_name can only has a-z, 0-9"
        )


class CommonEnvNameEnum(BetterStrEnum):
    """
    Standard environment name enumeration following industry best practices.

    Provides consistent naming for common deployment environments used across
    software development lifecycles. These names follow the aws_ops_alpha
    pattern and are widely recognized in DevOps practices.
    """

    devops = "devops"  # DevOps/CI environment for builds and testing
    sbx = "sbx"  # Sandbox environment for experimental development
    dev = "dev"  # Development environment for active coding
    tst = "tst"  # Test environment for integration testing
    stg = "stg"  # Staging environment for pre-production validation
    qa = "qa"  # Quality Assurance environment for QA team testing
    preprd = "preprd"  # Pre-production environment for final validation
    prd = "prd"  # Production environment for live user traffic


env_emoji_mapper = {
    CommonEnvNameEnum.devops.value: "🛠",
    CommonEnvNameEnum.sbx.value: "🧰",
    CommonEnvNameEnum.dev.value: "💻",
    CommonEnvNameEnum.tst.value: "🧪",
    CommonEnvNameEnum.stg.value: "🎸",
    CommonEnvNameEnum.qa.value: "👮",
    CommonEnvNameEnum.preprd.value: "🚦",
    CommonEnvNameEnum.prd.value: "🏭",
}


class BaseEnvNameEnum(BetterStrEnum):
    """
    Base class for defining custom environment name enumerations.

    This class provides the foundation for creating project-specific environment
    enumerations while enforcing validation rules and providing utility methods.
    All custom environment enumerations must inherit from this class and follow
    the established patterns.

    **Required Environments:**

    Every custom enumeration must define at least three environments:

    1. **devops**: Build and CI/CD environment (not for deployment)
    2. **dev**: Development environment for active coding and testing
    3. **prd**: Production environment for live user traffic

    1. Validation of environment names.
    2. Iteration over all available environment names.

    To define your own environment name enumerations class, you need to subclass
    this class. However, there are some restrictions:

    1. You cannot create a "devops" environment as it does not qualify as a workload environment.
    1. You must include at least a "devops", a "dev" (development) environment
        and a "prd" (production) environment.
    2. environment name has to be lower case, without

    **Validation Rules:**

    - Environment names must be lowercase with digits only (a-z, 0-9)
    - First character must be a letter (a-z)
    - No special characters, spaces, or uppercase letters
    - Must include required environments (devops, dev, prd)

    **Usage Pattern:**

    1. Inherit from BaseEnvNameEnum
    2. Define environment constants
    3. Call validate() to ensure compliance
    4. Use with detect_current_env() for runtime detection
    """

    @classmethod
    def validate(cls):
        """
        Validate that the enumeration follows required patterns and naming rules.

        Ensures the custom enumeration includes all required environments and
        that all environment names follow the established naming conventions.
        This method should be called after defining a custom enumeration to
        catch configuration errors early.

        **Validation Checks:**

        1. **Required Environments**: Must include 'devops', 'dev', and 'prd'
        2. **Naming Convention**: All names must follow validate_env_name() rules
        """
        if (
            cls.is_valid_value(CommonEnvNameEnum.devops.value) is False
            or cls.is_valid_value(CommonEnvNameEnum.dev.value) is False
            or cls.is_valid_value(CommonEnvNameEnum.prd.value) is False
        ):
            raise EnvNameValidationError(
                f"you have to define at least "
                f"a {CommonEnvNameEnum.devops.value!r}, "
                f"a {CommonEnvNameEnum.dev.value!r}, "
                f"and a {CommonEnvNameEnum.prd.value!r} environment,"
                f"you only have {list(cls)}."
            )
        for env_name in cls:
            validate_env_name(env_name.value)

    @classmethod
    def get_devops(cls):
        """
        Get the DevOps environment reference from the enumeration.
        """
        return cls.devops

    @classmethod
    def get_dev(cls):
        """
        Get the Development environment reference from the enumeration.
        """
        return cls.dev

    @classmethod
    def get_prd(cls):
        """
        Get the Production environment reference from the enumeration.
        """
        return cls.prd

    @property
    def emoji(self) -> str:
        """
        et the emoji representation of this environment.

        Provides a visual identifier for the environment that can be used
        in logging, user interfaces, or documentation to quickly identify
        the environment context.
        """
        return env_emoji_mapper[self.value]


def detect_current_env(
    env_name_enum_class: T.Union[BaseEnvNameEnum, T.Type[BaseEnvNameEnum]],
    runtime: T.Optional[Runtime] = None,
) -> str:  # pragma: no cover
    """
    Intelligently detect the current environment name based on runtime context.

    This function implements a sophisticated environment detection strategy that
    adapts to different runtime contexts (local development, CI/CD, production apps)
    and provides sensible defaults while allowing explicit overrides.

    **Detection Strategy:**

    The detection logic follows a priority-based approach designed to handle
    common deployment patterns while maintaining flexibility:

    1. **Local Development Runtime** (laptop, workstation):
        - **Default**: 'dev' environment (assumption: developers usually work in dev)
        - **Override**: USER_ENV_NAME environment variable allows switching contexts
        - **Use Case**: Developer testing different environment configurations locally
    2. **CI/CD Runtime** (GitHub Actions, Jenkins, etc.):
        - **Priority 1**: USER_ENV_NAME (manual override for special cases)
        - **Priority 2**: ENV_NAME (standard CI environment specification)
        - **Use Case**: Automated deployments to different target environments
    3. **Application Runtime** (deployed applications):
        - **Priority 1**: USER_ENV_NAME (operational override capability)
        - **Priority 2**: ENV_NAME (deployment-time environment specification)
        - **Use Case**: Production applications that need environment context

    **Design Rationale:**

    **Why Two Environment Variables?**

    - ``ENV_NAME``: **System-level** environment specification set by deployment
        infrastructure, CI/CD pipelines, or container orchestration. This represents
        the "official" environment designation.
    - ``USER_ENV_NAME``: **User-level** override for operational flexibility.
        Allows developers, DevOps engineers, or applications to temporarily
        override the environment context without changing infrastructure.

    **Why Default to 'dev' Locally?**

    - **Developer Experience**: Most local development work happens in dev context
    - **Safety**: Prevents accidental production operations from local machines
    - **Flexibility**: Easy override with USER_ENV_NAME when needed


    :param runtime: Runtime context detector from which_runtime package.
        Determines whether code is running locally, in CI, or in production.
    :param env_name_enum_class: Custom environment enumeration class inheriting
        from :class:`BaseEnvNameEnum`. Defines valid environments for the project.
    """
    # Validate the implementation of the enum.
    env_name_enum_class.validate()

    if runtime is None: # pragma: no cover
        runtime = runtime_

    if runtime.is_local_runtime_group:
        if os.environ.get(USER_ENV_NAME):
            return os.environ[USER_ENV_NAME]
        return env_name_enum_class.get_dev().value
    elif (
        runtime.is_ci_runtime_group
        or runtime.is_app_runtime_group
        or runtime.is_glue_container
    ):
        if os.environ.get(USER_ENV_NAME):
            env_name = os.environ[USER_ENV_NAME]
        else:
            env_name = os.environ[ENV_NAME]
        env_name_enum_class.ensure_is_valid_value(env_name)
        return env_name
    else:  # pragma: no cover
        raise NotImplementedError
