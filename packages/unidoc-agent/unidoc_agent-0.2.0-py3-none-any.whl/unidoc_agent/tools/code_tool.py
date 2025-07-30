from unidoc_agent.base_tool import BaseTool

class CodeTool(BaseTool):
    def can_handle(self, file_path, mime_type):
        return mime_type and mime_type.startswith('text/')

    def extract_content(self, file_path):
        return f"Extracted content from code file: {file_path}"
