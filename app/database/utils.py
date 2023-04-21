# coding: utf-8

# Credits : https://gist.github.com/jason-w/4969476

from typing import List, Dict, Any
from mongoengine import (
    Document,
    ListField,
    EmbeddedDocumentField,
    DictField,
    EmbeddedDocument,
    FloatField,
    DateTimeField,
    ComplexDateTimeField,
    IntField,
    BooleanField,
    ObjectIdField,
    DecimalField,
    StringField,
    QuerySet
)

def query_to_dict(query_set: QuerySet) -> List[Dict[str, str]]:
    """Convert a query result into a list of each ouput document as dict.

    Args:
        query_set (QuerySet): the query result.

    Returns:
        List[Dict[str, str]]: output list of documents as dicts.
    """
    return [mongo_to_dict(document) for document in query_set]

def mongo_to_dict(obj, exclude_fields: List[str] = []) -> Dict[str, str]:
    """Returns the Dict format of the Document instance given in parameter.

    Args:
        obj (Deferred): the document queried from database to convert into dict.
        exclude_fields (List[str], optional): list of fields to exclude in the
            output dict. Defaults to [].

    Returns:
        Dict[str, str]: output dict.
    """
    return_data = list()

    if obj is None:
        return None

    if isinstance(obj, Document):
        return_data.append(("id",str(obj.id)))

    for field_name in obj._fields:

        if field_name in exclude_fields:
            continue

        if field_name in ("id",):
            continue

        data = obj._data[field_name]

        if isinstance(obj._fields[field_name], ListField):
            return_data.append((field_name, list_field_to_dict(data)))
        elif isinstance(obj._fields[field_name], EmbeddedDocumentField):
            return_data.append((field_name, mongo_to_dict(data,[])))
        elif isinstance(obj._fields[field_name], DictField):
            return_data.append((field_name, data))
        else:
            return_data.append(
                (field_name, mongo_to_python_type(obj._fields[field_name],data))
            )

    return dict(return_data)

def list_field_to_dict(list_field: List) -> List[str]:
    """Converts mongo db output list fields as a list of str.

    Args:
        list_field (List): list to convert.

    Returns:
        List[str]: output list.
    """
    return_data = []

    for item in list_field:
        if isinstance(item, EmbeddedDocument):
            return_data.append(mongo_to_dict(item,[]))
        else:
            return_data.append(mongo_to_python_type(item,item))


    return return_data

def mongo_to_python_type(field: str, data: Any):
    """Convert the field into str depending on the field type.

    Args:
        field (str): field type.
        data (Any): Associated data to convert.

    Returns:
        str: data converted.
    """
    if isinstance(field, DateTimeField):
        return str(data.isoformat())
    elif isinstance(field, ComplexDateTimeField):
        return field.to_python(data).isoformat()
    elif isinstance(field, StringField):
        return str(data)
    elif isinstance(field, FloatField):
        return float(data)
    elif isinstance(field, IntField):
        return int(data)
    elif isinstance(field, BooleanField):
        return bool(data)
    elif isinstance(field, ObjectIdField):
        return str(data)
    elif isinstance(field, DecimalField):
        return data
    else:
        return str(data)