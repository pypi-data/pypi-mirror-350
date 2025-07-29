#%%
from FXTransact import FXTrade,FXTransactWrapper



# %%
mytrade=FXTrade.from_id("36197090")
# %%
mytrade2=FXTransactWrapper.from_path()
# %%
mytrade2.trades
# %%
