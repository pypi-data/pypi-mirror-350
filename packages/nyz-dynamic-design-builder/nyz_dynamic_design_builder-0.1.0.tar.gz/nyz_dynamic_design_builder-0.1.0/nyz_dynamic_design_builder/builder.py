import pandas as pd
from django.db.models import ForeignKey, ManyToManyField
from django.db.models.fields import DateField, DateTimeField

__all__ = [
    "search_fk_value",
    "get_m2m_fields",
    "get_special_fk_fields",
    "export_data",
]


def search_fk_value(obj, field, search_fk_list):
    """
    Traverse a ForeignKey field on `obj`, returning the first non-empty attribute
    from `search_fk_list`.
    """
    for attr in search_fk_list or []:
        try:
            fk_obj = getattr(obj, field)
            value = getattr(fk_obj, attr, None)
            if callable(value):
                value = value()
            if value:
                return value
        except Exception:
            return ""
    return ""


def get_m2m_fields(field_name, m2m_values, search_fk_list, ignore_m2m_fields=None):
    """
    Flatten a ManyToMany field into multiple columns.
    """
    rows = {}
    for idx, item in enumerate(m2m_values, start=1):
        for f in item._meta.fields:
            if ignore_m2m_fields and f.name in ignore_m2m_fields:
                continue
            col_label = f"{field_name} {idx} - {f.verbose_name}"
            val = getattr(item, f.name)
            if isinstance(f, (DateField, DateTimeField)):
                val = val.strftime("%Y-%m-%d %H:%M:%S") if val else ""
            if isinstance(f, ForeignKey):
                val = search_fk_value(item, f.name, search_fk_list)
            rows[col_label] = val
    return rows


def get_special_fk_fields(obj, field_name, sub_fields):
    """
    Extract specified attributes from a ForeignKey as separate columns.
    """
    result = {}
    fk_obj = getattr(obj, field_name, None)
    if not fk_obj:
        return result
    for sf in sub_fields:
        val = getattr(fk_obj, sf, "")
        if callable(val):
            val = val()
        try:
            label = fk_obj._meta.get_field(sf).verbose_name
        except Exception:
            label = sf
        result[label] = val
    return result


def export_data(
    field_list,
    query,
    search_fk_list=None,
    ignore_m2m_fields=None,
    special_fk_values=None,
):
    """
    Build a list of dictionaries from a Django queryset based on dynamic fields,
    handling Date, ForeignKey, and ManyToMany fields. Returns a pandas DataFrame.

    :param field_list: List of field names to include.
    :param query: Django queryset.
    :param search_fk_list: Attributes to traverse on ForeignKey.
    :param ignore_m2m_fields: M2M field names to skip.
    :param special_fk_values: Dict of FK field to list of its attributes.
    :return: pandas.DataFrame
    """
    rows = []
    for obj in query:
        row = {}
        for field in field_list:
            try:
                fld = obj._meta.get_field(field)
                label = fld.verbose_name
                val = getattr(obj, field)

                # Date handling
                if isinstance(fld, DateField):
                    val = val.strftime("%Y-%m-%d") if val else ""
                elif isinstance(fld, DateTimeField):
                    val = val.strftime("%Y-%m-%d %H:%M:%S") if val else ""

                # ForeignKey
                if isinstance(fld, ForeignKey):
                    if special_fk_values and field in special_fk_values:
                        row.update(get_special_fk_fields(obj, field, special_fk_values[field]))
                        continue
                    val = search_fk_value(obj, field, search_fk_list or [])
                    row[label] = val

                # ManyToMany
                elif isinstance(fld, ManyToManyField):
                    m2m_vals = val.all()
                    row.update(get_m2m_fields(label, m2m_vals, search_fk_list or [], ignore_m2m_fields))

                else:
                    row[label] = val
            except Exception:
                row[field] = ""
        rows.append(row)

    return pd.DataFrame(rows)