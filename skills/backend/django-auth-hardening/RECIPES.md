# Django Auth Hardening — Recipes

Concrete configuration and code. Load when implementing; the decision-making
lives in [SKILL.md](SKILL.md).

Targets Django 5.2+.

---

## Session Security

`settings.py`, appended after the base configuration so `DEBUG` is already set.

```python
# ==========================================
# SESSION SECURITY
# ==========================================

SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7          # 7 days
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True               # sliding expiry

if not DEBUG:
    # Cookies
    SESSION_COOKIE_SECURE = True                # HTTPS only
    SESSION_COOKIE_HTTPONLY = True              # no JS access
    SESSION_COOKIE_SAMESITE = "Lax"             # see quirks re: 'Strict'
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SAMESITE = "Lax"

    # Transport
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 3600                  # raise once TLS is proven
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = False                 # opt in deliberately, later

    # Headers
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "same-origin"
    X_FRAME_OPTIONS = "DENY"
```

Verify: `python manage.py check --deploy`.

---

## Logout

`urls.py`:

```python
from django.contrib.auth.views import LogoutView
from django.urls import path

urlpatterns = [
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
]
```

Template — a POST form, not a link:

```html
<form method="post" action="{% url 'logout' %}" class="logout-form">
  {% csrf_token %}
  <button type="submit" class="logout-button">Log out</button>
</form>
```

If the design requires a link, style the button as one. Do not add a GET route.

---

## Rate Limiting (django-axes)

```bash
uv add django-axes
```

`settings.py`:

```python
INSTALLED_APPS = [
    # ...
    "axes",
]

MIDDLEWARE = [
    # ... must come last
    "axes.middleware.AxesMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",   # must come first
    "django.contrib.auth.backends.ModelBackend",
]

AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1                        # hours
AXES_LOCKOUT_PARAMETERS = [["ip_address", "username"]]  # combination, not either
AXES_RESET_ON_SUCCESS = True
AXES_LOCKOUT_TEMPLATE = "registration/locked_out.html"
AXES_ENABLE_ADMIN = True
```

Then `python manage.py migrate`.

Unlock during development:

```bash
python manage.py axes_reset
python manage.py axes_reset_ip 203.0.113.5
```

---

## Email Backend

Credentials from the environment. Never commit them.

```python
import os

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

Verify before building anything on top of it:

```python
from django.core.mail import send_mail
send_mail("test", "body", None, ["you@example.com"])
```

---

## Password Reset

`urls.py` — four built-in views:

```python
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns += [
    path("password-reset/",
         auth_views.PasswordResetView.as_view(
             template_name="registration/password_reset_form.html",
             email_template_name="registration/password_reset_email.html",
             subject_template_name="registration/password_reset_subject.txt",
         ), name="password_reset"),
    path("password-reset/done/",
         auth_views.PasswordResetDoneView.as_view(
             template_name="registration/password_reset_done.html",
         ), name="password_reset_done"),
    path("reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(
             template_name="registration/password_reset_confirm.html",
         ), name="password_reset_confirm"),
    path("reset/done/",
         auth_views.PasswordResetCompleteView.as_view(
             template_name="registration/password_reset_complete.html",
         ), name="password_reset_complete"),
]
```

Tighten the token lifetime — the default is 3 days:

```python
PASSWORD_RESET_TIMEOUT = 60 * 60 * 2   # 2 hours
```

Required templates under `templates/registration/`:
`password_reset_form.html`, `password_reset_done.html`,
`password_reset_confirm.html`, `password_reset_complete.html`,
`password_reset_email.html`, `password_reset_subject.txt`.

---

## Profile Editing

Re-authenticate before an email change.

```python
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


class ProfileForm(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("email") != self.user.email:
            if not self.user.check_password(cleaned.get("current_password") or ""):
                raise forms.ValidationError(
                    "Enter your current password to change your email address."
                )
        return cleaned


@login_required
def profile_edit(request):
    form = ProfileForm(request.POST or None, instance=request.user, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("profile")
    return render(request, "registration/profile.html", {"form": form})
```

---

## Account Deletion

Two-step: a confirmation page, then the destructive action. Decide hard-delete
versus anonymize and state it in the UI.

```python
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone


@login_required
def account_delete(request):
    """Confirmation page — GET only."""
    return render(request, "registration/account_delete.html")


@login_required
def account_delete_confirm(request):
    if request.method != "POST":
        return redirect("account_delete")

    if not request.user.check_password(request.POST.get("password", "")):
        return render(
            request,
            "registration/account_delete.html",
            {"error": "Password incorrect. Your account has not been deleted."},
        )

    user = request.user
    logout(request)

    # Option A — hard delete. Audit every FK's on_delete first.
    user.delete()

    # Option B — anonymize, preserving referential integrity:
    # user.username = f"deleted_user_{user.pk}"
    # user.email = ""
    # user.first_name = user.last_name = ""
    # user.is_active = False
    # user.set_unusable_password()
    # user.deleted_at = timezone.now()
    # user.save()

    return redirect("account_deleted")
```

Before shipping, enumerate every relation:

```bash
python manage.py shell -c "
from django.contrib.auth.models import User
for f in User._meta.related_objects:
    print(f.related_model.__name__, f.field.name, f.on_delete.__name__)
"
```

---

## Deploy Verification

```bash
python manage.py check --deploy
```

Then walk manually: register → log in → fail login 5× and confirm lockout →
reset password by email → change email (expect password prompt) → log out →
delete account.
