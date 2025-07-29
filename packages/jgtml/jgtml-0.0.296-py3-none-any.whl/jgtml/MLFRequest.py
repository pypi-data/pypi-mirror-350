# jgtml/mlfsvc.py

class MLFRequest:
	def __init__(self, instrument, timeframe, use_full=True, force_refresh=False, lag_period=1, total_lagging_periods=5, dropna=True, columns_to_keep=None, columns_to_drop=None, drop_bid_ask=False, patternname="ttf"):
		self.instrument = instrument
		self.timeframe = timeframe
		self.use_full = use_full
		self.force_refresh = force_refresh
		self.lag_period = lag_period
		self.total_lagging_periods = total_lagging_periods
		self.dropna = dropna
		self.columns_to_keep = columns_to_keep
		self.columns_to_drop = columns_to_drop
		self.drop_bid_ask = drop_bid_ask
		self.patternname = patternname

	def to_dict(self):
		return {
			"instrument": self.instrument,
			"timeframe": self.timeframe,
			"use_full": self.use_full,
			"force_refresh": self.force_refresh,
			"lag_period": self.lag_period,
			"total_lagging_periods": self.total_lagging_periods,
			"dropna": self.dropna,
			"columns_to_keep": self.columns_to_keep,
			"columns_to_drop": self.columns_to_drop,
			"drop_bid_ask": self.drop_bid_ask,
			"patternname": self.patternname,
		}
