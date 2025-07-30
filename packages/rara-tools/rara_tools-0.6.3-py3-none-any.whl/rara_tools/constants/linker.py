COMPONENT_KEY = "linker"


class Task:
    BASE = "base_linker_task"
    VECTORIZE = "vectorize_text"
    LINK_AND_NORMALIZE = "core_linker_with_normalization"
    VECTORIZE_AND_INDEX = "core_vectorize_and_index"
    RECEIVE_LINK_AND_NORMALIZE = "receive_link_and_normalize"


class Queue:
    LINKER = "linker"
    VECTORIZER = "vectorizer"
