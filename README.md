# Online-Store-Price-Checker
Checks the current price of a product on an online store

To set up, edit config.ini with:
1. The URL of the product you want to monitor
2. The HTML tags that containg the price
3. The standard (current) price of this product
4. Your email settings to allow email alerts to be sent

This script will download the given webpage, then parse the HTML for the given elements containing the price. This is then compared to the standard price set in config. If the price has lowered, an email alert will be sent to the designated recipients. If not, no email is sent.
