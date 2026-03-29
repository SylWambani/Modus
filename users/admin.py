from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth import get_user_model
from .models import UserInvite
from .utils import send_invite_email

User = get_user_model()

@admin.register(UserInvite)
class UserInviteAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name", "employee_number","email", "role", "is_used", "created_at")
    actions = ["send_invites"]

    def send_invites(self, request, queryset):
        sent_count = 0

        for invite in queryset:
            if not invite.is_used:
                send_invite_email(invite)
                sent_count += 1

        self.message_user(request, f"{sent_count} invite(s) sent successfully.")

    send_invites.short_description = "Send invite emails"

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name','username', 'email'),
        }),
    )
