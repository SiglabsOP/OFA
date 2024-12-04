# Options Flow Analyzer


 


Options Flow Analyzer

 Version 2.4
Developed by Sig Labs - Peter De Ceuster
 
  
 
 The Options Flow Analyzer is a desktop application built with PyQt5 that helps users detect unusual options activity in the stock market. It fetches live options data from Yahoo Finance, analyzes options based on volume and open interest spikes, and displays the anomalies in a user-friendly interface. It is designed for traders who want to identify significant market movements through options activity.

Features
Live Options Data: Fetches options chain data for any stock ticker from Yahoo Finance.
Anomaly Detection: Identifies unusual options activity by analyzing volume and open interest.
Customizable Thresholds: Adjust the anomaly threshold for volume and open interest spikes.
User Interface: Simple and intuitive UI built with PyQt5.
Notifications: Provides desktop notifications when unusual options activity is detected.
Ticker Persistence: Remembers the last entered stock ticker.
Help & About: In-app help and version information.


How It Works
Enter a Stock Ticker: Type the ticker of a stock (e.g., AAPL) in the input field.
Adjust the Anomaly Threshold: Use the slider to adjust the anomaly threshold multiplier for volume and open interest spikes.
Analyze Options: Click the "Analyze Options" button to fetch options data and detect unusual activity.
Review Results: The table will display the detected anomalies, including details like type (call/put), strike price, volume, open interest, and implied volatility.

GUI Overview
Ticker Input Field: Where you can input a stock ticker (e.g., AAPL).
Anomaly Threshold Slider: Adjust the sensitivity for detecting anomalies in options activity.
Analyze Button: Starts the analysis process to detect unusual activity.
Results Table: Displays detected anomalies with relevant options data. ( IV stands for Implied Volatility )


Notifications
When unusual options activity is detected, the app will send a desktop notification with the number of anomalies found.

Saving Ticker
The app saves the last entered ticker in a text file (last_ticker.txt) so you don’t have to re-enter it each time you start the app.




If you enjoy this program, buy me a coffee https://buymeacoffee.com/siglabo
You can use it free of charge or build upon my code. 
 
(c) Peter De Ceuster 2024
Software Distribution Notice: https://peterdeceuster.uk/doc/code-terms 
This software is released under the FPA General Code License.
 
