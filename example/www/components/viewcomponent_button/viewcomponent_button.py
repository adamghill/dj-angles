from django_viewcomponent import component


@component.register("viewcomponent_button")
class ButtonComponent(component.Component):
    template_name = "viewcomponent_button/viewcomponent_button.html"

    def __init__(self, **kwargs):
        self.label = kwargs["label"]
