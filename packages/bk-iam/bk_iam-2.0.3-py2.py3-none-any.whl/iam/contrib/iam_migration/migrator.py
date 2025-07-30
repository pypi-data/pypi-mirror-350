# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making
蓝鲸智云 - 权限中心 Python SDK(iam-python-sdk) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""


import codecs
import json
import os
import sys

from django.conf import settings

from iam.contrib.iam_migration import exceptions
from iam.contrib.iam_migration.utils import do_migrate


def upsert_system_render(data):
    resource_api_host = getattr(settings, "BK_IAM_RESOURCE_API_HOST", None)
    if resource_api_host:
        data["provider_config"]["host"] = resource_api_host


renders = {"upsert_system": upsert_system_render}


class IAMMigrator(object):
    def __init__(self, migration_json):
        self.migration_json = migration_json
        self._bk_app_code = getattr(settings, "APP_CODE", "")
        self._bk_app_secret = settings.SECRET_KEY
        self._bk_app_tenant_id = self.get_tenant_id()

    @staticmethod
    def get_tenant_id():
        """
        获取应用所属的租户 ID
        Note: BKPAAS_APP_TENANT_ID 和 BK_APP_TENANT_ID 的含义不一样
            BKPAAS_APP_TENANT_ID 是应用的租户模式标识，表示应用是全租户还是单租户
            BK_APP_TENANT_ID 是应用所属的租户 ID，表示应用是属于哪个租户的，即由哪个租户产生的
        """
        # PaaS 平台上部署运行的应用，会自动内置 BKPAAS_APP_TENANT_ID 环境变量，表示应用是全租户的还是单租户的
        tenant_id = os.environ.get("BKPAAS_APP_TENANT_ID")
        if tenant_id is not None:
            # 空字符串表示全租户应用，则返回 system，因为全租户应用只能在运营租户 (system) 下创建
            return tenant_id or "system"

        # 如果从环境变量获取不到，即非 PaaS 平台上运行，则需要从配置中获取
        # 注意：对于单租户应用，BK_APP_TENANT_ID 可以不设置
        #  对于全租户应用，BK_APP_TENANT_ID 必须设置，建议设置为 system
        return getattr(settings, "BK_APP_TENANT_ID", "")

    def migrate(self):
        iam_host = getattr(settings, "BK_IAM_APIGATEWAY_URL", "")
        if iam_host == "":
            raise exceptions.MigrationFailError("settings.BK_IAM_APIGATEWAY_URL should be set")

        # only trigger migrator at db migrate
        if "migrate" not in sys.argv:
            return

        if getattr(settings, "BK_IAM_SKIP", False):
            return

        json_path = getattr(settings, "BK_IAM_MIGRATION_JSON_PATH", "support-files/iam/")
        file_path = os.path.join(settings.BASE_DIR, json_path, self.migration_json)

        with codecs.open(file_path, mode="r", encoding="utf-8") as fp:
            data = json.load(fp=fp)

        # data pre render
        for op in data["operations"]:
            if op["operation"] in renders:
                renders[op["operation"]](op["data"])

        ok, _ = do_migrate.api_ping(iam_host)
        if not ok:
            raise exceptions.NetworkUnreachableError("bk iam ping error")

        ok = do_migrate.do_migrate(data, iam_host, self._bk_app_code, self._bk_app_secret, self._bk_app_tenant_id)
        if not ok:
            raise exceptions.MigrationFailError("iam migrate fail")
