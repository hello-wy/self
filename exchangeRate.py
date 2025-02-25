def exchange_rate_calculator(amount, from_currency, to_currency, exchange_rate, unit=100):
    # 假设传入的汇率是以输入单位兑换到目标货币单位
    converted_amount = amount * exchange_rate / unit  # 以100为单位的换算
    return converted_amount

def different_rate_calculator(currency):
    amount = exchage_rate[currency]['amount']
    exchange_rate1 = exchage_rate[currency]['rate1']
    exchange_rate2 = exchage_rate[currency]['rate2']
    unit = exchage_rate[currency]['unit']
    
    converted_amount1 = amount * exchange_rate1 / unit 
    converted_amount2 = amount * exchange_rate2 / unit

    return abs(converted_amount1-converted_amount2)

JPY = 200000
rate1 = 0.476
rate2 = 0.480

exchage_rate={
    'JPY': {
        'rate1': 0.473,
        'rate2': 0.5,
        'amount': 200000,
        'unit': 100
    },
    'AUD':{
        'rate1':450,
        'rate2': 461,
        'amount': 2100,
        'unit': 100
    },
    'GBP':{
        'rate1':900,
        'rate2': 915,
        'amount': 550,
        'unit': 100
    }
}
# exchange_rate_calculator(JPY, 'JPY', 'cny', rate1, 100)
# amont = different_rate_calculator('JPY')
amont = different_rate_calculator('GBP')

print(f'{amont}')