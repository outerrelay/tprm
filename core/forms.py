from django import forms


class BootstrapFormMixin:
    """Auto-applies Bootstrap 5 widget classes based on widget type.

    Form classes that inherit this mixin (in addition to forms.ModelForm or
    forms.Form) no longer need to declare a `widgets` dict in Meta just to set
    Bootstrap classes. Per-field placeholder/step/min/etc. attrs can still be
    set via Meta.widgets — this mixin only fills the `class` attribute when
    one isn't already present.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            existing = widget.attrs.get('class', '')
            if existing:
                continue
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs['class'] = 'form-select'
            elif isinstance(widget, forms.DateInput):
                widget.attrs.setdefault('type', 'date')
                widget.attrs['class'] = 'form-control'
            else:
                widget.attrs['class'] = 'form-control'
