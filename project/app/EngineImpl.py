from app.Engine import Engine

class EngineImpl(Engine):
    def __init__(self, df):
        Engine.__init__(df)

    def set_strategy(self, strategy):
        pass

    # todo: set default values to start and end of df
    def run(self, start=0, stop=0):
        pass
