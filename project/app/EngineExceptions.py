class InconsistencyData(Exception):
    """data with gap bigger than one week is reported as error"""

class RedundantEdgeData(Exception):
    """redundant start or stop position"""

class EdgeDateNotExist(Exception):
    """Edge date doesn't exist in loaded data"""
