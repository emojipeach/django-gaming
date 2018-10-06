from utils import list_event_types, call_api, api_operation, headers, api_url

market_book = {'marketId': '1.148555305', 'isMarketDataDelayed': True, 'status': 'OPEN', 'betDelay': 0, 'bspReconciled': False, 'complete': True, 'inplay': False, 'numberOfWinners': 1, 'numberOfRunners': 3, 'numberOfActiveRunners': 3, 'lastMatchTime': '2018-10-04T16:38:49.270Z', 'totalMatched': 1364.38, 'totalAvailable': 58725.94, 'crossMatching': True, 'runnersVoidable': False, 'version': 2418347898, 'runners': [{'selectionId': 44508, 'handicap': 0.0, 'status': 'ACTIVE', 'lastPriceTraded': 1.62, 'totalMatched': 0.0, 'ex': {'availableToBack': [{'price': 1.59, 'size': 345.92}, {'price': 1.58, 'size': 136.84}, {'price': 1.57, 'size': 44.2}], 'availableToLay': [{'price': 1.63, 'size': 110.7}, {'price': 1.64, 'size': 96.69}, {'price': 1.65, 'size': 199.9}], 'tradedVolume': []}}, {'selectionId': 66483, 'handicap': 0.0, 'status': 'ACTIVE', 'lastPriceTraded': 6.4, 'totalMatched': 0.0, 'ex': {'availableToBack': [{'price': 5.6, 'size': 12.15}, {'price': 5.5, 'size': 44.83}, {'price': 5.3, 'size': 35.34}], 'availableToLay': [{'price': 6.6, 'size': 199.76}, {'price': 6.8, 'size': 10.73}, {'price': 7.0, 'size': 61.49}], 'tradedVolume': []}}, {'selectionId': 58805, 'handicap': 0.0, 'status': 'ACTIVE', 'lastPriceTraded': 4.6, 'totalMatched': 0.0, 'ex': {'availableToBack': [{'price': 4.5, 'size': 10.17}, {'price': 4.4, 'size': 61.92}, {'price': 4.3, 'size': 10.58}], 'availableToLay': [{'price': 5.0, 'size': 204.42}, {'price': 5.1, 'size': 20.75}, {'price': 5.2, 'size': 15.7}], 'tradedVolume': []}}]}

market_info = {'marketId': '1.148555305', 'marketName': 'Match Odds', 'marketStartTime': '2018-10-07T16:30:00.000Z', 'totalMatched': 1369.81, 'runners': [{'selectionId': 44508, 'runnerName': 'Sevilla', 'handicap': 0.0, 'sortPriority': 1}, {'selectionId': 66483, 'runnerName': 'Celta Vigo', 'handicap': 0.0, 'sortPriority': 2}, {'selectionId': 58805, 'runnerName': 'The Draw', 'handicap': 0.0, 'sortPriority': 3}], 'eventType': {'id': '1', 'name': 'Soccer'}, 'competition': {'id': '117', 'name': 'Spanish La Liga'}, 'event': {'id': '28920121', 'name': 'Sevilla v Celta Vigo', 'countryCode': 'ES', 'timezone': 'Europe/London', 'openDate': '2018-10-07T16:30:00.000Z'}}


for i in range(len(market_info['runners'])):
    if market_info['runners'][i]['selectionId'] == market_book['runners'][i]['selectionId']:
        market_info['runners'][i]['latestOdds'] = market_book['runners'][i]['lastPriceTraded']

print(market_info)