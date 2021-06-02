class DatasetError(Exception):
    def __init__(self, start, end):
        message="start or end is not defined"
        super().__init__(f'{message}. start: {start}, end: {end} should be dates in format: yyyy-mm-dd')

class DataError(Exception):
    def __init__(self, start, end):
        super().__init__(f'No data about ticker is given')

class StrategyNameError(Exception):
    def __init__(self, strategy):
        super().__init__(f'No strategy "{strategy}" was found')

class NoStrategyError(Exception):
    def __init__(self):
        super().__init__(f'\nStrategy is not defined, use:\n\n>>> CPF.set_traid_strategy("strategy_name")')
