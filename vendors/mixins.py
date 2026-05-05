class AuditMixin:
    """Sets created_by/updated_by from request.user on form save."""

    def form_valid(self, form):
        if not form.instance.pk:
            form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
