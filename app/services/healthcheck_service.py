def get_healthcheck_payload() -> dict:
    return {
        "status_code": 200,
        "detail":"ok",
        "result": "working"
    }