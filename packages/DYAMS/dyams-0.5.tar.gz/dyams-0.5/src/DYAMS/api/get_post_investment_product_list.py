import requests
import pandas as pd
from .util import get_response_json_with_check

field_mapping = {
    'accountName': 'post_investment_product_name',  # 产品名称
    'accountCode': 'post_investment_product_id',    # 产品代码
    'openDate': 'establishment_date',               # 成立日期
    'accountType': 'product_type',                  # 账户类型作为产品类型
    'benchmark': 'benchmark',                       # 参考基准
    'user': 'creator',                              # 用户作为创建人
    'netValueStartDate': 'NAV_start_date',          # 净值开始日期
    'netValueDate': 'latest_NAV_date',              # 最新净值日期
    'navFrequency': 'NAV_update_frequency'          # 净值更新频率
}


def get_post_investment_product_list(client,
                                     post_investment_product_id=None):

    url = f"{client.base_url}/lib/portfolio/v1/list"
    headers = client.get_headers()
    data = "[]"
    if post_investment_product_id:
        data = "[\"" + post_investment_product_id + "\"]"

    try:
        response = requests.post(url, headers=headers, data=data)
        r = get_response_json_with_check(response)

        rows = []
        for item in r.get('list'):
            row = {}
            for api_field, our_field in field_mapping.items():
                row[our_field] = item.get(api_field, None)
            rows.append(row)

        df = pd.DataFrame(rows)
        return df
    except Exception as e:
        raise e
