import os
from datetime import datetime
from fpdf import FPDF


class ExportManager:
    """Export conversations to PDF and Text"""
    
    def __init__(self):
        self.history = []
        self.export_folder = "./exports"
        os.makedirs(self.export_folder, exist_ok=True)
    
    def add_conversation(self, question, reviews, answer):
        """Add conversation to history"""
        self.history.append({
            "question": question,
            "reviews": reviews,
            "answer": answer,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    def export_to_text(self):
        """Export to text file"""
        if not self.history:
            return None
        
        filename = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = os.path.join(self.export_folder, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("AI DATA ASSISTANT - CONVERSATION EXPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            for idx, conv in enumerate(self.history, 1):
                f.write(f"[{idx}] {conv['time']}\n")
                f.write(f"Q: {conv['question']}\n")
                f.write(f"A: {conv['answer']}\n")
                f.write("-" * 80 + "\n\n")
        
        return filepath
    
    def export_to_pdf(self):
        """Export to PDF file"""
        if not self.history:
            return None
        
        filename = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.export_folder, filename)
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, "AI DATA ASSISTANT - CONVERSATION EXPORT", ln=True)
        
        pdf.set_font("Arial", "", 8)
        for idx, conv in enumerate(self.history, 1):
            pdf.set_font("Arial", "B", 9)
            pdf.cell(0, 6, f"{idx}. {conv['time']}", ln=True)
            pdf.set_font("Arial", "", 8)
            pdf.multi_cell(0, 4, f"Q: {conv['question']}\nA: {conv['answer']}")
            pdf.ln(1)
        
        pdf.output(filepath)
        return filepath
    
    def clear_history(self):
        """Clear history"""
        self.history = []
