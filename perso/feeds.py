from django.urls import reverse_lazy

from dmdb.feeds import BlogEntriesFeed

class Feed(BlogEntriesFeed):
    title = "Nim's web.log"
    link = reverse_lazy('feed')
    description = "Latest blog entries on saurel.me"
