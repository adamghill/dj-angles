from django_components import Component, register


@register("button")
class Button(Component):
    template_name = "button.html"

    def get_context_data(self, label):
        return {
            "label": label,
        }
