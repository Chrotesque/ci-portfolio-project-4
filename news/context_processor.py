from .models import Category


def add_categories_to_context(request):
    categories = Category.objects.order_by('name')
    return {
        'categories': categories
    }
