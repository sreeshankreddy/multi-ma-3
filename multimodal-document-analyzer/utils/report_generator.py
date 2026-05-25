"""
Report generation module.
Generates downloadable PDF and text reports with analysis results.
"""

import os
from typing import Dict, List, Any
from datetime import datetime
import json
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


class ReportGenerator:
    """
    Generates professional PDF and text reports from document analysis results.
    Includes summary, insights, tables, keywords, and other analysis output.
    """

    @staticmethod
    def generate_pdf_report(analysis_results: Dict[str, Any], output_path: str,
                          document_title: str = "Document Analysis Report") -> str:
        """
        Generate PDF report from analysis results.

        Args:
            analysis_results (Dict): Dictionary containing analysis results.
            output_path (str): Path to save PDF report.
            document_title (str): Title for the report.

        Returns:
            str: Path to saved PDF file.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=TA_CENTER
        )

        story.append(Paragraph(document_title, title_style))
        story.append(Spacer(1, 0.2 * inch))

        # Metadata
        metadata_style = ParagraphStyle(
            'Metadata',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.grey,
        )

        timestamp = datetime.now().strftime("%B %d, %Y at %H:%M")
        story.append(Paragraph(f"Generated: {timestamp}", metadata_style))
        story.append(Spacer(1, 0.3 * inch))

        # Summary Section
        if 'summary' in analysis_results and analysis_results['summary']:
            story.append(Paragraph("Summary", styles['Heading2']))
            story.append(Paragraph(analysis_results['summary'], styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))

        # Key Insights Section
        if 'key_insights' in analysis_results:
            story.append(Paragraph("Key Insights", styles['Heading2']))
            for insight in analysis_results.get('key_insights', [])[:5]:
                story.append(Paragraph(f"• {insight}", styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))

        # Keywords Section
        if 'keywords' in analysis_results and analysis_results['keywords']:
            story.append(Paragraph("Keywords", styles['Heading2']))
            keywords_text = ", ".join(analysis_results['keywords'][:10])
            story.append(Paragraph(keywords_text, styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))

        # Entities Section
        if 'entities' in analysis_results:
            story.append(Paragraph("Extracted Entities", styles['Heading2']))
            entities = analysis_results['entities']

            for entity_type, entity_list in entities.items():
                if entity_list:
                    entities_text = ", ".join(entity_list[:5])
                    story.append(Paragraph(f"<b>{entity_type}:</b> {entities_text}", styles['Normal']))

            story.append(Spacer(1, 0.2 * inch))

        # Sentiment Analysis Section
        if 'sentiment' in analysis_results:
            story.append(Paragraph("Sentiment Analysis", styles['Heading2']))
            sentiment = analysis_results['sentiment']
            if isinstance(sentiment, dict):
                story.append(Paragraph(f"<b>Overall Sentiment:</b> {sentiment.get('overall_sentiment', 'N/A')}", styles['Normal']))
                story.append(Paragraph(f"<b>Confidence:</b> {sentiment.get('confidence', 'N/A')}", styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))

        # Topics Section
        if 'topics' in analysis_results and analysis_results['topics']:
            story.append(Paragraph("Main Topics", styles['Heading2']))
            topics_text = ", ".join(analysis_results['topics'][:5])
            story.append(Paragraph(topics_text, styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))

        # Statistics Section
        if 'statistics' in analysis_results:
            story.append(Paragraph("Document Statistics", styles['Heading2']))
            stats = analysis_results['statistics']
            stats_data = [
                ['Metric', 'Value'],
                ['Total Words', str(stats.get('total_words', 'N/A'))],
                ['Total Sentences', str(stats.get('total_sentences', 'N/A'))],
                ['Unique Words', str(stats.get('unique_words', 'N/A'))],
                ['Average Word Length', f"{stats.get('average_word_length', 0):.2f}"],
                ['Reading Time (minutes)', str(stats.get('reading_time_minutes', 'N/A'))],
            ]

            stats_table = Table(stats_data, colWidths=[3 * inch, 2 * inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))

            story.append(stats_table)
            story.append(Spacer(1, 0.2 * inch))

        # Build PDF
        doc.build(story)
        return output_path

    @staticmethod
    def generate_text_report(analysis_results: Dict[str, Any], output_path: str,
                           document_title: str = "Document Analysis Report") -> str:
        """
        Generate text report from analysis results.

        Args:
            analysis_results (Dict): Dictionary containing analysis results.
            output_path (str): Path to save text report.
            document_title (str): Title for the report.

        Returns:
            str: Path to saved text file.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            # Write header
            f.write("=" * 80 + "\n")
            f.write(document_title.center(80) + "\n")
            f.write("=" * 80 + "\n\n")

            timestamp = datetime.now().strftime("%B %d, %Y at %H:%M")
            f.write(f"Generated: {timestamp}\n\n")

            # Summary Section
            if 'summary' in analysis_results and analysis_results['summary']:
                f.write("SUMMARY\n")
                f.write("-" * 40 + "\n")
                f.write(analysis_results['summary'] + "\n\n")

            # Key Insights
            if 'key_insights' in analysis_results:
                f.write("KEY INSIGHTS\n")
                f.write("-" * 40 + "\n")
                for insight in analysis_results.get('key_insights', [])[:5]:
                    f.write(f"• {insight}\n")
                f.write("\n")

            # Keywords
            if 'keywords' in analysis_results and analysis_results['keywords']:
                f.write("KEYWORDS\n")
                f.write("-" * 40 + "\n")
                keywords_text = ", ".join(analysis_results['keywords'][:10])
                f.write(keywords_text + "\n\n")

            # Entities
            if 'entities' in analysis_results:
                f.write("EXTRACTED ENTITIES\n")
                f.write("-" * 40 + "\n")
                entities = analysis_results['entities']
                for entity_type, entity_list in entities.items():
                    if entity_list:
                        entities_text = ", ".join(entity_list[:5])
                        f.write(f"{entity_type}: {entities_text}\n")
                f.write("\n")

            # Sentiment
            if 'sentiment' in analysis_results:
                f.write("SENTIMENT ANALYSIS\n")
                f.write("-" * 40 + "\n")
                sentiment = analysis_results['sentiment']
                if isinstance(sentiment, dict):
                    f.write(f"Overall Sentiment: {sentiment.get('overall_sentiment', 'N/A')}\n")
                    f.write(f"Confidence: {sentiment.get('confidence', 'N/A')}\n")
                f.write("\n")

            # Topics
            if 'topics' in analysis_results and analysis_results['topics']:
                f.write("MAIN TOPICS\n")
                f.write("-" * 40 + "\n")
                topics_text = ", ".join(analysis_results['topics'][:5])
                f.write(topics_text + "\n\n")

            # Statistics
            if 'statistics' in analysis_results:
                f.write("DOCUMENT STATISTICS\n")
                f.write("-" * 40 + "\n")
                stats = analysis_results['statistics']
                f.write(f"Total Words: {stats.get('total_words', 'N/A')}\n")
                f.write(f"Total Sentences: {stats.get('total_sentences', 'N/A')}\n")
                f.write(f"Unique Words: {stats.get('unique_words', 'N/A')}\n")
                f.write(f"Average Word Length: {stats.get('average_word_length', 0):.2f}\n")
                f.write(f"Reading Time (minutes): {stats.get('reading_time_minutes', 'N/A')}\n\n")

            # Footer
            f.write("=" * 80 + "\n")
            f.write("End of Report\n")
            f.write("=" * 80 + "\n")

        return output_path

    @staticmethod
    def generate_json_report(analysis_results: Dict[str, Any], output_path: str) -> str:
        """
        Generate JSON report from analysis results.

        Args:
            analysis_results (Dict): Dictionary containing analysis results.
            output_path (str): Path to save JSON report.

        Returns:
            str: Path to saved JSON file.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        report_data = {
            'generated_at': datetime.now().isoformat(),
            'analysis_results': analysis_results
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        return output_path

    @staticmethod
    def generate_html_report(analysis_results: Dict[str, Any], output_path: str,
                           document_title: str = "Document Analysis Report") -> str:
        """
        Generate HTML report from analysis results.

        Args:
            analysis_results (Dict): Dictionary containing analysis results.
            output_path (str): Path to save HTML report.
            document_title (str): Title for the report.

        Returns:
            str: Path to saved HTML file.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{document_title}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 900px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #1f4788;
                    text-align: center;
                    border-bottom: 2px solid #1f4788;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #1f4788;
                    margin-top: 20px;
                }}
                .metadata {{
                    color: #666;
                    font-size: 12px;
                    margin-bottom: 20px;
                }}
                .section {{
                    margin-bottom: 20px;
                }}
                .keywords {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                }}
                .keyword {{
                    background-color: #e8f0f7;
                    padding: 4px 12px;
                    border-radius: 4px;
                    font-size: 12px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 10px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #1f4788;
                    color: white;
                }}
                ul {{
                    line-height: 1.8;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{document_title}</h1>
                <div class="metadata">
                    Generated: {datetime.now().strftime("%B %d, %Y at %H:%M")}
                </div>
        """

        # Summary
        if 'summary' in analysis_results and analysis_results['summary']:
            html_content += f"""
                <div class="section">
                    <h2>Summary</h2>
                    <p>{analysis_results['summary']}</p>
                </div>
            """

        # Key Insights
        if 'key_insights' in analysis_results:
            insights_html = "".join([f"<li>{insight}</li>" for insight in analysis_results.get('key_insights', [])[:5]])
            html_content += f"""
                <div class="section">
                    <h2>Key Insights</h2>
                    <ul>{insights_html}</ul>
                </div>
            """

        # Keywords
        if 'keywords' in analysis_results and analysis_results['keywords']:
            keywords_html = "".join([f'<span class="keyword">{kw}</span>' for kw in analysis_results['keywords'][:10]])
            html_content += f"""
                <div class="section">
                    <h2>Keywords</h2>
                    <div class="keywords">{keywords_html}</div>
                </div>
            """

        # Statistics
        if 'statistics' in analysis_results:
            stats = analysis_results['statistics']
            html_content += f"""
                <div class="section">
                    <h2>Document Statistics</h2>
                    <table>
                        <tr><th>Metric</th><th>Value</th></tr>
                        <tr><td>Total Words</td><td>{stats.get('total_words', 'N/A')}</td></tr>
                        <tr><td>Total Sentences</td><td>{stats.get('total_sentences', 'N/A')}</td></tr>
                        <tr><td>Unique Words</td><td>{stats.get('unique_words', 'N/A')}</td></tr>
                        <tr><td>Average Word Length</td><td>{stats.get('average_word_length', 0):.2f}</td></tr>
                        <tr><td>Reading Time (minutes)</td><td>{stats.get('reading_time_minutes', 'N/A')}</td></tr>
                    </table>
                </div>
            """

        html_content += """
            </div>
        </body>
        </html>
        """

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return output_path

    @staticmethod
    def generate_all_reports(analysis_results: Dict[str, Any], output_dir: str,
                           document_title: str = "Document Analysis Report") -> Dict[str, str]:
        """
        Generate all report formats (PDF, HTML, Text, JSON).

        Args:
            analysis_results (Dict): Analysis results dictionary.
            output_dir (str): Directory to save reports.
            document_title (str): Title for reports.

        Returns:
            Dict: Paths to all generated reports.
        """
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"analysis_report_{timestamp}"

        reports = {}

        try:
            # PDF Report
            pdf_path = os.path.join(output_dir, f"{base_filename}.pdf")
            ReportGenerator.generate_pdf_report(analysis_results, pdf_path, document_title)
            reports['pdf'] = pdf_path
        except Exception as e:
            print(f"Error generating PDF report: {e}")

        try:
            # HTML Report
            html_path = os.path.join(output_dir, f"{base_filename}.html")
            ReportGenerator.generate_html_report(analysis_results, html_path, document_title)
            reports['html'] = html_path
        except Exception as e:
            print(f"Error generating HTML report: {e}")

        try:
            # Text Report
            txt_path = os.path.join(output_dir, f"{base_filename}.txt")
            ReportGenerator.generate_text_report(analysis_results, txt_path, document_title)
            reports['txt'] = txt_path
        except Exception as e:
            print(f"Error generating text report: {e}")

        try:
            # JSON Report
            json_path = os.path.join(output_dir, f"{base_filename}.json")
            ReportGenerator.generate_json_report(analysis_results, json_path)
            reports['json'] = json_path
        except Exception as e:
            print(f"Error generating JSON report: {e}")

        return reports
