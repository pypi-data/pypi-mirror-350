from django_post_api.fields import ForeignKeyField, ManyToManyField


def build_tree_data(data_list, key="pid"):
    res = {}
    for comment in data_list:
        if comment[key]:
            res[str(comment['id'])] = comment
            if str(comment[key]) in res.keys():
                res[str(comment[key])]['children'].append(res[str(comment['id'])])
        else:
            comment['children'] = []
            res[str(comment['id'])] = comment
    result_list = list([i for i in res.values() if i[key] is None])
    return result_list


def merge_two_field_list(field_list, detail_field_list):
    if detail_field_list is None:
        return field_list
    detail_field_dict = {field.name: field for field in detail_field_list}
    merge_field_list = []
    for field in field_list:
        if field.name in detail_field_dict:
            if isinstance(field, ForeignKeyField) or isinstance(field, ManyToManyField):
                detail_field = detail_field_dict[field.name]
                detail_field_list.remove(detail_field)
                detail_field.related_field_list = merge_two_field_list(field.related_field_list,
                                                                       detail_field.related_field_list)
                merge_field_list.append(detail_field)
            else:
                merge_field_list.append(field)
        else:
            merge_field_list.append(field)

    merge_field_list.extend(detail_field_list)
    return merge_field_list
