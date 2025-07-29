import requests
import pandas as pd
from .util import get_response_json_with_check

field_mapping = {
    'date': '净值日期',
    'unitNav': '单位净值',
    'accumNav': '累计净值',
    'adjustNav': '复权净值'
}


def get_post_investment_product_net(client,
                                    post_investment_product_id,
                                    start_date,
                                    end_date):

    url = f"{client.base_url}/lib/portfolio/v1/nav"
    headers = client.get_headers()
    params = {
        'accountCode': post_investment_product_id,
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
