from rest_framework.pagination import PageNumberPagination


class CoursePagination(PageNumberPagination):
    page_size = 10  # Количество элементов на странице
    page_size_query_param = 'page_size'
    max_page_size = 100


class LessonPagination(PageNumberPagination):
    page_size = 15  # Количество элементов на странице
    page_size_query_param = 'page_size'
    max_page_size = 50