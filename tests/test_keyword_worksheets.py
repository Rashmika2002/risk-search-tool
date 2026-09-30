import unittest
from unittest.mock import patch

import cloud_sync


class FakeWorksheet:
    def __init__(self, title, values=None, spreadsheet=None):
        self.title = title
        self.values = values or []
        self.spreadsheet = spreadsheet

    def get_all_values(self):
        return [row[:] for row in self.values]

    def append_rows(self, rows):
        self.values.extend([row[:] for row in rows])

    def update(self, cell_range, values):
        if cell_range == 'A1:C1':
            if self.values:
                self.values[0] = values[0][:]
            else:
                self.values = [values[0][:]]

    def format(self, cell_range, formatting):
        pass

    def update_title(self, title):
        del self.spreadsheet.worksheets[self.title]
        self.title = title
        self.spreadsheet.worksheets[title] = self


class FakeSpreadsheet:
    def __init__(self, worksheets):
        self.worksheets = worksheets
        for worksheet in worksheets.values():
            worksheet.spreadsheet = self

    def worksheet(self, title):
        try:
            return self.worksheets[title]
        except KeyError:
            raise cloud_sync.gspread.exceptions.WorksheetNotFound(title)

    def add_worksheet(self, title, rows, cols):
        worksheet = FakeWorksheet(title, spreadsheet=self)
        self.worksheets[title] = worksheet
        return worksheet


class FakeClient:
    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet

    def open_by_key(self, sheet_id):
        return self.spreadsheet


class KeywordWorksheetTests(unittest.TestCase):
    def test_criminal_conviction_sheet_copies_standard_keywords(self):
        standard_rows = [
            ['Category', 'Keyword', 'Active'],
            ['Financial Crime', 'fraud', 'TRUE'],
            ['Legal & Regulatory', 'lawsuit', 'FALSE'],
        ]
        cloud = cloud_sync.CloudSync.__new__(cloud_sync.CloudSync)
        cloud.keywords_worksheet = FakeWorksheet('Keywords', standard_rows)
        cloud.criminal_conviction_worksheet = FakeWorksheet(
            cloud_sync.CRIMINAL_CONVICTION_WORKSHEET_NAME
        )

        cloud._populate_criminal_conviction_keywords()

        self.assertEqual(
            cloud.criminal_conviction_worksheet.values,
            [
                ['Financial Crime', 'fraud', 'TRUE'],
                ['Legal & Regulatory', 'lawsuit', 'FALSE'],
                ['Legal & Regulatory', 'Criminal Conviction', 'TRUE'],
            ],
        )

    def test_empty_standard_sheet_uses_all_default_keywords(self):
        cloud = cloud_sync.CloudSync.__new__(cloud_sync.CloudSync)
        cloud.keywords_worksheet = FakeWorksheet('Keywords', [['Category', 'Keyword', 'Active']])
        cloud.criminal_conviction_worksheet = FakeWorksheet(
            cloud_sync.CRIMINAL_CONVICTION_WORKSHEET_NAME
        )

        cloud._populate_criminal_conviction_keywords()

        self.assertEqual(
            cloud.criminal_conviction_worksheet.values[:-1],
            [list(row) for row in cloud_sync.DEFAULT_STANDARD_KEYWORDS],
        )
        self.assertEqual(
            cloud.criminal_conviction_worksheet.values[-1],
            ['Legal & Regulatory', 'Criminal Conviction', 'TRUE'],
        )

    def test_legacy_russian_sheet_is_renamed_and_new_sheet_created(self):
        standard_values = [
            ['Category', 'Keyword', 'Active'],
            *[list(row) for row in cloud_sync.DEFAULT_STANDARD_KEYWORDS],
        ]
        old_kuwait_sheet = FakeWorksheet(
            cloud_sync.LEGACY_RUSSIAN_KEYWORDS_WORKSHEET_NAME,
            [['Category', 'Keyword', 'Active'], ['Kuwait Risk', 'Example', 'TRUE']],
        )
        spreadsheet = FakeSpreadsheet({
            'Risk Searches': FakeWorksheet('Risk Searches', [['ID']]),
            'Keywords': FakeWorksheet('Keywords', standard_values),
            cloud_sync.LEGACY_RUSSIAN_KEYWORDS_WORKSHEET_NAME: old_kuwait_sheet,
        })
        client = FakeClient(spreadsheet)
        config = {
            'credentials_file': 'credentials.json',
            'sheet_id': 'test-sheet',
        }
        cloud = cloud_sync.CloudSync.__new__(cloud_sync.CloudSync)
        cloud.username = 'test-user'

        with patch.dict(cloud_sync.GOOGLE_SHEETS_CONFIG, config, clear=True), \
                patch.object(cloud_sync.os.path, 'exists', return_value=True), \
                patch.object(
                    cloud_sync.Credentials,
                    'from_service_account_file',
                    return_value=object(),
                ), \
                patch.object(cloud_sync.gspread, 'authorize', return_value=client), \
                patch('builtins.print'):
            cloud._connect_to_google_sheets()

        self.assertIs(cloud.kuwait_keywords_worksheet, old_kuwait_sheet)
        self.assertIn(cloud_sync.KUWAIT_KEYWORDS_WORKSHEET_NAME, spreadsheet.worksheets)
        self.assertNotIn(
            cloud_sync.LEGACY_RUSSIAN_KEYWORDS_WORKSHEET_NAME,
            spreadsheet.worksheets,
        )
        self.assertEqual(
            cloud.criminal_conviction_worksheet.get_all_values()[1:],
            [
                *[list(row) for row in cloud_sync.DEFAULT_STANDARD_KEYWORDS],
                ['Legal & Regulatory', 'Criminal Conviction', 'TRUE'],
            ],
        )

    def test_selector_exposes_standard_kuwait_and_criminal_sheets(self):
        cloud = cloud_sync.CloudSync.__new__(cloud_sync.CloudSync)

        self.assertEqual(
            [sheet['label'] for sheet in cloud.get_keyword_sheets()],
            [
                'Standard Keywords',
                'Kuwait keywords Sheet',
                'Standard + Criminal Conviction',
            ],
        )

    def test_criminal_conviction_sheet_is_readable_for_searches(self):
        cloud = cloud_sync.CloudSync.__new__(cloud_sync.CloudSync)
        cloud.keywords_worksheet = FakeWorksheet(
            'Keywords',
            [['Category', 'Keyword', 'Active'], ['Financial Crime', 'fraud', 'TRUE']],
        )
        cloud.kuwait_keywords_worksheet = FakeWorksheet(
            cloud_sync.KUWAIT_KEYWORDS_WORKSHEET_NAME,
            [['Category', 'Keyword', 'Active'], ['Kuwait Risk', 'Example', 'TRUE']],
        )
        cloud.criminal_conviction_worksheet = FakeWorksheet(
            cloud_sync.CRIMINAL_CONVICTION_WORKSHEET_NAME,
            [
                ['Category', 'Keyword', 'Active'],
                ['Financial Crime', 'fraud', 'TRUE'],
                ['Legal & Regulatory', 'Criminal Conviction', 'TRUE'],
                ['Legal & Regulatory', 'inactive term', 'FALSE'],
            ],
        )

        self.assertEqual(
            cloud.get_keywords(cloud_sync.CRIMINAL_CONVICTION_WORKSHEET_NAME),
            ['fraud', 'Criminal Conviction'],
        )


if __name__ == '__main__':
    unittest.main()
