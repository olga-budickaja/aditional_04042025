from django.http import HttpRequest


def pagination(request: HttpRequest, class_obj, qnt=int, obj=True):
    page = request.GET.get("page", 1)
    return (class_obj.objects.all()[int(page)*qnt-qnt:int(page)*qnt]
            if obj==True
            else class_obj.products.all()[int(page)*qnt-qnt:int(page)*qnt]
            )
