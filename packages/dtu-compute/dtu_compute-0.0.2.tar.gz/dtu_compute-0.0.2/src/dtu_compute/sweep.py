from pathlib import Path

import sweeps

from dtu_compute.run_config import ConfigProcessor


def get_runs(config: dict, n: int = 10):
    """Generate a list of runs based on the provided configuration.

    Args:
        config: Configuration dictionary containing the sweep parameters.
        n: Number of runs to generate.

    """
    if "method" not in config:
        config["method"] = "random"

    method = config["method"]
    if method not in ["grid", "random"]:
        raise ValueError(f"Expected method to be 'grid' or 'random', got {method}")

    if "n_runs" in config:
        n = config["n_runs"]
        del config["n_runs"]

    runs: list[sweeps.SweepRun] = []
    for n in range(n):
        run = sweeps.next_run(config, runs=runs, validate=True)
        if run is None:  # grid search is done
            break
        run.state = sweeps.RunState.finished
        runs.append(run)

    params = [r.config for r in runs]
    return params


class SweepProcessor(ConfigProcessor):
    """Class to process a sweep configuration file and generate multiple job configurations."""

    def __init__(self, config_path: Path) -> None:
        """Initialize the SweepProcessor with a path to a config file."""
        super().__init__(config_path)

        self.sweep_config = self.config.pop("sweep", {})
        if not self.sweep_config:
            raise ValueError("No sweep configuration found in the provided config file.")

    def process(self) -> None:
        """Process the config by substituting placeholders and sampling the sweep parameters."""
        super().process()  # fill in substitutions
        processed_config = self.processed_config.copy()

        # Sample the sweep parameters
        params = get_runs(self.sweep_config)

        # Substitute the sampled parameters into the processed config
        self.processed_config = [self._substitute_placeholders(processed_config, p) for p in params]
