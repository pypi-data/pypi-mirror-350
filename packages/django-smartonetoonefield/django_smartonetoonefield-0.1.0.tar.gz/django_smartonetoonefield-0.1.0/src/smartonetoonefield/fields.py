# https://www.fusionbox.com/blog/detail/django-onetoonefields-are-hard-to-use-lets-make-them-better/551/
from django.db.models.fields.related import OneToOneField
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor


class AutoReverseOneToOneDescriptor(ReverseOneToOneDescriptor):
    def __get__(self, instance, type_=None):
        try:
            return super().__get__(instance, type_)
        except self.RelatedObjectDoesNotExist:
            rel_obj = self.get_queryset().create(**{self.related.field.name: instance})
            setattr(instance, self.related.related_name, rel_obj)
            return rel_obj


class AutoOneToOneField(OneToOneField):
    related_accessor_class = AutoReverseOneToOneDescriptor


class SoftReverseOneToOneDescriptor(ReverseOneToOneDescriptor):
    def __init__(self, *args, **kwargs):
        self.flag_name = kwargs.pop('flag_name')
        super().__init__(*args, **kwargs)

    def __get__(self, *args, **kwargs):
        try:
            return super().__get__(*args, **kwargs)
        except self.RelatedObjectDoesNotExist:
            return None

    def contribute_to_related_class(self, cls, related):
        super().contribute_to_related_class(cls, related)

        if not self.flag_name.endswith('+'):
            def flag(model_instance):
                return hasattr(model_instance, related.get_accessor_name())
            setattr(cls, self.flag_name, property(flag))

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['flag_name'] = self.flag_name
        return name, path, args, kwargs


class SoftOneToOneField(OneToOneField):
    related_accessor_class = SoftReverseOneToOneDescriptor


class AddFlagOneToOneField(OneToOneField):
    def __init__(self, *args, **kwargs):
        self.flag_name = kwargs.pop('flag_name')
        super(AddFlagOneToOneField, self).__init__(*args, **kwargs)

    def contribute_to_related_class(self, cls, related):
        super(AddFlagOneToOneField, self).contribute_to_related_class(cls, related)

        def flag(model_instance):
            return hasattr(model_instance, related.get_accessor_name())
        setattr(cls, self.flag_name, property(flag))

    def deconstruct(self):
        name, path, args, kwargs = super(AddFlagOneToOneField, self).deconstruct()
        kwargs['flag_name'] = self.flag_name
        return name, path, args, kwargs
