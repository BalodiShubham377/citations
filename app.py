import sys
import requests
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout

API_URL = "https://devapi.beyondchats.com/api/get_message_with_sources"
TIMEOUT = 5  # Timeout for each request

class CitationsViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Citations Viewer")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.page_input = QLineEdit()
        self.page_input.setPlaceholderText("Enter page number")
        layout.addWidget(self.page_input)

        fetch_button = QPushButton("Fetch Citations")
        fetch_button.clicked.connect(self.fetch_citations)
        layout.addWidget(fetch_button)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)  # Make the text edit widget read-only
        layout.addWidget(self.text_edit)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def fetch_citations(self):
        try:
            page = int(self.page_input.text())
            response = requests.get(API_URL, params={"page": page}, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            print("Data from API:", data)  # Print data for debugging
            if isinstance(data, dict) and 'data' in data and 'data' in data['data']:
                citations = self.extract_citations(data['data']['data'])
                if citations:
                    self.display_citations(citations)
                else:
                    self.text_edit.setPlainText("No citations found.")
            else:
                self.text_edit.setPlainText("Unexpected data format from API.")
        except ValueError:
            self.text_edit.setPlainText("Please enter a valid page number.")
        except requests.exceptions.RequestException as e:
            self.text_edit.setPlainText(f"Error fetching data: {e}")
        except json.JSONDecodeError as e:
            self.text_edit.setPlainText(f"Error decoding JSON: {e}")

    def extract_citations(self, data):
        citations = []
        for item in data:
            if 'response' in item and 'source' in item:
                citation = {'response': item['response'], 'sources': []}
                for source in item['source']:
                    citation['sources'].append({'context': source['context'], 'link': source['link']})
                citations.append(citation)
        return citations

    def display_citations(self, citations):
        if citations:
            self.text_edit.clear()
            for citation in citations:
                self.text_edit.append(f"Response: {citation['response']}")
                self.text_edit.append("Sources:")
                for source in citation['sources']:
                    self.text_edit.append(f"- Context: {source['context']}")
                    if source['link']:
                        self.text_edit.append(f"  Link: {source['link']}")
                self.text_edit.append("\n")
        else:
            self.text_edit.setPlainText("No citations found.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CitationsViewer()
    window.show()
    sys.exit(app.exec_())

