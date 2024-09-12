import sys
sys.path.insert(0, '.')  # Add the current directory to the path

from show_urls import show_urls
from django.urls import get_resolver

urls = get_resolver().url_patterns
show_urls(urls)
