# Custom user model in Django.

### 1. **Why Customize the User Model?**

You may want to customize the user model in Django for the following reasons:

- Add custom fields to the user (e.g., date of birth, address, etc.)
- Add additional authentication logic (e.g., account verification, roles, etc.)
- Use custom manager methods (e.g., creating users, staff, superusers with additional logic)
- Add specific business logic related to users

### 2. **How to Customize the User Model**

#### Step 1: Create a New Custom User Model

In Django, you can customize the user model by extending `AbstractBaseUser` and `BaseUserManager`.

- `AbstractBaseUser` provides the core implementation for authentication, such as password hashing, authentication methods, and more.
- `BaseUserManager` helps with managing user creation logic (creating regular users, superusers, etc.).

Let's start by creating a custom user model.

1. **Create a new app for user-related functionality** (if you don't already have one):

   ```bash
   python manage.py startapp accounts
   ```

2. **Define a Custom User Model** in `accounts/models.py`:

   ```python
   from django.db import models
   from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
   from django.utils import timezone

   # Custom User Manager
   class CustomUserManager(BaseUserManager):
       def create_user(self, email, username, password=None, **extra_fields):
           """Create and return a regular user with an email and password."""
           if not email:
               raise ValueError('The Email field must be set')
           email = self.normalize_email(email)
           user = self.model(email=email, username=username, **extra_fields)
           user.set_password(password)
           user.save(using=self._db)
           return user

       def create_superuser(self, email, username, password=None, **extra_fields):
           """Create and return a superuser with an email, username, and password."""
           extra_fields.setdefault('is_staff', True)
           extra_fields.setdefault('is_superuser', True)
           return self.create_user(email, username, password, **extra_fields)

   # Custom User Model
   class CustomUser(AbstractBaseUser):
       email = models.EmailField(unique=True)
       username = models.CharField(max_length=150, unique=True)
       first_name = models.CharField(max_length=30, blank=True)
       last_name = models.CharField(max_length=30, blank=True)
       date_of_birth = models.DateField(null=True, blank=True)
       is_active = models.BooleanField(default=True)
       is_staff = models.BooleanField(default=False)
       is_superuser = models.BooleanField(default=False)
       date_joined = models.DateTimeField(default=timezone.now)

       objects = CustomUserManager()

       USERNAME_FIELD = 'email'
       REQUIRED_FIELDS = ['username']

       def __str__(self):
           return self.email

       # Optionally, you can add other fields here like profile picture, etc.
   ```

   ### Explanation:

   - **`CustomUserManager`**: Defines methods to create users and superusers. The `create_user` method is used for creating normal users, and the `create_superuser` method ensures that the superuser has appropriate staff and superuser permissions.
   - **`CustomUser`**: The custom user model. Here, we replaced the default `username` field with an `email` field for login (you can also add other fields like `date_of_birth`, `profile_picture`, etc.).
   - **`USERNAME_FIELD`**: This tells Django that the unique identifier for a user is the `email` field (instead of the default `username` field).
   - **`REQUIRED_FIELDS`**: A list of fields that must be filled when creating a superuser.

#### Step 2: Update `settings.py` to Use the Custom User Model

Once the custom user model is defined, you need to tell Django to use it. In your project’s `settings.py` file, add or update the following setting:

```python
AUTH_USER_MODEL = 'accounts.CustomUser'
```

This tells Django to use the `CustomUser` model from the `accounts` app as the user model.

#### Step 3: Create and Apply Migrations

Once you’ve defined your custom user model and updated your settings, run the migrations to create the necessary database tables.

```bash
python manage.py makemigrations accounts
python manage.py migrate
```

#### Step 4: Create Custom User Forms (Optional)

You may want to create custom forms for user registration, updating, or authentication. Django’s built-in `UserCreationForm` and `UserChangeForm` can be extended for this purpose.

1. **Creating a custom user creation form**:

   ```python
   from django import forms
   from .models import CustomUser

   class CustomUserCreationForm(forms.ModelForm):
       class Meta:
           model = CustomUser
           fields = ['email', 'username', 'password', 'first_name', 'last_name']

       password = forms.CharField(widget=forms.PasswordInput)

       def save(self, commit=True):
           user = super().save(commit=False)
           if commit:
               user.set_password(self.cleaned_data['password'])
               user.save()
           return user
   ```

2. **Creating a custom user change form**:

   ```python
   from django import forms
   from django.contrib.auth.forms import UserChangeForm
   from .models import CustomUser

   class CustomUserChangeForm(UserChangeForm):
       class Meta:
           model = CustomUser
           fields = ['email', 'username', 'first_name', 'last_name']
   ```

These forms can now be used in your Django admin panel or views.

#### Step 5: Update Django Admin (Optional)

To manage your custom user model through the Django admin panel, you need to create a custom admin form.

1. **Creating a custom admin form**:

   In your `accounts/admin.py`, define the following:

   ```python
   from django.contrib import admin
   from django.contrib.auth.admin import UserAdmin
   from .models import CustomUser
   from .forms import CustomUserCreationForm, CustomUserChangeForm

   class CustomUserAdmin(UserAdmin):
       add_form = CustomUserCreationForm
       form = CustomUserChangeForm
       model = CustomUser
       list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
       list_filter = ('is_staff', 'is_active')
       search_fields = ('email', 'username')
       ordering = ('email',)

   admin.site.register(CustomUser, CustomUserAdmin)
   ```

This will allow you to manage the custom user model through the admin panel.

#### Step 6: Using the Custom User Model in Your Application

Now that the custom user model is set up, you can use it in your views, serializers, and anywhere else in your application.

For example, to create a user in a view:

```python
from django.shortcuts import render
from .models import CustomUser

def create_user(request):
    user = CustomUser.objects.create_user(email="test@example.com", username="testuser", password="password123")
    return render(request, "user_created.html", {"user": user})
```

### 3. **Important Considerations**

- **Custom User Model Before Migrations**: You should define the custom user model **before running any migrations** for the project. Django does not allow changing the user model after migrations have been created, so it’s important to set `AUTH_USER_MODEL` early.
- **Extending `AbstractBaseUser` and `BaseUserManager`**: This is the recommended approach for custom user models, but you can also extend `AbstractUser` if you want to inherit Django's default user fields like `first_name`, `last_name`, `email`, `password`, etc., without having to reimplement everything.

- **Use `CustomUserManager` for Managing Users**: The `CustomUserManager` class should be used to handle user creation, particularly the `create_user` and `create_superuser` methods, to ensure password hashing and other important tasks are performed.

- **Don't Change User Model After Migrations**: Once you have applied migrations and have data in the database, changing the user model becomes much harder and might require custom migration scripts. Always decide on the custom user model at the start of the project.

### 4. **Conclusion**

Customizing the user model in Django is a straightforward process but requires some careful setup. By extending `AbstractBaseUser` and `BaseUserManager`, you gain full control over the user model. The steps involve:

1. Defining a custom user model.
2. Updating `settings.py` to point to the new user model.
3. Creating and applying migrations.
4. Optionally customizing forms and admin views for the new model.
