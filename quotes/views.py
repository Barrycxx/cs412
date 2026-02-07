from django.shortcuts import render
from django.utils import timezone
import random

# Person
PERSON_NAME = "Joker Xue (Xue Zhiqian)"

# Global lists (course requirement: 2 Python lists in global scope)
quotes = [
    "I am not someone born talented. I just never gave up.",
    "If persistence is hard, then persist a little longer.",
    "Music is the only thing I can trust completely.",
]

images = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/%E8%96%9B%E4%B9%8B%E8%B0%A6_%E5%93%94%E5%93%A9%E5%93%94%E5%93%A9%E6%B0%B8%E8%BF%9C22%E6%AF%95%E4%B8%9A%E6%AD%8C%E4%BC%9A_20250602_%28cropped%29.jpg/960px-%E8%96%9B%E4%B9%8B%E8%B0%A6_%E5%93%94%E5%93%A9%E5%93%94%E5%93%A9%E6%B0%B8%E8%BF%9C22%E6%AF%95%E4%B8%9A%E6%AD%8C%E4%BC%9A_20250602_%28cropped%29.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/%E6%99%82%E9%96%93%E9%81%8E%E5%BE%97%E7%9C%9F%E5%BF%AB%EF%BC%8C%E8%B7%9D%E9%9B%A2%E4%B8%8A%E4%B8%80%E6%AC%A1%E8%A6%8B%E4%BD%A0%E9%83%BD%E4%B8%80%E5%B9%B4%E4%BA%86..._%28%E8%96%9B%E4%B9%8B%E8%B0%A6%29_%283%29.jpg/960px-%E6%99%82%E9%96%93%E9%81%8E%E5%BE%97%E7%9C%9F%E5%BF%AB%EF%BC%8C%E8%B7%9D%E9%9B%A2%E4%B8%8A%E4%B8%80%E6%AC%A1%E8%A6%8B%E4%BD%A0%E9%83%BD%E4%B8%80%E5%B9%B4%E4%BA%86..._%28%E8%96%9B%E4%B9%8B%E8%B0%A6%29_%283%29.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/%E8%96%9B%E4%B9%8B%E8%B0%A6_%E8%B4%B5%E9%98%B3%E7%88%B1%E6%9C%AA%E6%9D%A5%E5%9F%8E%E5%B8%82%E9%9F%B3%E4%B9%90%E8%8A%82_20231003_%28cropped%29.jpg/960px-%E8%96%9B%E4%B9%8B%E8%B0%A6_%E8%B4%B5%E9%98%B3%E7%88%B1%E6%9C%AA%E6%9D%A5%E5%9F%8E%E5%B8%82%E9%9F%B3%E4%B9%90%E8%8A%82_20231003_%28cropped%29.jpg",
]


def quote(request):
    q = random.choice(quotes)
    img = random.choice(images)

    context = {
        "person_name": PERSON_NAME,
        "quote": q,
        "image": img,
        "generated_at": timezone.now(),
        "creator": "Xinxu Chen (chenxin@bu.edu)",
    }

    return render(request, "quotes/quote.html", context)


def show_all(request):
    context = {
        "person_name": PERSON_NAME,
        "quotes": quotes,
        "images": images,
        "generated_at": timezone.now(),
        "creator": "Xinxu Chen (chenxin@bu.edu)",
    }

    return render(request, "quotes/show_all.html", context)


def about(request):
    context = {
        "person_name": PERSON_NAME,
        "bio": (
            "Joker Xue is a Chinese pop singer, songwriter, and music producer. "
            "He became widely known for his emotional ballads and humorous personality on television shows. "
            "His music style focuses on storytelling and deep lyrical expression."
        ),
        "creator": "Xinxu Chen (chenxin@bu.edu)",
        "generated_at": timezone.now(),
    }

    return render(request, "quotes/about.html", context)
