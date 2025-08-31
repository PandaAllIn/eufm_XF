from app.services.task_router import route_task as _route


def route_task(prompt: str) -> tuple[str, str]:
    return _route(prompt)
