# data class with email content data

from dataclasses import dataclass
from datetime import datetime

from state_of_the_art.paper.arxiv_paper import ArxivPaper


@dataclass
class EmailData:
    # the dicts are in the format of {'interest': str, 'papers': list[ArxivPaper]}
    recommendations_with_papers: list[dict]
    user_email: str
    empty_interests: list[str]
    total_interests: int
    days_to_lookback: int
    papers_found_in_last_n_days: int

class EmailContentGenerator:

    def generate_html(self, email_data: EmailData) -> str:
        html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.4;
            color: #2c3e50;
            margin: 0;
            padding: 15px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
        }}
        .welcome-message {{
            text-align: left;
            margin-bottom: 15px;
            color: #34495e;
            font-size: 14px;
        }}
        .welcome-message p {{
            margin: 0 0 8px 0;
            font-size: 15px;
            color: #2c3e50;
        }}
        .welcome-message .summary {{
            color: #34495e;
            font-size: 13px;
            line-height: 1.5;
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin: 0 0 8px 0;
            font-size: 22px;
            font-weight: 600;
            letter-spacing: -0.5px;
        }}
        .date {{
            text-align: center;
            color: #7f8c8d;
            font-size: 13px;
            margin-bottom: 15px;
        }}
        .interest-section {{
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #ecf0f1;
        }}
        .interest-title {{
            color: #2980b9;
            font-size: 16px;
            margin-bottom: 10px;
            font-weight: bold;
        }}
        .paper-card {{
            background: #f8f9fa;
            padding: 8px 10px;
            margin: 6px 0;
            border-radius: 4px;
            border-left: 3px solid #3498db;
        }}
        .paper-title {{
            margin-bottom: 4px;
        }}
        .paper-title a {{
            color: #2c3e50;
            text-decoration: none;
            font-weight: bold;
            font-size: 14px;
        }}
        .paper-meta {{
            font-size: 12px;
            color: #7f8c8d;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .paper-date {{
            font-style: italic;
        }}
        .paper-button {{
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 4px 8px;
            border-radius: 3px;
            text-decoration: none;
            font-size: 12px;
        }}
        .empty-interests {{
            background: #f8f9fa;
            padding: 12px;
            margin-top: 15px;
            border-radius: 6px;
            border: 1px solid #ecf0f1;
        }}
        .empty-interests h2 {{
            font-size: 16px;
            margin-bottom: 8px;
            color: #2c3e50;
        }}
        .empty-interests-list {{
            list-style-type: disc;
            padding-left: 20px;
            margin: 0;
        }}
        .empty-interest-item {{
            color: #7f8c8d;
            font-size: 13px;
            margin-bottom: 3px;
        }}
    </style>
    </head>
    <body>
    <div class="container">
        <h1>Your Research Update</h1>
        <div class="date">{datetime.now().strftime('%B %d, %Y')}</div>
        <div class="welcome-message">
            <p>Hi {email_data.user_email.split('@')[0]},</p>
            <div class="summary">
                Here's your latest research update. We've analyzed papers from the past {email_data.days_to_lookback} days and found {email_data.papers_found_in_last_n_days} relevant papers across your {email_data.total_interests} research interests.
            </div>
        </div>
    """
        for rec in email_data.recommendations_with_papers:
            html += f"""
        <div class="interest-section">
            <div class="interest-title">{rec['interest']}</div>
    """
            for paper in rec['papers']:
                html += f"""
            <div class="paper-card">
                <div class="paper-title">
                    <a href="{paper.abstract_url}" target="_blank">{paper.title}</a>
                </div>
                <div class="paper-meta">
                    <span class="paper-date">{paper.published.strftime('%B %d, %Y')}</span>
                    <a href="http://localhost:8509/paper_details_page?paper_url={paper.abstract_url}" class="paper-button">Open in App</a>
                </div>
            </div>
    """
            html += """
        </div>
    """
        
        if email_data.empty_interests:
            html += f"""
        <div class="empty-interests">
            <h2>Interests Without Papers</h2>
            <ul class="empty-interests-list">
    """
            for interest in email_data.empty_interests:
                html += f"""
                <li class="empty-interest-item">{interest}</li>
    """
            html += """
            </ul>
        </div>
    """
        
        html += """
    </div>
    </body>
    </html>
    """
        return html
