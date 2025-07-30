from unidoc_agent.base_tool import BaseTool
import openpyxl

class ExcelTool(BaseTool):
    def can_handle(self, file_path, mime_type):
        return file_path.endswith('.xlsx')

    def extract_content(self, file_path):
        wb = openpyxl.load_workbook(file_path)
        text = ''
        for sheet in wb:
            for row in sheet.iter_rows(values_only=True):
                text += ' '.join(str(cell) for cell in row if cell) + '\n'
        return text