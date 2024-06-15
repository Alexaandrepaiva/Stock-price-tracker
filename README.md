# Stock-price-tracker

Investment web interface to notify the user of Brazilian Stocks trading opportunities.

## Description

The goal of this project is to develop a Python and Django web interface that:
- Periodically records the current price of brazilian stock prices;
- Allows the user to see the chart of the latest prices of any brazilian stock;
- Allows the user to configure a notification, via email, if there is a trading opportunity to buy or sell.

To configure a notification of a buying or selling opportunity, the user must:
- Choose the brazilian stock to be monitored;
- Set the parameters of the price tunnel;
- Set the frequency of the check (in minutes);
- Provide the email address to receive the notifications.

The system obtains and stores the price of Brazilian stocks registered in the Stock API https://fcsapi.com/api-v3/stock/latest?country=Brazil.

After configuring an email notification, if the value of the stock crosses any of the tunnel limits, the user will receive an email notifying them of the buying or selling opportunity.

## Preview 

TODO
