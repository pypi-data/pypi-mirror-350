from scientiflow_cli.services.request_handler import make_auth_request
from scientiflow_cli.services.rich_printer import RichPrinter

printer = RichPrinter()

def update_stopped_at_node(project_id: int, project_job_id: int, stopped_at_node: str):
    body = {"project_id": project_id, "project_job_id": project_job_id, "stopped_at_node": stopped_at_node}
    try:
        make_auth_request(endpoint="/jobs/update-stopped-at-node", method="POST", data=body, error_message="Unable to update stopped at node!")
        printer.print_message("[+] Stopped at node updated successfully.", style="bold green")
    except Exception as e:
        printer.print_panel(f"Error updating stopped at node: {e}", style="bold red")

def update_job_status(project_job_id: int, status: str):
    body = {"project_job_id": project_job_id, "status": status}
    try:
        make_auth_request(endpoint="/agent-application/update-project-job-status", method="POST", data=body, error_message="Unable to update job status!")
        printer.print_message("[+] Project status updated successfully.", style="bold green")
    except Exception as e:
        printer.print_panel(f"Error updating job status: {e}", style="bold red")
