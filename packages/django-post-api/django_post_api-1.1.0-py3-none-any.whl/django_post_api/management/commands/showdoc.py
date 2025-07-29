import os
from pathlib import Path

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import get_resolver, reverse

from django_post_api.views import BaseAPIView


class Command(BaseCommand):
    def add_arguments(self, parser):
        # 可选参数使用 '--' 前缀
        parser.add_argument(
            '--upload',
            action='store_true',  # 当提供此参数时，将会在 options 中设置为 True
            help='Set this flag to change the behavior of the command'
        )
        parser.add_argument(
            '--init',
            action='store_true',  # 当提供此参数时，将会在 options 中设置为 True
            help='Set this flag to change the behavior of the command'
        )
        parser.add_argument(
            '--swagger',
            action='store_true',  # 当提供此参数时，将会在 options 中设置为 True
            help='Set this flag to change the behavior of the command'
        )

    def get_class_name(self, view_func):
        # 先用 view_class 下面的注释，没有的话用 view_func 里的 initkwargs 的name，处理 不同的链接使用相同的 class 的情况。
        view_class = view_func.view_class
        class_name = view_class.__doc__
        if class_name is None:
            view_initkwargs = view_func.view_initkwargs
            class_name = view_initkwargs.get("name", None)
        if class_name is None:
            model = getattr(view_class, "model", None)
            if model:
                class_name = model._meta.verbose_name
        if class_name is None:
            class_name = view_class.__name__

        return class_name

    def handle(self, *args, **options):
        all_name_list = []
        resolver = get_resolver(None)
        s_number = 1
        showdoc_data = getattr(settings, "SHOWDOC_DATA", None)
        api_key = showdoc_data['api_key']
        api_token = showdoc_data['api_token']
        for view_func, pattern in resolver.reverse_dict.items():
            view_class = getattr(view_func, "view_class", None)
            if not view_class or not issubclass(view_class, BaseAPIView):
                continue
            s_number += 1
            url = reverse(view_func)

            class_name = self.get_class_name(view_func)
            cat_name_dict = showdoc_data['cat_name_url_mapping']
            cat_name = showdoc_data.get("default_cat_name", "其他")
            for one_cat_url, one_cat_name in cat_name_dict.items():
                if pattern[1].startswith(one_cat_url):
                    cat_name = one_cat_name
                    break
            showdoc_str = f"""

[TOC]


#### 请求URL
` {url} `

{view_class.get_showdoc_content()}"""
            url = "https://www.showdoc.cc/server/api/item/updateByApi"

            json_data = {
                "cat_name": cat_name,  # 目录名 可选参数
                "page_title": class_name,  # 页面标题
                "page_content": showdoc_str,  # 页面内容
            }
            file_menu = os.path.join(settings.BASE_DIR, "showdoc", cat_name)
            if not os.path.exists(file_menu):
                os.makedirs(file_menu)
            filename = os.path.join(file_menu, f"{class_name}.txt")
            page_name = f"{cat_name}-{class_name}"
            if page_name not in all_name_list:
                all_name_list.append(page_name)
            else:
                print(f"有两个相同的页面名称：{page_name}")
                break

            if not options['init']:
                if os.path.exists(filename):
                    content = Path(filename).read_text(encoding='utf-8')
                    if content == showdoc_str:
                        continue
            print(view_func, pattern)
            print(cat_name, class_name)
            print(s_number)
            with open(filename, "w", encoding='utf-8') as f:
                f.write(showdoc_str)
                if options['upload']:
                    api_data = {
                        "api_key": api_key,
                        "api_token": api_token,
                        "s_number": s_number,  # 页面序号
                    }
                    api_data.update(json_data)
                    res = requests.post(url, json=api_data).json()
                    if res.get("error_message", None):
                        print(res.get("error_message"))
                        break
        if options['upload']:
            print("已保存到本地并上传到showdoc")
        else:
            print("已保存到本地")
