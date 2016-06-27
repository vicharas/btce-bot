#/usr/bin/python
# Copyright (c) 2013 Alan McIntyre

import time

import btceapi
import btcebot
from logger import MarketDataLogger

def run(database_path):
    logger= MarketDataLogger(('ltc_btc',), database_path)
    #logger= MarketDataLogger(("btc_usd", "ltc_usd"), database_path)

    # Create a bot and add the logger to it.
    bot = btcebot.Bot()
    bot.addTrader(logger)

    # Add an error handler so we can print info about any failures
    # bot.addErrorHandler(onBotError)    

    # The bot will provide the logger with updated information every
    # 60 seconds.
    bot.setCollectionInterval(60)
    bot.start()
    print "Running; press Ctrl-C to stop"

    try:
        while 1:
            # you can do anything else you prefer in this loop while 
            # the bot is running in the background
            time.sleep(3600)
            
    except KeyboardInterrupt:
        print "Stopping..."
    finally:    
        bot.stop()
            
        
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Simple range trader example.')
    parser.add_argument('--db-path', default='btce.db',
                        help='Path to the logger database.')

    args = parser.parse_args()
    run(args.db_path)
