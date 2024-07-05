from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
User = get_user_model()


class SuccessMessageMixin(object):
    """CBV mixin which adds a success message on form save."""

    success_message = ""

    def get_success_message(self):
        return self.success_message

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message()
        if not self.request.is_ajax() and success_message:
            messages.success(self.request, success_message)
        return response


class AdminLoginRequiredMixin(LoginRequiredMixin):
    def has_permission(self):
        """
        Override this method to customize the way permissions are checked.
        """
        return True if (self.request.user.role in [User.SUPER_ADMIN]) else False
        # return True if self.request.user.role == User.SUPER_ADMIN

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not self.has_permission():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)