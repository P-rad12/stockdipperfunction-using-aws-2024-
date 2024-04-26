import json
import requests
import boto3
from datetime import datetime, timedelta

API_KEY = 'Your_api_key' #need to obtain this from alpha vantage
STOCKS = {
    'Facebook': 'META',  
    'Apple': 'AAPL',
    'Amazon': 'AMZN',
    'Netflix': 'NFLX',
    'Boeing': 'BA',
    'Google': 'GOOGL'
}
PERCENT_DROP_THRESHOLD = 5

def handler(event, context):
    ses_client = boto3.client('ses', region_name='us-east-1')
    sender = "seders email" #need to register this email in aws SES 
    recipient = "recipents mail"
    
    
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    print(f"Yesterday's date: {yesterday}")


    body = "Daily Stock Summary:\n\n"
    dipped_stocks_info = []
    has_dipped = False

    for name, symbol in STOCKS.items():

        response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}")
        data = response.json()

        
        print(f"API response for {name}: {json.dumps(data, indent=2)}")

        if 'Time Series (Daily)' in data:
            time_series = data['Time Series (Daily)']
            
            
            if yesterday in time_series:
                prev_day_data = time_series[yesterday]
                high_price = float(prev_day_data['2. high'])
                low_price = float(prev_day_data['3. low'])
                body += f"{name} ({symbol}) - High: ${high_price}, Low: ${low_price}\n"
                
                all_time_high = max(float(day['2. high']) for day in time_series.values())
                close_price = float(prev_day_data['4. close'])
                threshold_price = all_time_high * (1 - PERCENT_DROP_THRESHOLD / 100.0)
                
                if close_price < threshold_price:
                    has_dipped = True
                    dipped_stocks_info.append(f"{name} ({symbol}) - Current Price: ${close_price}, All-Time High: ${all_time_high}\n")
            else:
                
                print(f"No data found for {name} ({symbol}) on {yesterday}")
        else:
            print(f"'Time Series (Daily)' not found in API response for {name} ({symbol})")

    
    if has_dipped:
        body += "\n\nStocks that dipped below the threshold:\n" + "".join(dipped_stocks_info)
        subject = "Stock Alert: Price Drop Below Threshold"
    else:
        subject = "Daily Stock Summary"

    
    print("Final email body before sending:")  
    print(body)

    send_email(ses_client, sender, recipient, subject, body)

def send_email(ses_client, sender, recipient, subject, body):
    try:
        response = ses_client.send_email(
            Source=sender,
            Destination={'ToAddresses': [recipient]},
            Message={
                'Subject': {'Data': subject},
                'Body': {
                    'Text': {'Data': body}
                }
            }
        )
        
        print(f"Email sent with subject: {subject}. Response: {response['MessageId']}")
    except Exception as e:
        
        print(f"Error sending email: {e}")

