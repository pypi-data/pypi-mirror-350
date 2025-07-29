import requests
import pandas as pd
from .util import get_response_json_with_check

field_mapping = {
    'date': '净值日期',
    'unitNav': '单位净值',
    'accumNav': '累计净值',
    'adjustNav': '复权净值'
}


def private_net(client,
                product_name=None,
                product_code=None,
                start_date=None,
                end_date=None):

    url = f"{client.base_url}/lib/asset/v1/nav"
    headers = client.get_headers()
    params = {
        'accountCode': product_code,
        'accountName': product_name,
        'startDate': start_date,
        'endDate': end_date
    }

    try:
        response = requests.get(url, headers=headers, params=params)
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
