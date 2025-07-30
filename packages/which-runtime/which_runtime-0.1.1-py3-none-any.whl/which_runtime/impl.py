# -*- coding: utf-8 -*-

"""
Runtime refers to the specific computational environment in which your code
is executed. For example, running code on a local laptop, CI/CD build environments,
AWS EC2 instances, AWS Lambda functions, and more. Understanding the current runtime
is essential as it can impact how your code behaves.

For instance, when running your code on a local laptop, you might want to use
an AWS CLI named profile to access DevOps or workload AWS accounts. However,
in an application runtime like AWS Lambda, the default Boto session is typically
preconfigured for the current workload AWS account.

This Python module is designed to detect the current runtime information and
offers a set of ``is_xyz`` methods to assist you in crafting conditional logic
for performing different actions based on the runtime. Notably, many of these
methods employ the LAZY LOAD technique for efficiency.
"""

import os
import sys
import enum
from functools import cached_property

USER_RUNTIME_NAME = "USER_RUNTIME_NAME"


class RunTimeGroupEnum(str, enum.Enum):
    """
    Enumeration of common runtime groups in AWS projects.
    """

    local = "local"
    ci = "ci"
    app = "app"
    unknown = "unknown"


class RunTimeEnum(str, enum.Enum):
    """
    Enumeration of common runtime in AWS projects.
    """

    # local runtime group
    local = "local"
    aws_cloud9 = "aws_cloud9"
    # ci runtime group
    aws_codebuild = "aws_codebuild"
    github_action = "github_action"
    gitlab_ci = "gitlab_ci"
    bitbucket_pipeline = "bitbucket_pipeline"
    circleci = "circleci"
    jenkins = "jenkins"
    # app runtime group
    aws_lambda = "aws_lambda"
    aws_batch = "aws_batch"
    aws_glue = "aws_glue"
    aws_ec2 = "aws_ec2"
    aws_ecs = "aws_ecs"
    # special runtimes
    glue_container = "glue_container"
    unknown = "unknown"


runtime_emoji_mapper = {
    RunTimeEnum.local: "💻",
    RunTimeEnum.aws_cloud9: "💻",
    RunTimeEnum.aws_codebuild: "🏗",
    RunTimeEnum.github_action: "🏗",
    RunTimeEnum.gitlab_ci: "🏗",
    RunTimeEnum.bitbucket_pipeline: "🏗",
    RunTimeEnum.circleci: "🏗",
    RunTimeEnum.jenkins: "🏗",
    RunTimeEnum.aws_lambda: "🚀",
    RunTimeEnum.aws_batch: "🚀",
    RunTimeEnum.aws_glue: "🚀",
    RunTimeEnum.aws_ec2: "🚀",
    RunTimeEnum.aws_ecs: "🚀",
    RunTimeEnum.glue_container: "🗳",
    RunTimeEnum.unknown: "🤔",
}


def _check_user_env_var(expect: str) -> bool:
    """
    Users can manually set the runtime using the ``USER_RUNTIME_NAME`` environment variable
    to override the default detection rules.
    """
    return os.environ.get(USER_RUNTIME_NAME, "__unknown") == expect


class Runtime:
    """
    Detect the current runtime information by inspecting environment variables.

    The instance of this class is the entry point of all kinds of runtime related
    variables, methods.

    You can extend this class to add more runtime detection logic.
    """

    # --------------------------------------------------------------------------
    # detect if it is a specific runtime
    # --------------------------------------------------------------------------
    @cached_property
    def is_aws_codebuild(self) -> bool:
        """
        AWS CodeBuild is a fully managed continuous integration service that compiles source code,
        runs tests, and produces software packages ready for deployment. It eliminates the need to
        provision, manage, and scale your own build servers.

        Detection is primarily based on the presence of the ``CODEBUILD_BUILD_ID`` environment variable,
        which is automatically set in the AWS CodeBuild build environment.

        Reference:

        - https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-env-vars.html
        """
        if _check_user_env_var(RunTimeEnum.aws_codebuild.value):  # pragma: no cover
            return True
        return "CODEBUILD_BUILD_ID" in os.environ

    @cached_property
    def is_github_action(self) -> bool:
        """
        GitHub Actions is a continuous integration and continuous delivery (CI/CD) platform that
        allows you to automate your build, test, and deployment pipeline. It enables developers to
        create workflows that build and test every pull request to your repository.

        Detection relies on the presence of the ``GITHUB_ACTION`` environment variable, which is
        automatically set in GitHub Actions runner environments.

        Reference:

        - https://docs.github.com/en/actions/learn-github-actions/variables
        """
        if _check_user_env_var(RunTimeEnum.github_action.value):  # pragma: no cover
            return True
        return "GITHUB_ACTION" in os.environ

    @cached_property
    def is_gitlab_ci(self) -> bool:
        """
        Reference:

        - https://docs.gitlab.com/ee/ci/variables/predefined_variables.html
        """
        if _check_user_env_var(RunTimeEnum.gitlab_ci.value):  # pragma: no cover
            return True
        return "CI_PROJECT_ID" in os.environ

    @cached_property
    def is_bitbucket_pipeline(self) -> bool:
        """
        Bitbucket Pipelines is a continuous integration and continuous delivery (CI/CD) service
        built into Bitbucket Cloud. It allows developers to automatically build, test, and deploy
        their code based on a configuration file in their repository.

        Detection relies on the presence of the ``BITBUCKET_BUILD_NUMBER`` environment variable, which
        is automatically set in Bitbucket Pipeline environments.

        Reference:

        - https://support.atlassian.com/bitbucket-cloud/docs/variables-and-secrets/
        """
        if _check_user_env_var(
            RunTimeEnum.bitbucket_pipeline.value
        ):  # pragma: no cover
            return True
        return "BITBUCKET_BUILD_NUMBER" in os.environ

    @cached_property
    def is_circleci(self) -> bool:
        """
        CircleCI is a cloud-based continuous integration and continuous delivery (CI/CD) platform
        that automates the software development process, from code building to testing and deployment.

        Detection is based on the presence of the ``CIRCLECI`` environment variable, which is
        automatically set in CircleCI runner environments.

        Reference:

        - https://circleci.com/docs/variables/
        """
        if _check_user_env_var(RunTimeEnum.circleci.value):  # pragma: no cover
            return True
        return "CIRCLECI" in os.environ

    @cached_property
    def is_jenkins(self) -> bool:
        """
        Jenkins is an open-source automation server that supports building, deploying, and automating
        any software development project through continuous integration and continuous delivery (CI/CD).

        Detection relies on the presence of both ``BUILD_TAG`` and ``EXECUTOR_NUMBER`` environment
        variables, which are typically set in Jenkins build environments.

        Reference:

        - https://www.jenkins.io/doc/book/pipeline/jenkinsfile/#using-environment-variables
        """
        if _check_user_env_var(RunTimeEnum.jenkins.value):  # pragma: no cover
            return True
        return "BUILD_TAG" in os.environ and "EXECUTOR_NUMBER" in os.environ

    @cached_property
    def is_aws_lambda(self) -> bool:
        """
        AWS Lambda is a serverless compute service that lets you run code without provisioning or
        managing servers. It supports various programming languages and automatically scales your
        application by running code in response to each trigger.

        Detection is based on the presence of the ``AWS_LAMBDA_FUNCTION_NAME`` environment variable,
        which is automatically set in AWS Lambda function execution environments.

        Reference:

        - https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html
        """
        if _check_user_env_var(RunTimeEnum.aws_lambda.value):  # pragma: no cover
            return True
        return "AWS_LAMBDA_FUNCTION_NAME" in os.environ

    @cached_property
    def is_aws_batch(self) -> bool:
        """
        AWS Batch is a fully managed batch computing service that enables developers to easily and
        efficiently run hundreds of thousands of batch computing jobs on AWS. It dynamically provisions
        optimal quantity and type of compute resources based on job requirements.

        Detection relies on the presence of the ``AWS_BATCH_JOB_ID`` environment variable, which is
        automatically set in AWS Batch job environments.

        Reference:

        - https://docs.aws.amazon.com/batch/latest/userguide/job_env_vars.html
        """
        if _check_user_env_var(RunTimeEnum.aws_batch.value):  # pragma: no cover
            return True
        return "AWS_BATCH_JOB_ID" in os.environ

    @cached_property
    def is_aws_glue(self) -> bool:
        """
        AWS Glue is a fully managed extract, transform, and load (ETL) service that makes it easy to
        prepare and load data for analytics. It automatically provisions and manages the resources
        required for data transformation and movement.

        Detection is based on the presence of the ``--JOB_RUN_ID`` argument in system arguments, which
        is typically used in AWS Glue job environments.
        """
        if _check_user_env_var(RunTimeEnum.aws_glue.value):  # pragma: no cover
            return True
        return "--JOB_RUN_ID" in sys.argv

    @cached_property
    def is_aws_cloud9(self) -> bool:
        """
        AWS Cloud9 is a cloud-based integrated development environment (IDE) that lets you write,
        run, and debug code with just a web browser. It provides a complete development environment
        in the cloud, including a code editor, debugger, and terminal.

        Detection relies on the presence of the ``C9`` environment variable, which can be manually set
        in Cloud9 environments. Note that this method may not be stable. You can add the
        ``export C9=true`` to the ``~/.bashrc`` or ``~/.bash_profile`` to make it stable.

        Reference:

        - https://docs.aws.amazon.com/cloud9/latest/user-guide/env-vars.html
        """
        if _check_user_env_var(RunTimeEnum.aws_cloud9.value):  # pragma: no cover
            return True
        return "C9" in os.environ

    @cached_property
    def is_aws_ec2(self) -> bool:
        """
        Amazon EC2 (Elastic Compute Cloud) provides scalable computing capacity in the AWS cloud.
        It allows users to run virtual servers, known as instances, with various configurations and
        operating systems.

        Detection is based on a custom ``IS_AWS_EC2`` environment variable, as there's no standard
        built-in way to detect EC2 instances. You should set a custom environment variable
        for your ec2 instances to make it stable.
        """
        if _check_user_env_var(RunTimeEnum.aws_ec2.value):  # pragma: no cover
            return True
        return "IS_AWS_EC2" in os.environ

    @cached_property
    def is_aws_ecs(self) -> bool:
        """
        Amazon ECS (Elastic Container Service) is a fully managed container orchestration service
        that helps you easily deploy, manage, and scale containerized applications using Docker
        containers.

        Detection relies on a custom ``IS_AWS_ECS_TASK`` environment variable, as there's no standard
        built-in way to detect ECS task containers. You could set a custom environment variable
        for your ECS task to make it stable.

        Reference:

        - https://docs.aws.amazon.com/AmazonECS/latest/userguide/taskdef-envfiles.html
        """
        if _check_user_env_var(RunTimeEnum.aws_ecs.value):  # pragma: no cover
            return True
        return "IS_AWS_ECS_TASK" in os.environ

    @cached_property
    def is_glue_container(self) -> bool:
        """
        Glue container runtime refers to the specific environment used for running AWS Glue ETL jobs
        in a containerized setting. This provides additional flexibility in job execution and
        resource management.

        Detection is based on a custom ``IS_GLUE_CONTAINER`` environment variable set to 'true',
        as there's no standard built-in way to detect Glue containers. You could
        set a custom environment variable for your Glue container to make it stable.
        """
        if _check_user_env_var(RunTimeEnum.aws_ecs.value):  # pragma: no cover
            return True
        return os.environ.get("IS_GLUE_CONTAINER", "false") == "true"

    @cached_property
    def is_local(self) -> bool:
        """
        Local runtime represents a standard development environment on a personal computer or
        local workstation. It is the default runtime when no specific cloud or CI/CD environment
        is detected.

        Detection occurs by checking if none of the other specific runtime environments are active.
        Users can also manually set the runtime using the USER_RUNTIME_NAME environment variable
        to explicitly indicate a local runtime.
        """
        if _check_user_env_var(RunTimeEnum.local.value):  # pragma: no cover
            return True

        # or is a short-circuit operator, the performance is good
        flag = (
            self.is_aws_codebuild
            or self.is_github_action
            or self.is_gitlab_ci
            or self.is_bitbucket_pipeline
            or self.is_circleci
            or self.is_jenkins
            or self.is_aws_lambda
            or self.is_aws_batch
            or self.is_aws_glue
            or self.is_aws_cloud9
            or self.is_aws_ec2
            or self.is_aws_ecs
            or self.is_glue_container
        )
        return not flag

    @cached_property
    def current_runtime(self) -> str:  # pragma: no cover
        """
        Return the human friendly name of the current runtime.
        """
        if os.environ.get(USER_RUNTIME_NAME, "__unknown") != "__unknown":
            return os.environ[USER_RUNTIME_NAME]

        if self.is_aws_codebuild:
            return RunTimeEnum.aws_codebuild.value
        if self.is_github_action:
            return RunTimeEnum.github_action.value
        if self.is_gitlab_ci:
            return RunTimeEnum.gitlab_ci.value
        if self.is_bitbucket_pipeline:
            return RunTimeEnum.bitbucket_pipeline.value
        if self.is_circleci:
            return RunTimeEnum.circleci.value
        if self.is_jenkins:
            return RunTimeEnum.jenkins.value
        if self.is_aws_lambda:
            return RunTimeEnum.aws_lambda.value
        if self.is_aws_batch:
            return RunTimeEnum.aws_batch.value
        if self.is_aws_glue:
            return RunTimeEnum.aws_glue.value
        if self.is_aws_cloud9:
            return RunTimeEnum.aws_cloud9.value
        if self.is_aws_ec2:
            return RunTimeEnum.aws_ec2.value
        if self.is_aws_ecs:
            return RunTimeEnum.aws_ecs.value
        if self.is_glue_container:
            return RunTimeEnum.glue_container.value
        if self.is_local:
            return RunTimeEnum.local.value
        return RunTimeEnum.unknown.value

    # --------------------------------------------------------------------------
    # detect if it is a specific runtime group
    # --------------------------------------------------------------------------
    @cached_property
    def is_local_runtime_group(self) -> bool:
        """
        Local runtime group encompasses development environments where a developer has direct
        access to the local file system and operating system. This includes standard local machines
        and cloud-based development environments like AWS Cloud9.

        Detection is based on checking if the current runtime is either a local machine or an
        AWS Cloud9 environment.
        """
        return self.is_local or self.is_aws_cloud9

    @cached_property
    def is_ci_runtime_group(self) -> bool:  # pragma: no cover
        """
        CI (Continuous Integration) runtime group includes various automated build and testing
        environments used in software development workflows. These are platforms that automatically
        build, test, and validate code changes.

        Detection checks for the presence of any CI platform environment variables (CodeBuild,
        GitHub Actions, GitLab CI, etc.) or a generic 'CI' environment variable.
        """
        if (
            self.is_aws_codebuild
            or self.is_github_action
            or self.is_gitlab_ci
            or self.is_bitbucket_pipeline
            or self.is_circleci
            or self.is_jenkins
        ):
            return True
        else:
            return "CI" in os.environ

    @cached_property
    def is_app_runtime_group(self) -> bool:
        """
        Application runtime group includes cloud-based execution environments where application
        code is deployed and run. This covers various serverless and container-based platforms
        for running production applications.

        Detection checks if the current runtime is any of the supported application platforms
        like AWS Lambda, Batch, Glue, EC2, ECS, or Cloud9.
        """
        return (
            self.is_aws_lambda
            or self.is_aws_batch
            or self.is_aws_glue
            or self.is_aws_cloud9
            or self.is_aws_ec2
            or self.is_aws_ecs
        )

    @cached_property
    def current_runtime_group(self) -> str:  # pragma: no cover
        """
        Return the human friendly name of the current runtime group.
        """
        if self.is_ci_runtime_group:
            return RunTimeGroupEnum.ci.value
        if self.is_app_runtime_group:
            return RunTimeGroupEnum.app.value
        if self.is_local_runtime_group:
            return RunTimeGroupEnum.local.value
        return RunTimeGroupEnum.unknown.value


# A singleton object that can be used in your concrete project.
runtime = Runtime()
