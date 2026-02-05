import logging

from django.apps import apps

from dj_angles.evaluator import Portion
from dj_angles.templatetags.call import CallNode, do_call

logger = logging.getLogger(__name__)

"""
Global storage of all available models.
"""
models = None


def get_models() -> dict:
    models = {}

    for app_config in apps.get_app_configs():
        app_label = app_config.label

        if app_label not in models:
            models[app_label] = {}

        for model in app_config.get_models():
            model_name = model.__name__

            if model_name in models:
                if isinstance(models[model_name], dict):
                    logger.warning("Model name collision with app label: %s", model_name)
                else:
                    logger.warning("Model name collision: %s. Using %s.", model_name, app_label)

            models[model_name] = model
            models[app_label][model_name] = model

    return models


def clear_models() -> None:
    global models  # noqa: PLW0603
    models = None


class ModelNode(CallNode):
    def render(self, context):
        global models  # noqa: PLW0603

        if models is None:
            models = get_models()

        context["__dj_angles_models"] = models

        return super().render(context)


def do_model(parser, token) -> ModelNode:
    call_node = do_call(parser, token)

    # Models are stored in a special part of the context so it doesn't conflict with other data
    # so add this fake object name because we will use it in the render method
    call_node.parsed_function.portions.insert(0, Portion(name="__dj_angles_models"))

    return ModelNode(call_node.parsed_function, call_node.context_variable_name)
