import os
from pathlib import Path
from typing import Optional

from .datasetargs import DatasetArgs
from .evaluatorargs import EvalMethodArgs


class EnvValidator:
    """
    Central environment variable validator for datasets and eval methods.
    Pulls dependencies dynamically from DatasetArgs and EvalMethodArgs.
    """

    @classmethod
    def validate(cls, dataset: Optional[str] = None, eval_name: Optional[str] = None):
        missing_vars = set()
        any_var_missing = []

        # ✅ Dataset env validation
        if dataset:
            dataset_enum = cls._resolve_dataset_enum(dataset)
            dataset_envs = DatasetArgs.DATASET_ENV_MAP.get(
                dataset_enum, {"all": [], "any": []}
            )
            print(
                f"🔍 Checking env vars for dataset '{dataset_enum.value}': {dataset_envs}"
            )

            missing_vars.update(cls._check_all(dataset_envs["all"]))
            if dataset_envs["any"] and not cls._check_any(dataset_envs["any"]):
                any_var_missing.append(
                    f"Dataset '{dataset_enum.value}' requires at least one of: {', '.join(dataset_envs['any'])}"
                )

        # ✅ Eval env validation
        if eval_name:
            eval_config = EvalMethodArgs.EVAL_CHOICES.get(eval_name.lower())
            if eval_config:
                eval_envs = eval_config.get("env_vars", [])
                print(f"🔍 Checking env vars for eval '{eval_name}': {eval_envs}")
                missing_vars.update(cls._check_all(eval_envs))

        # ✅ If missing, raise clean error
        if missing_vars or any_var_missing:
            message = []
            if missing_vars:
                message.append(
                    f"🚨 Missing environment variables: {', '.join(sorted(missing_vars))}"
                )
            if any_var_missing:
                message.append("🚨 " + " | ".join(any_var_missing))

            env_file = cls._find_env_file()
            if env_file:
                message.append(
                    f"\n💡 You can update your environment variables in: {env_file}"
                )
            else:
                message.append(
                    "\n💡 Consider creating a .env file to store environment variables."
                )

            raise EnvironmentError("\n".join(message))

        print("✅ Environment check passed.")

    @staticmethod
    def _check_all(vars_list):
        return {var for var in vars_list if not os.getenv(var)}

    @staticmethod
    def _check_any(vars_list):
        return any(os.getenv(var) for var in vars_list)

    @staticmethod
    def _find_env_file():
        possible_paths = [
            os.path.join(os.getcwd(), ".env"),
            os.path.join(str(Path.home()), ".dtx", ".env"),
            os.path.join(os.getcwd(), "config", ".env"),
        ]
        for path in possible_paths:
            if os.path.isfile(path):
                return path
        return None

    @staticmethod
    def _resolve_dataset_enum(dataset_input: str):
        dataset_input = dataset_input.strip().lower()
        dataset_enum = DatasetArgs.ALL_DATASETS.get(dataset_input)
        if not dataset_enum:
            raise ValueError(f"Unknown dataset '{dataset_input}'")
        return dataset_enum

    @classmethod
    def list_all_dependencies(cls):
        """Optional: List all datasets and eval env dependencies."""
        dependencies = {
            "datasets": {
                dataset.value: deps
                for dataset, deps in DatasetArgs.DATASET_ENV_MAP.items()
            },
            "evals": {
                name: config.get("env_vars", [])
                for name, config in EvalMethodArgs.EVAL_CHOICES.items()
            },
        }
        return dependencies
