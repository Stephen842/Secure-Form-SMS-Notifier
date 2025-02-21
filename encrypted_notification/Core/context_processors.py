def token_processor(request):
    return{'token': request.GET.get('token', '')}