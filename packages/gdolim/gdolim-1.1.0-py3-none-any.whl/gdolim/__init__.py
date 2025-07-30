import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
import xlsxwriter.utility

logger = logging.getLogger('gdolim')


class GoogleSheetsClient:
    def __init__(self, google_service_account_credentials, spreadsheet_id, spreadsheet_name='Sheet1'):
        google_service_account_credentials = service_account.Credentials.from_service_account_info(google_service_account_credentials)
        self.google_sheets_resource = build('sheets', 'v4', credentials=google_service_account_credentials)

        self.spreadsheet_name = spreadsheet_name
        self.spreadsheet_id = spreadsheet_id
        self.rows = []
        self.headers = []
        self.items = []

    def __enter__(self):
        self.reload()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def reload(self, spreadsheet_range='A:ZZ'):
        result = self.google_sheets_resource.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range=f'{self.spreadsheet_name}!{spreadsheet_range}').execute()
        rows = result.get('values', [])

        if not rows:
            logger.warning(f'no records for spreadsheet="{self.spreadsheet_id}"')
            return

        self.rows = rows
        rows = iter(rows)
        headers = next(rows)
        items = []
        for row_index, row in enumerate(rows):
            item = {}
            for header_index, header in enumerate(headers):
                item[header] = row[header_index] if len(row) > header_index else ''

            item['id'] = row_index + 1  # we skipped the headers
            items.append(item)

        self.headers = headers
        self.items = items

    def set_item_field(self, item, field_name, value):
        row = item['id'] + 1
        if field_name not in self.headers:
            self.add_header(field_name)

        column_index = self.headers.index(field_name)
        range_start_letter = xlsxwriter.utility.xl_col_to_name(column_index)
        range_end_letter = xlsxwriter.utility.xl_col_to_name(column_index + 1)
        spreadsheet_range = f'{self.spreadsheet_name}!{range_start_letter}{row}:{range_end_letter}{row}'
        self._update_cell(spreadsheet_range, value)
        self.reload()

    def add_header(self, field_name):
        new_header_index = len(self.headers)
        range_start_letter = xlsxwriter.utility.xl_col_to_name(new_header_index)
        range_end_letter = xlsxwriter.utility.xl_col_to_name(new_header_index + 1)
        spreadsheet_range = f'{self.spreadsheet_name}!{range_start_letter}:{range_end_letter}'
        self._update_cell(spreadsheet_range, field_name)
        self.reload()

    def _update_cell(self, spreadsheet_range, value):
        self.google_sheets_resource.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=spreadsheet_range,
            body={
                "majorDimension": "ROWS",
                "values": [[value]]
            },
            valueInputOption="USER_ENTERED"
        ).execute()
