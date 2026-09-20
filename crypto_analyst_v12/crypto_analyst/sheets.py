import os
def _ws(sa,sid,name):
    if not sa or not sid or not os.path.exists(sa): return None
    import gspread
    return gspread.service_account(filename=sa).open_by_key(sid).worksheet(name)
def sync_trade(sa,sid,row):
    w=_ws(sa,sid,"Trades")
    if w: w.append_row(row,value_input_option="USER_ENTERED")
def sync_setup(sa,sid,row):
    w=_ws(sa,sid,"Setups")
    if w: w.append_row(row,value_input_option="USER_ENTERED")
