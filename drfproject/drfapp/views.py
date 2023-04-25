# from django.shortcuts import render
# from django.http import HttpResponse
# from drfapp.models import Movie
# from django.http import JsonResponse
# # Create your views here.
# # movie list
# def movie_list(request):
#     movies=Movie.objects.all()
#     data={'movies':list(movies.values())}
#     print(movies.values())
#     return JsonResponse(data)

# #movie details list for individual
# def movie_details(request,pk):
#     movie=Movie.objects.get(pk=pk)
#     data={
#         'name':movie.name,
#         'description':movie.description,
#         'active':movie.active,
#     }
#     return JsonResponse(data)