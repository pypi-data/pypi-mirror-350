class Status:
    SKIPPED = "SKIPPED"
    FAILED = "FAILED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    RETRYING = "RETRYING"


class Queue:
    CORE = "core"
    EMS = "ems"
    SIERRA = "sierra"


class Tasks:
    SEND_VERSION = "send_version_to_core"
    UPDATE_TASK_STATUS = "update_task_status"
    UPDATE_TASK_VALUES = "update_task_values"
    MODEL_UPDATE = "component_model_update"
