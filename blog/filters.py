"""Custom Jinja filters"""

from blog import app

@app.template_filter()
def dateformat(date, format):
    """Format date/time using python method with provided string"""
    if not date:
        return None
    return date.strftime(format)