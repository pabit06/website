from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'home/index.html')


def coming_soon(request):
    return render(request, 'coming_soon.html')


def sitemap_xml(request):
    """Serve sitemap.xml for SEO."""
    base = request.build_absolute_uri('/').rstrip('/')
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{base}/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>'''
    return HttpResponse(xml, content_type='application/xml')
