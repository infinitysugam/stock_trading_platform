# from django.shortcuts import render
# from . models import News_article
# # Create your views here.

# def news_list(request):
#     #Fetch all news articles
#     articles = News_article.objects.all()

#     #pass articles to the template
#     return render(request, 'news_aggregator/news_list.html', {'articles': articles})

from django.shortcuts import render

def news_list(request):
    return render(request, 'news_list.html')  # Render your template for the news list
