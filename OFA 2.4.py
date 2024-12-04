import sys
import os
import pandas as pd
import numpy as np
import yfinance as yf
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
    QLabel, QLineEdit, QPushButton, QSlider, QMessageBox, QHBoxLayout, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon
from plyer import notification

 
# Fetch live options data (c) SIG Labs - you can use this source code, or build further upon it. See the license for more info.
def fetch_options_data(ticker):
    """
    Fetches options chain data for a given ticker using Yahoo Finance.
    """
    try:
        stock = yf.Ticker(ticker)
        options_dates = stock.options  # Expiry dates for options
        
        if not options_dates:
            print(f"No options data available for {ticker}.")
            return None

        # Fetch options for the earliest expiry date as an example
        options_data = stock.option_chain(options_dates[0])
        
        calls = options_data.calls
        puts = options_data.puts

        # Combine calls and puts into one DataFrame
        calls["Type"] = "Call"
        puts["Type"] = "Put"
        options_df = pd.concat([calls, puts], ignore_index=True)

        return options_df
    except Exception as e:
        print(f"Error fetching options data for {ticker}: {e}")
        return None

# Analyze unusual options activity
def analyze_options_activity(options_df, volume_threshold=2.0, oi_threshold=2.0):
    """
    Identifies unusual options activity based on volume and open interest spikes.
    """
    if options_df is None or options_df.empty:
        print("No options data to analyze.")
        return pd.DataFrame()

    # Add rolling averages for volume and open interest (assume some historical data)
    options_df["VolumeAnomaly"] = options_df["volume"] > (options_df["volume"].mean() * volume_threshold)
    options_df["OIAnomaly"] = options_df["openInterest"] > (options_df["openInterest"].mean() * oi_threshold)

    # Filter rows with anomalies
    anomalies = options_df[(options_df["VolumeAnomaly"]) | (options_df["OIAnomaly"])]

    return anomalies

class OptionsFlowAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Options Flow Analyzer")
        self.setGeometry(100, 100, 900, 700)
        self.setWindowIcon(QIcon("options_icon.png"))
        self.set_theme()

        self.main_widget = QWidget(self)
        self.layout = QVBoxLayout(self.main_widget)
        self.threshold = 2.0  # Default threshold multiplier

        self.add_widgets()
        self.setCentralWidget(self.main_widget)

        # Load the last ticker on start
        self.load_last_ticker()

    def set_theme(self):
        """
        Sets a dark theme for the application.
        """
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(33, 37, 43))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.setPalette(palette)

    def add_widgets(self):
        """
        Adds the main widgets to the GUI.
        """
        title = QLabel("Options Flow Analyzer", self)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16))
        self.layout.addWidget(title)
        self.setWindowIcon(QIcon("logo.png"))


        # Menu buttons for Help and About
        menu_layout = QHBoxLayout()
        help_button = QPushButton("Help", self)
        help_button.clicked.connect(self.show_help)
        about_button = QPushButton("About", self)
        about_button.clicked.connect(self.show_about)
        menu_layout.addWidget(help_button)
        menu_layout.addWidget(about_button)
        self.layout.addLayout(menu_layout)

        # Ticker input
        self.ticker_input = QLineEdit(self)
        self.ticker_input.setPlaceholderText("Enter stock ticker (e.g., AAPL)")
        self.layout.addWidget(self.ticker_input)

        # Threshold slider for volume anomalies
        self.threshold_slider = QSlider(Qt.Horizontal, self)
        self.threshold_slider.setMinimum(1)
        self.threshold_slider.setMaximum(10)
        self.threshold_slider.setValue(int(self.threshold))
        self.threshold_slider.valueChanged.connect(self.update_threshold)
        self.layout.addWidget(QLabel("Anomaly Threshold Multiplier:"))
        self.layout.addWidget(self.threshold_slider)

        # Current threshold label
        self.threshold_label = QLabel(f"Threshold: {self.threshold:.1f}", self)
        self.layout.addWidget(self.threshold_label)

        # Analyze button
        self.analyze_button = QPushButton("Analyze Options", self)
        self.analyze_button.clicked.connect(self.on_analyze_button_clicked)
        self.layout.addWidget(self.analyze_button)

        # Table to display results
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Type", "Strike", "Volume", "Open Interest", "IV", "Anomaly"])
        self.layout.addWidget(self.table)

    def update_threshold(self):
        """
        Updates the threshold value based on the slider.
        """
        self.threshold = self.threshold_slider.value()
        self.threshold_label.setText(f"Threshold: {self.threshold:.1f}")

    def on_analyze_button_clicked(self):
        """
        Fetches and analyzes options data for the given ticker.
        """
        ticker = self.ticker_input.text().strip().upper()
        if not ticker:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid stock ticker.")
            return

        # Fetch options data
        options_data = fetch_options_data(ticker)
        if options_data is None or options_data.empty:
            QMessageBox.warning(self, "No Data", f"No options data available for {ticker}.")
            return

        # Analyze anomalies
        anomalies = analyze_options_activity(options_data, volume_threshold=self.threshold, oi_threshold=self.threshold)

        # Update GUI with results
        self.update_table(anomalies)

    def update_table(self, anomalies):
        """
        Updates the table with detected anomalies.
        """
        if anomalies.empty:
            QMessageBox.information(self, "No Anomalies", "No unusual options activity detected.")
            self.table.setRowCount(0)
            return

        self.table.setRowCount(len(anomalies))
        for row, (_, anomaly) in enumerate(anomalies.iterrows()):
            self.table.setItem(row, 0, QTableWidgetItem(anomaly["Type"]))
            self.table.setItem(row, 1, QTableWidgetItem(f"{anomaly['strike']:.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(f"{anomaly['volume']}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{anomaly['openInterest']}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{anomaly['impliedVolatility']:.2%}"))
            self.table.setItem(row, 5, QTableWidgetItem("Yes" if anomaly["VolumeAnomaly"] or anomaly["OIAnomaly"] else "No"))

        notification.notify(
            title="Options Flow Alert",
            message=f"Detected {len(anomalies)} unusual options activities.",
            timeout=10
        )

    def show_help(self):
        """
        Displays a help section with information on how to use the app.
        """
        help_text = """
        <b>Options Flow Analyzer</b><br><br>
        This application helps you detect unusual options activity based on volume, open interest, 
        and implied volatility changes.<br><br>
        <b>Steps to Use:</b><br>
        1. Enter a stock ticker (e.g., AAPL) in the input field.<br>
        2. Adjust the anomaly threshold using the slider.<br>
        3. Click 'Analyze Options' to detect unusual activity.<br>
        4. Review detected anomalies in the table.<br>
        """
        QMessageBox.information(self, "Help", help_text)

    def show_about(self):
        """
        Displays an about section.
        """
        about_text = """
        <b>Options Flow Analyzer</b><br><br>
        Version: 2.4<br>
        (c) 2024 Peter De Ceuster<br><br>
        This application analyzes options flow to detect unusual trading activity. Visit us at peterdeceuster.uk
        """
        QMessageBox.information(self, "About", about_text)

    def save_last_ticker(self):
        """
        Saves the last entered ticker to a file.
        """
        with open("last_ticker.txt", "w") as file:
            file.write(self.ticker_input.text().strip())

    def load_last_ticker(self):
        """
        Loads the last ticker entered by the user, if it exists.
        """
        if os.path.exists("last_ticker.txt"):
            with open("last_ticker.txt", "r") as file:
                self.ticker_input.setText(file.read().strip())

    def closeEvent(self, event):
        """
        Saves the last ticker on application close.
        """
        self.save_last_ticker()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OptionsFlowAnalyzer()
    window.showMaximized()  # Start the window maximized

    window.show()
    sys.exit(app.exec_())
