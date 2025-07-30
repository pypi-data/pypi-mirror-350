from pipelex.cogt.exceptions import CogtError


class OpenAIWorkerError(CogtError):
    pass


class OpenAIWorkerModelNotFoundError(OpenAIWorkerError):
    pass
