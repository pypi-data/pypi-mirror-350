from typing import Any, Dict, List, Literal


class WorkflowOperations:
    """Workflow operation utilities for QoreClient"""

    def __init__(self, request_method):
        """
        Initialize with the request method from the parent client

        :param request_method: The _request method from QoreClient
        """
        self._request = request_method

    def execute_workflow(
        self,
        workflow_id: str,
        format: Literal["raw", "logs"] = "logs",
        **kwargs,
    ) -> List[str] | Dict[str, Any]:
        """
        워크플로우를 실행합니다.

        :param workflow_id: 실행할 워크플로우의 ID
        :param kwargs: 워크플로우 실행에 필요한 인수들 (키워드 인수)
        :return: 워크플로우 실행 결과에 대한 HTTP 응답 객체
        """
        response_data = self._request("POST", f"/api/workflow/{workflow_id}/execute", json=kwargs)

        if response_data is None:
            raise ValueError("Failed to execute workflow, received None response.")

        if format == "logs":
            return extract_logs(response_data)
        elif format == "raw":
            return response_data
        else:
            raise ValueError(f"Invalid format: {format}")


def extract_logs(workflow_result: Dict[str, Any]) -> List[str]:
    """
    워크플로우 실행 결과에서 logs만 추출하여 리스트로 반환

    :param workflow_result: execute_workflow의 원본 결과
    :return: 각 노드의 logs를 담은 리스트 (None이 아닌 것만)
    """
    logs = []
    for node_id, node_data in workflow_result.items():
        execute_result = node_data.get("execute_result", {})
        log_content = execute_result.get("logs")
        if log_content:
            logs.append(log_content)
    return logs
