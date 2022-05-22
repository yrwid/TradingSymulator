from app.Engine import Engine

class EngineImpl(Engine):
    def __init__(self, df):
        Engine.__init__(self, df)

    def set_strategy(self, strategy):
        pass

    # todo: set default values to start and end of df
    def run(self, start=None, stop=None):
        pass

    def get_current_run_data(self):
        pass