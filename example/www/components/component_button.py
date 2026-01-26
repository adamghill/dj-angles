from django_components import Component, NotRegistered, register, registry

try:
    registry.get("component_button")
except NotRegistered:

    @register("component_button")
    class ComponentButton(Component):
        template_name = "component_button.html"

        def get_context_data(self, label):
            return {
                "label": label,
            }
