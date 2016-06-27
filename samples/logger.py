#!/usr/bin/python
# Copyright (c) 2013 Alan McIntyre

import time

import btcebot

class MarketDataLogger(btcebot.TraderBase):
    '''
    This "trader" simply logs all of the updates it receives from the bot.
    '''
    def __init__(self, pairs, database_path):
        btcebot.TraderBase.__init__(self, pairs)
        self.database_path = database_path
        self.db = None
        self.trade_history_seen = {}
       
    def getDB(self):
        # The database is lazily created here instead of the constructor
        # so that it can be created and used in the bot's thread.
        if self.db is None:
            self.db = btcebot.MarketDatabase(self.database_path)

        return self.db
    
    def onExit(self):
        if self.db is not None:
            self.db.close()
       
    # This overrides the onNewDepth method in the TraderBase class, so the 
    # framework will automatically pick it up and send updates to it.
    def onNewDepth(self, t, pair, asks, bids):
        print "%s Entering new %s depth" % (t, pair)
        self.getDB().insertDepth(t, pair, asks, bids)

    # This overrides the onNewTradeHistory method in the TraderBase class, so the 
    # framework will automatically pick it up and send updates to it.
    def onNewTradeHistory(self, t, pair, trades):
        history = self.trade_history_seen.setdefault(pair, set())
        
        new_trades = filter(lambda trade: trade.tid not in history, trades)
        if new_trades:
            print "%s Entering %d new %s trades" % (t, len(new_trades), pair)
            self.getDB().insertTradeHistory(new_trades)
            history.update(t.tid for t in new_trades)
