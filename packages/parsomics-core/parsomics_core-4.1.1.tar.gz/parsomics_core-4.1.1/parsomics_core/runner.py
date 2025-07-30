import importlib
from pathlib import Path
import tomllib
from typing import Any

from sqlmodel import Session
from parsomics_core.configuration import ConfigurationReader
from parsomics_core.entities.workflow.assembly.models import Assembly, AssemblyDemand
from parsomics_core.entities.workflow.assembly.transactions import AssemblyTransactions
from parsomics_core.entities.workflow.metadata.models import Metadata, MetadataDemand
from parsomics_core.entities.workflow.metadata.transactions import MetadataTransactions
from parsomics_core.entities.workflow.progress import ProgressStatus
from parsomics_core.entities.workflow.project.models import Project, ProjectDemand
from parsomics_core.entities.workflow.project.transactions import ProjectTransactions
from parsomics_core.globals.database import engine, init_db
from parsomics_core.globals.environment import Environment
from parsomics_core.globals.logger import setup_logging
from parsomics_core.plugin_utils.plugin_initializer import PluginInitializer
from parsomics_core.populate import populate_all


class Runner:
    config: dict[str, Any]
    plugin_initializers: list[PluginInitializer] | None = None

    def __init__(self, config_file_path: Path | None = None):
        reader = ConfigurationReader(config_file_path)

        self.config = reader.config
        self.initialize_plugins()

    def initialize_plugins(self):
        plugins: list[str] = self.config["plugins"]

        # HACK: relies on the convention that source directories have the same name
        #       as their package, but replacing "-" with "_".
        #
        modules = [plugin.replace("-", "_") for plugin in plugins]

        plugin_initializers: list[PluginInitializer] = []
        for module in modules:
            imported = importlib.import_module(module)
            initializer = getattr(imported, "initializer")
            plugin_initializers.append(initializer)

        self.plugin_initializers = plugin_initializers

    @classmethod
    def _create_or_update(cls, transactions, demand_model):
        with Session(engine) as session:
            obj = transactions().demand(session, demand_model)
            obj.status = ProgressStatus.IN_PROGRESS
            session.commit()
            obj_key = obj.key

        return obj_key

    @classmethod
    def _finalize(cls, model, key):
        with Session(engine) as session:
            obj = session.get(model, key)
            if not obj:
                raise Exception(
                    f"Unexpectedly unable to get {model.__name__} with key {key}"
                )
            obj.status = ProgressStatus.DONE
            session.commit()

    def handle_config(self):
        # Create or update Metadata, and set status to IN_PROGRESS
        metadata_key: int = Runner._create_or_update(
            MetadataTransactions,
            MetadataDemand(),
        )

        for project_config in self.config["Project"]:
            self.handle_project_config(project_config)

        # Finalize Metadata, and set status to DONE
        Runner._finalize(Metadata, metadata_key)

    def handle_project_config(self, project_config: dict[str, Any]):
        # Create or update Project, and set status to IN_PROGRESS
        project_name: str = project_config["name"]
        project_config.pop("name")
        project_key: int = Runner._create_or_update(
            ProjectTransactions,
            ProjectDemand(name=project_name),
        )

        for assembly_config in project_config["Assembly"]:
            self.handle_assembly_config(assembly_config, project_key)

        # Finalize Project, and set status to DONE
        Runner._finalize(Project, project_key)

    def handle_assembly_config(self, assembly_config: dict[str, Any], project_key: int):
        assembly_name: str = assembly_config["name"]
        assembly_config.pop("name")

        # Create or update Assembly, and set status to IN_PROGRESS
        assembly_key: int = Runner._create_or_update(
            AssemblyTransactions,
            AssemblyDemand(project_key=project_key, name=assembly_name.upper()),
        )

        # Populate tables with all data from this Assembly
        populate_all(
            assembly_config, assembly_name, assembly_key, self.plugin_initializers
        )

        # Finalize Assembly, and set status to DONE
        Runner._finalize(Assembly, assembly_key)

    def run(self):
        # Initialize database
        init_db()

        # Parse the configuration and populate tables
        self.handle_config()
