"""
Response formatting utilities
"""
def format_response_for_html(response_text: str) -> str:
    """Format response text for HTML display"""
    if not response_text:
        return ""
    
    # Convert markdown-style headers
    formatted = response_text
    formatted = formatted.replace('## ', '<h3>').replace('\n\n', '</h3>\n')
    
    # Convert bold text
    formatted = formatted.replace('**', '<strong>').replace('**', '</strong>')
    
    # Convert newlines to <br>
    formatted = formatted.replace('\n', '<br>')
    
    return formatted

def format_response_for_json(response_text: str, intent: str = '') -> dict:
    """Format response for JSON API"""
    return {
        'text': response_text,
        'html': format_response_for_html(response_text),
        'intent': intent,
        'timestamp': ''
    }
