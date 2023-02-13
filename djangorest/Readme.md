# Django Rest Framework
Django Rest Framework (DRF) is a powerful and flexible toolkit for building Web APIs. It is a third-party package for the Django web framework that makes it easy to build, test, and debug RESTful APIs written using Django.

DRF takes care of the heavy lifting of transforming Django models into a RESTful API. It supports a wide range of features, including authentication, URL routing, request parsing, and response handling. It also provides generic views, serializers, and query parameters that allow you to easily build RESTful APIs for your Django models.

DRF is highly customizable and can be used for building APIs for a variety of use cases, from simple CRUD operations to complex, real-time data processing. With its robust documentation and large community, DRF is a popular choice for building RESTful APIs in Django.

# Serialization
Serialization is the process of converting complex data structures, such as Django models, into a format that can be easily transmitted over the internet, such as JSON or XML. In DRF, this is achieved using serializers, which are similar to Django's forms.

A serializer in DRF is a class that defines the fields that should be serialized and how they should be converted to and from Python data types. DRF provides two types of serializers:

* `serializers.Serializer:` This is a basic serializer that provides a simple way to convert simple Python data types, such as strings, integers, and lists, into JSON or XML format, and vice versa.
* `serializers.ModelSerializer:` This is a more powerful serializer that is designed to work with Django models. It generates a serializer class automatically based on a Django model and provides a simple way to serialize and deserialize model instances.

Here is an example of how to use a `ModelSerializer` in DRF:
```python
from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'description']
```
In this example, we define a `ArticleSerializer` class that serializes the `Article` model. The `Meta` class specifies the model to use and the fields to serialize. You can then use this serializer to serialize and deserialize `Article` instances.

`serializers.Serializer`, is a basic serializer that allows you to convert simple Python data types, such as strings, integers, and lists, into JSON or XML format, and vice versa.

Here's an example of how to use a Serializer in DRF:
```python
from rest_framework import serializers

class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500)
    created_at = serializers.DateTimeField()
```
In this example, we define an `ArticleSerializer` class that serializes an article. The class includes three fields: `title`, `description`, and `created_at`, each of which is represented as a different type of serializer field.

The `Meta` class in a Django Rest Framework serializer is used to specify metadata for the serializer. In the context of `ModelSerializer`, the `Meta` class is used to specify the model that the serializer should be based on, as well as other options for the serializer.

Here's an example of a `Meta` class for a `ModelSerializer`:
```python
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'description', 'created_at']
```
In this example, the `Meta` class has two attributes:
* `model`: The model that the serializer should be based on. This attribute is required.
* `fields`: The fields of the model that should be serialized. This attribute is optional. If not specified, all fields of the model will be serialized.

Other attributes that can be included in the Meta class include:

* `exclude`: A list of fields that should be excluded from serialization. This attribute can be used instead of fields to exclude certain fields.
* `read_only_fields`: A list of fields that should be serialized as read-only. These fields will be included in serialized data, but will be ignored during deserialization.
* `write_only_fields`: A list of fields that should be serialized as write-only. These fields will be included in deserialized data, but will be ignored during serialization.

The `Meta` class is an important part of a Django Rest Framework serializer, as it provides a way to specify the model and fields to be used, as well as other options that affect the behavior of the serializer.

## Creating serializer class
```python
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
```
This is an example of a `SnippetSerializer` class that serializes and deserializes instances of the `Snippet` model. The class inherits from `serializers.Serializer` and specifies the fields that should be serialized. Each field is specified using one of the field classes provided by DRF, such as `CharField`, `BooleanField`, `ChoiceField`, etc.

In this example, the `id` field is **_read-only_**, _meaning it will only be used when serializing a `Snippet` instance, and not when deserializing data._ The `title` field is not required, and allows blank values.

The code field uses a different HTML template when being rendered in the API browser. The `linenos`, `language`, and `style` fields are all boolean or choice fields, and have default values specified.

The `create` and `update` methods allow you to customize how instances of the `Snippet` model are created and updated using this serializer. The `create` method takes the validated data and creates a new `Snippet` instance using the `Snippet.objects.create` method. The `update` method updates an existing `Snippet` instance with the validated data.

To use the serializer, you would first instantiate it and pass in the data you want to serialize or deserialize. Then, you can call the `.is_valid()` method to validate the data before serializing or deserializing it, and access the serialized or deserialized data using the `.data` or `.validated_data` attributes, respectively.