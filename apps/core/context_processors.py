import os

def google_tag_manager(request):
    return {'GTM_ID': os.getenv("GTM_ID", "12345")}
