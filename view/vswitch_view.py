# views/output_format.py

class OutputFormat:
    @staticmethod
    def format_result(result):
        if result['status']:
            return f"Success: {result['message']}"
        else:
            return f"Error: {result['message']}"
