import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
import csv
import matplotlib.pyplot as plt

# Assuming the functions are in a file named `app.py`
from app import submit_data, visualize_data, entry_product_name, entry_cost_price, entry_sell_price, entry_month, entry_region

class TestProductDataEntry(unittest.TestCase):

    def setUp(self):
        self.test_file = 'test_data.csv'
        # Clear the CSV file before each test
        if os.path.isfile(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        # Clean up after each test
        if os.path.isfile(self.test_file):
            os.remove(self.test_file)

    @patch('app.messagebox.showerror')
    @patch('app.messagebox.showinfo')
    @patch('app.csv.writer')
    @patch('app.open', new_callable=MagicMock)
    def test_submit_data_success(self, mock_open, mock_csv_writer, mock_showinfo, mock_showerror):
        # Set up mock objects
        mock_file = MagicMock()
        mock_open.return_value = mock_file
        
        entry_product_name.insert(0, 'ProductA')
        entry_cost_price.insert(0, '10.00')
        entry_sell_price.insert(0, '15.00')
        entry_month.insert(0, '2024-08')
        entry_region.insert(0, 'Region1')

        submit_data()

        # Check if the file was opened in append mode
        mock_open.assert_called_with(self.test_file, 'a', newline='')
        
        # Check if the CSV writer was called correctly
        mock_csv_writer.assert_called()
        args, kwargs = mock_csv_writer.call_args
        written_data = args[0].write.call_args_list
        written_rows = [call[0][0] for call in written_data]

        # Verify that data was written correctly
        self.assertIn('ProductA', written_rows)
        self.assertIn('10.00', written_rows)
        self.assertIn('15.00', written_rows)
        self.assertIn('2024-08', written_rows)
        self.assertIn('Region1', written_rows)
        self.assertIn('5.00', written_rows)  # Profit/Loss

        mock_showinfo.assert_called_with("Success", f"{self.test_file} Saved Successfully!")

    @patch('app.messagebox.showerror')
    @patch('app.messagebox.showinfo')
    @patch('app.pd.read_csv')
    @patch('app.matplotlib.pyplot.show')
    def test_visualize_data(self, mock_plt_show, mock_read_csv, mock_showinfo, mock_showerror):
        # Create a DataFrame to mock read_csv
        df = pd.DataFrame({
            'Product': ['ProductA', 'ProductB'],
            'Cost': [10.00, 20.00],
            'Sell': [15.00, 25.00],
            'Month': ['2024-08', '2024-08'],
            'Region': ['Region1', 'Region2'],
            'Profit/Loss': [5.00, 5.00]
        })
        mock_read_csv.return_value = df

        visualize_data()

        # Check if the matplotlib plot was shown
        mock_plt_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()
