from __future__ import annotations

import sqlalchemy

from project.sqladmin_.model_view import SimpleMV
from project.sqladmin_.util.etc import format_datetime_, format_json_for_preview_, format_json_
from project.sqlalchemy_db_.sqlalchemy_model import VerificationCodeDBM


class VerificationCodeMV(SimpleMV, model=VerificationCodeDBM):
    name = "VerificationCode"
    name_plural = "VerificationCodes"
    icon = "fa-solid fa-envelope"
    column_list = [
        VerificationCodeDBM.id,
        VerificationCodeDBM.long_id,
        VerificationCodeDBM.slug,
        VerificationCodeDBM.creation_dt,
        VerificationCodeDBM.type,
        VerificationCodeDBM.value,
        VerificationCodeDBM.recipient,
        VerificationCodeDBM.user,
        VerificationCodeDBM.is_active,
        VerificationCodeDBM.extra_data
    ]
    form_columns = [
        VerificationCodeDBM.slug,
        VerificationCodeDBM.type,
        VerificationCodeDBM.value,
        VerificationCodeDBM.recipient,
        VerificationCodeDBM.user,
        VerificationCodeDBM.is_active,
        VerificationCodeDBM.extra_data
    ]
    column_sortable_list = sqlalchemy.inspect(VerificationCodeDBM).columns
    column_default_sort = [
        (VerificationCodeDBM.creation_dt, True)
    ]
    column_searchable_list = [
        VerificationCodeDBM.id,
        VerificationCodeDBM.long_id,
        VerificationCodeDBM.slug,
        VerificationCodeDBM.value,
        VerificationCodeDBM.recipient,
    ]
    column_formatters = {
        VerificationCodeDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt),
        VerificationCodeDBM.extra_data: lambda m, _: format_json_for_preview_(m.extra_data)
    }
    column_formatters_detail = {
        VerificationCodeDBM.creation_dt: lambda m, _: format_datetime_(m.creation_dt),
        VerificationCodeDBM.extra_data: lambda m, a: format_json_(m.extra_data),
    }
