# Smart One-To-One Field

### For Django

[![pypi](https://img.shields.io/pypi/v/django-smartonetoonefield.svg)](https://pypi.python.org/pypi/django-smartonetoonefield/)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/blag/django-smartonetoonefield/main.svg)](https://results.pre-commit.ci/latest/github/blag/django-smartonetoonefield/main)
[![tests ci](https://github.com/blag/django-smartonetoonefield/workflows/tests/badge.svg)](https://github.com/blag/django-smartonetoonefield/actions)

**django-smartonetoonefield** provides utility fields discussed in [this Fusionbox blog post](https://www.fusionbox.com/blog/detail/django-onetoonefields-are-hard-to-use-lets-make-them-better/551/)


## Compatibility

- Python: >= **3.12**
- Django: >= **4.2**


## Installation

1. Install the latest version:

   ```sh
   pip install django-smartonetoonefield
   ```

   ```sh
   poetry add django-smartonetoonefield
   ```

2. Add `smartonetoonefield` to `INSTALLED_APPS` in your project's `settings.py`.


## Usage

### `AutoOneToOneField`

If you can create a related model by just filling in one field, then `AutoOneToOneField` will simplify your code.

To use, define an `AutoOneToOneField` field on a model with a relation to another field. This will ensure that the related model object will always exist, even if it must be created upon first access.

`models.py`:

```python
class CustomerProfile(models.Model):
    user = AutoOneToOneField('User', related_name='customer_profile')
```

```python
user = User.objects.all()[0]
user.customer_profile  # Always returns a customer profile
```

### `SoftOneToOneField`

If you cannot create the related model by simply setting the foreign key on the related model, then a `SoftOneToOneField` might work better for you.

With `SoftOneToOneField`, if the related model object exists, the lookup will work as normal. But if the related model object does not exist, then the attribute will be `None`.

`models.py`:

```python
class CustomerProfile(models.Model):
    user = SoftOneToOneField('User', related_name='customer_profile')
```

`views.py`:

```python
class MyProfileView(DetailView):
    def get_context_data(self, **kwargs):
        kwargs = super(MyProfileView, self).get_context_data(**kwargs)
        # This will not raise an exception if the customer_profile does
        # not exist
        kwargs.update(my_profile=self.customer_profile)
        return kwargs
```

### `AddFlagOneToOneField`

Sometimes, when you need to check if a related model exists or not, it can be unwieldy to query the relation directly. A workaround to this is to define properties on the reverse related model:

`models.py`:

```python
class User(AbstractUser):
    # ...
    def is_customer(self):
        return hasattr(self, 'customer_profile')


class CustomerProfile(models.Model):
    user = models.OneToOneField('User', related_name='customer_profile')
```

However, this can necessitate creating a custom default user model for a project, and this can be impossible if you need to override a model in a third party Django app.

Instead of overriding models or querying the related fields directly, the `AddFlagOneToOneField` will automatically add flags to the related model to make it easier to query related fields:

`models.py`:

```python
class CustomerProfile(models.Model):
    user = AddFlagOneToOneField('auth.User', related_name='customer_profile',
                                flag_name='is_customer')


class MerchantProfile(models.Model):
    user = AddFlagOneToOneField('auth.User', related_name='merchant_profile',
                                flag_name='is_merchant')


class EmployeeProfile(models.Model):
    user = AddFlagOneToOneField('auth.User', related_name='employee_profile',
                                flag_name='is_employee')
```

`views.py`:

```python
user = User.objects.get(email='customer@example.com')
user.is_customer  # True
user.is_merchant  # False
user.is_employee  # False
```

Since the `AddFlagOneToOneField` won't throw exceptions on access, you don't have to override, inherit, or modify other models when using the specified flags.

## TODO

I have intentionally kept this app very small to minimize the maintenance
burden. But contributions are very welcome!

## License

BSD
