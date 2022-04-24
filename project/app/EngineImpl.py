from app.Engine import Engine

class EngineImpl(Engine):
    def __init__(self, df):
        Engine.__init__(df)

    def set_strategy(self, strategy):
        pass

    def run(self, start, stop):
        pass
