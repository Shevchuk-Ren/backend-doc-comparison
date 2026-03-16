list_table = {
    "document_type": "Document type",
    "main_purpose": "Main purpose",
    "key_points": "Key points",
    "pros": "Pros",
    "cons": "Cons",
    "risk_flags": "Risk Flags",
    "decision_summary": "Dicision Summary",
}


class ComparisonService:
    def __init__(self):
        self.table_list = list_table

    def comparison_table(self, files_data):
        table = [
            {
                "criterion": "Document type",
                "values": {
                    doc["filename"]: doc["summary"].get("document_type")
                    for doc in files_data
                },
            },
            {
                "criterion": "Main purpose",
                "values": {
                    doc["filename"]: doc["summary"].get("main_purpose")
                    for doc in files_data
                },
            },
            {
                "criterion": "Key points",
                "values": {
                    doc["filename"]: doc["summary"].get("key_points", [])
                    for doc in files_data
                },
            },
            {
                "criterion": "Pros",
                "values": {
                    doc["filename"]: doc["summary"].get("pros", [])
                    for doc in files_data
                },
            },
            {
                "criterion": "Cons",
                "values": {
                    doc["filename"]: doc["summary"].get("cons", [])
                    for doc in files_data
                },
            },
            {
                "criterion": "Risk flags",
                "values": {
                    doc["filename"]: doc["summary"].get("risk_flags", [])
                    for doc in files_data
                },
            },
            {
                "criterion": "Decision summary",
                "values": {
                    doc["filename"]: doc["summary"].get("decision_summary")
                    for doc in files_data
                },
            },
        ]

        return {"comparison_table": table}
