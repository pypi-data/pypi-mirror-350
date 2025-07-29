import requests
from .util import get_response_json_with_check

field_mapping = {
    'accountCode': 'product_id',
    'benchmark': 'benchmark',
    'startDate': 'start_date',
    'endDate': 'end_date',
    'totalReturn': 'cumulative_return',
    'activeReturn': 'active_return',
    'latestWeekReturn': 'recent_week_return',
    'thisWeekReturn': 'weekly_return',
    'latestMonthReturn': 'recent_month_return',
    'thisMonthReturn': 'monthly_return',
    'ytdReturn': 'YTD_return',
    'annualTotalReturn': 'annualized_total_return',
    'annualActiveReturn': 'annualized_active_return',
    'annualTotalRisk': 'annualized_total_risk',
    'annualActiveRisk': 'annualized_active_risk',
    'maxDrawdown': 'maximum_drawdown',
    'sharpRatio': 'sharpe_ratio',
    'infoRatio': 'information_ratio',
    'sortinoRatio': 'sortino_ratio',
    'calmarRatio': 'calmar_ratio'
}


def get_performance_indicators(client,
                               post_investment_product_id):

    url = f"{client.base_url}/lib/portfolio/v1/perf"
    headers = client.get_headers()
    params = {
        'accountCode': post_investment_product_id
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        r = get_response_json_with_check(response)

        data = {}
        for item in r.get('data').keys():
            data[item] = r.get('data').get(item)

        return data
    except Exception as e:
        raise e
