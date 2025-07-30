import subprocess
import tempfile
import os
import re
from typing import Dict, List, Any
from scientiflow_cli.services.status_updater import update_job_status, update_stopped_at_node
from scientiflow_cli.services.request_handler import make_auth_request
from scientiflow_cli.services.rich_printer import RichPrinter

printer = RichPrinter()

class PipelineExecutor:
    def __init__(self, base_dir: str, project_id: int, project_job_id: int, project_title: str, job_dir_name: str, nodes: List[Dict[str, Any]], edges: List[Dict[str, str]], environment_variables: Dict[str, str], start_node: str = None, end_node: str = None):
        self.base_dir = base_dir
        self.project_id = project_id
        self.project_job_id = project_job_id
        self.project_title = project_title
        self.job_dir_name = job_dir_name
        self.nodes = nodes
        self.edges = edges
        self.environment_variables = environment_variables
        self.start_node = start_node
        self.end_node = end_node
        self.current_node = None

        # Set up job-specific log file
        self.log_file_path = os.path.join(self.base_dir, self.project_title, self.job_dir_name, "logs", "output.log")
        os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)

        # Create mappings for efficient execution
        self.nodes_map = {node['id']: node for node in nodes}
        self.adj_list = {node['id']: [] for node in nodes}
        for edge in edges:
            self.adj_list[edge['source']].append(edge['target'])

        # Identify root nodes (nodes with no incoming edges)
        all_nodes = set(self.nodes_map.keys())
        target_nodes = {edge['target'] for edge in edges}
        self.root_nodes = all_nodes - target_nodes

        # Initialize log file
        self.init_log()

    def init_log(self):
        """Initialize the log file."""
        try:
            with open(self.log_file_path, 'w') as f:
                f.write('')
        except Exception as e:
            print(f"[ERROR] Failed to initialize log file: {e}")

    def log_output(self, text: str):
        """Write to log file."""
        try:
            with open(self.log_file_path, 'a') as f:
                f.write(text + "\n")
        except Exception as e:
            print(f"[ERROR] Failed to write log: {e}")

    def update_terminal_output(self):
        """Update the terminal output after execution is complete."""
        try:
            with open(self.log_file_path, 'r') as f:
                terminal_output = f.read()
            body = {"project_job_id": self.project_job_id, "terminal_output": terminal_output}
            make_auth_request(endpoint="/agent-application/update-terminal-output", method="POST", data=body, error_message="Unable to update terminal output!")
            printer.print_message("[+] Terminal output updated successfully.", style="bold green")
        except Exception as e:
            print(f"[ERROR] Failed to update terminal output: {e}")

    def replace_variables(self, command: str) -> str:
        """Replace placeholders like ${VAR} with environment values."""
        return re.sub(r'\$\{(\w+)\}', lambda m: self.environment_variables.get(m.group(1), m.group(0)), command)

    def execute_command(self, command: str):
        """Run the command in the terminal, display output in real-time, and log the captured output."""
        try:
            with tempfile.TemporaryFile() as tempf:
                proc = subprocess.Popen(command, shell=True, stdout=None, stderr=None)
                proc.wait()

                tempf.seek(0)
                result = tempf.read().decode()
                self.log_output(result)  # Log the entire output

                if proc.returncode != 0:
                    self.log_output(f"[ERROR] Command failed with return code {proc.returncode}")
                    update_job_status(self.project_job_id, "failed")
                    update_stopped_at_node(self.project_id, self.project_job_id, self.current_node)
                    self.update_terminal_output()
                    raise SystemExit("[ERROR] Pipeline execution terminated due to failure.")

        except Exception as e:
            self.log_output(f"[ERROR] An unexpected error occurred: {e}")
            update_job_status(self.project_job_id, "failed")
            update_stopped_at_node(self.project_id, self.project_job_id, self.current_node)
            self.update_terminal_output()
            raise SystemExit("[ERROR] Pipeline execution terminated due to an unexpected error.")

    def dfs(self, node: str):
        """Perform Depth-First Search (DFS) for executing pipeline nodes."""
        if self.current_node == self.end_node:
            return

        self.current_node = node
        current_node = self.nodes_map[node]

        if current_node['type'] == "splitterParent":
            collector = None
            for child in self.adj_list[node]:
                if self.nodes_map[child]['data']['active']:
                    collector = self.dfs(child)
            if collector and self.adj_list[collector]:
                return self.dfs(self.adj_list[collector][0])
            return

        elif current_node['type'] == "splitter-child":
            if current_node['data']['active'] and self.adj_list[node]:
                return self.dfs(self.adj_list[node][0])
            return

        elif current_node['type'] == "terminal":
            commands = current_node['data']['commands']
            isGPUEnabled = current_node['data'].get('gpuEnabled', False)

            for command in commands:
                cmd = self.replace_variables(command.get('command', ''))
                if cmd:
                    base_command = f"cd {self.base_dir}/{self.project_title}/{self.job_dir_name} && singularity exec "
                    container_path = f"{self.base_dir}/containers/{current_node['data']['software']}.sif"
                    gpu_flag = "--nv --nvccli" if isGPUEnabled else ""

                    full_command = f"{base_command} {gpu_flag} {container_path} {cmd}"
                    self.execute_command(full_command)

            if self.adj_list[node]:
                return self.dfs(self.adj_list[node][0])
            return

        elif current_node['type'] == "collector":
            return node if self.adj_list[node] else None

    def decode_and_execute_pipeline(self):
        """Start executing the pipeline."""
        update_job_status(self.project_job_id, "running")
        root_node = self.start_node or next(iter(self.root_nodes), None)

        if root_node:
            self.dfs(root_node)

        update_job_status(self.project_job_id, "completed")
        update_stopped_at_node(self.project_id, self.project_job_id, self.current_node)

        # Update terminal output at the end of execution
        self.update_terminal_output()

# External function to initiate the pipeline execution
def decode_and_execute_pipeline(base_dir: str, project_id: int, project_job_id: int, project_title: str, job_dir_name: str, nodes: List[Dict[str, Any]], edges: List[Dict[str, str]], environment_variables: Dict[str, str], start_node: str = None, end_node: str = None):
    """Initialize and execute the pipeline."""
    executor = PipelineExecutor(base_dir, project_id, project_job_id, project_title, job_dir_name, nodes, edges, environment_variables, start_node, end_node)
    executor.decode_and_execute_pipeline()