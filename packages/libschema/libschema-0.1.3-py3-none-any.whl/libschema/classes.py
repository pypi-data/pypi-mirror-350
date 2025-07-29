# -*- coding: utf-8 -*-
"""
This file defines key classes for libSCHEMA.
"""

class ModEngine(object):
    def apply(self, seasonality, anomaly, periodics, history):
        raise NotImplementedError("ModEngine.apply")
        return (seasonality, anomaly, periodics)
    
    def coefficients(self):
        raise NotImplementedError("ModEngine.coefficients")
        return {}
    
    def from_data():
        raise NotImplementedError("ModEngine.from_data")
    
    def to_dict(self):
        raise NotImplementedError("ModEngine.to_dict")

    def from_dict(d):
        raise NotImplementedError("ModEngine.from_dict")
        

class Seasonality(object):
    def apply(self, period):
        raise NotImplementedError("Seasonality.apply")
    
    def apply_vec(self, period_array):
        raise NotImplementedError("Seasonality.apply_vec")
        
    def to_dict(self):
        raise NotImplementedError("Seasonality.to_dict")

    def from_dict(d):
        raise NotImplementedError("Seasonality.from_dict")


class Anomaly(object):
    def apply(self, periodic, period, anom_history):
        raise NotImplementedError("Anomaly.apply")
    
    def apply_vec(self, periodic, period, anom_history):
        raise NotImplementedError("Anomaly.apply_vec")
        
    def to_dict(self):
        raise NotImplementedError("Anomaly.to_dict")

    def from_dict(d):
        raise NotImplementedError("Anomaly.from_dict")
