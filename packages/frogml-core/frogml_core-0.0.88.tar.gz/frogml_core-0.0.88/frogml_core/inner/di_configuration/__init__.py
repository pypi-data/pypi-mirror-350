import os

from .account import UserAccountConfiguration
from .containers import FrogmlContainer


def wire_dependencies():
    container = FrogmlContainer()

    default_config_file = os.path.join(os.path.dirname(__file__), "config.yml")
    container.config.from_yaml(default_config_file)

    from frogml_core.clients import (
        administration,
        alert_management,
        alerts_registry,
        analytics,
        audience,
        automation_management,
        autoscaling,
        batch_job_management,
        build_management,
        build_orchestrator,
        data_versioning,
        deployment,
        feature_store,
        file_versioning,
        instance_template,
        integration_management,
        kube_deployment_captain,
        logging_client,
        model_management,
        model_version_manager,
        project,
        prompt_manager,
        system_secret,
        user_application_instance,
        vector_store,
        workspace_manager,
        jfrog_gateway,
    )

    container.wire(
        packages=[
            administration,
            alert_management,
            audience,
            automation_management,
            autoscaling,
            analytics,
            batch_job_management,
            build_management,
            build_orchestrator,
            data_versioning,
            deployment,
            file_versioning,
            instance_template,
            kube_deployment_captain,
            logging_client,
            model_management,
            project,
            feature_store,
            user_application_instance,
            alerts_registry,
            workspace_manager,
            vector_store,
            integration_management,
            system_secret,
            prompt_manager,
            model_version_manager,
            jfrog_gateway,
        ]
    )

    return container
