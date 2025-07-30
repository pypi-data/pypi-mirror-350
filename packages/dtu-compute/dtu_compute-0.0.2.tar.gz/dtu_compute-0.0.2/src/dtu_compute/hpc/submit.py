from pathlib import Path

from dtu_compute.connection import ClusterConnection
from dtu_compute.run_config import JobConfig


class LSFJob:
    """Class to generate a LSF job script from a job configuration."""

    def __init__(self, config: JobConfig, target_dir: str | None = None) -> None:
        self.config = config
        self.target_dir = target_dir

    def submit(self, connection: ClusterConnection) -> None:
        """Submit the job script to the cluster using the provided connection."""
        submit_file = self.process()
        connection.put(submit_file, remote_path=self.target_dir)
        connection.run(f"cd {self.target_dir} && bsub < {submit_file.name}")
        connection.run(f"rm {self.target_dir}/{submit_file.name}")

    def process(self) -> Path:
        """Process the job configuration and create a LSF script file."""
        # Create the script file
        script_content = self.to_script()

        # Create unique file name
        save_folder = Path(".dtu_compute")
        save_folder.mkdir(parents=True, exist_ok=True)
        base_name = self.config.name.replace(" ", "_").replace("/", "_")
        extension = ".sh"
        version = 0
        save_path = save_folder / f"{base_name}_v{version}{extension}"
        while save_path.exists():
            save_path = save_folder / f"{base_name}_v{version}{extension}"
            version += 1

        # Write the script content to the file
        with save_path.open("w") as f:
            f.write(script_content)
        return save_path

    def to_script(self) -> str:
        """Convert the job configuration to a LSF script."""
        cfg = self.config
        lines = [
            f"#BSUB -J {cfg.name}",
            f"#BSUB -q {cfg.queue}",
            f"#BSUB -n {cfg.cores}",
            f"#BSUB -R 'rusage[mem={cfg.memory}]'",
            f"#BSUB -M {int(cfg.memory * 1024)}",  # LSF uses MB
            f"#BSUB -W {cfg.walltime.hours:02}:{cfg.walltime.minutes:02}",
            f"#BSUB -o {cfg.std_out}",
            f"#BSUB -e {cfg.std_err}",
        ]

        if cfg.notification.email_on_start or cfg.notification.email_on_end:
            mail_flags = ""
            if cfg.notification.email_on_start:
                mail_flags += "b"
            if cfg.notification.email_on_end:
                mail_flags += "e"
            lines += [
                f"#BSUB -u {cfg.notification.email}",
                "#BSUB -B" if "b" in mail_flags else "",
                "#BSUB -N" if "e" in mail_flags else "",
            ]

        if cfg.gpu.num_gpus > 0:
            lines += [f"#BSUB -R 'select[gpu_model0=={cfg.gpu.gpu_type}] rusage[ngpus_excl_p={cfg.gpu.num_gpus}]'"]

        lines += ["", *cfg.commands]
        return "\n".join([line for line in lines if line])
