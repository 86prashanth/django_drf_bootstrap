from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from drfapp.models import Review,Movie,Streamplatform,Watchlist
from rest_framework.response import Response
from drfapp.api.serializers import (ReviewSerializer,MovieModelSerializer,Streamplatformserializer,Watchlistserializer)
from rest_framework.decorators import api_view
from rest_framework import status,mixins,generics
from rest_framework import viewsets
from drfapp.api.pagination import WatchListPagenation
from drfapp.api.permissions import AdminOrReadOnly,ReviewUserOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from user_app.api.throttling import ReviewCreateThrottle,ReviewlistThrottle
# modelviewsets
# class StreamplatformMvs(viewsets.ModelViewSet):
class StreamplatformMvs(viewsets.ReadOnlyModelViewSet):
    serializer_class=Streamplatformserializer
    queryset=Streamplatform.objects.all()


# router
class Streamplatformv(viewsets.ViewSet):
        def list(self,request):
            queryset=Streamplatform.objects.all()
            serializer=Streamplatformserializer(queryset,many=True)
            return Response(serializer.data)
        
        def retrive(self,request,pk=None):
            queryset=Streamplatform.objects.all()
            user=get_object_or_404(queryset,pk=pk)
            serializer=Streamplatformserializer(user)
            return(serializer.data)
        
        def create(self,request):
            serializer=Streamplatformserializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
#Concrete api views classes
class UserReview(generics.ListAPIView):
    # queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    # permission_classes=[IsAuthenticated]
    # throttle_classes=[ReviewListThrottle,AnnoRateThrottle]
    def get_queryset(self):
        username=self.kwargs['username']
        return Review.objects.filter(review_user__username=username)
class ReviewCreate(generics.CreateAPIView):
    serializer_class=ReviewSerializer
    permisson_classes=[IsAuthenticated]
    throttle_classes=[ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self,serializer):
        pk=self.kwargs.get('pk')
        watchlist=Watchlist.objects.get(pk=pk)
        review_user=self.request.user
        review_queryset=Review.objects.filter(watchlist=watchlist,review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie")
        if watchlist.number_rating==0:
            watchlist.avg_rating=serializer.validated_data['rating']
        else:
            watchlist.avg_rating=(watchlist.avg_rating + serializer.validated_data['rating'])/2
        watchlist.number_rating=watchlist.number_rating + 1
        watchlist.save()
        serializer.save(watchlist=watchlist,review_user=review_user)


        
class ReviewList(generics.ListAPIView):
    # queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    throttle_classes=[ReviewlistThrottle]
    filter_backends=[DjangoFilterBackend]
    filterset_fields=['review_user__username','active']
    pagination_class=WatchListPagenation
    # permission_classes=[IsAuthenticated]
    # permissions
    permission_class=[AdminOrReadOnly]
    # permission_classes=[IsAuthenticatedOrReadOnly]
    # overwrite queryset
    def get_queryset(self,pk):
        pk=self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    

class ReviewDetailg(generics.RetrieveUpdateDestroyAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[AdminOrReadOnly]
    throttle_classes='review-detail'
# Genericapi and mixins
class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
     
class ReviewLists(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 generics.GenericAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
# class Based API view
class MovieListAv(APIView):
    def get(self,request):
        movie=Movie.objects.all()
        # serializer=MovieSerializer(movie,many=True)
        serializer=MovieModelSerializer(movie,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        # serializer=MovieSerializer(data=request.data)
        serializer=MovieModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

#movie detailview
class MovieDetailAV(APIView):
    def get(self,request,pk):
        try:
            movie=Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'error':'Movie Not Found'},status=status.HTTP_404_NOT_FOUND)
        # serializer=MovieSerializer(movie)
        serializer=MovieModelSerializer(movie)
        return Response(serializer.data)
    
    def put(self,request,pk):
        movie=Movie.objects.get(pk=pk)
        # serializer=MovieSerializer(movie,data=request.data)
        serializer=MovieModelSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        movie=Movie.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# function based view
@api_view(['GET','POST'])
def movie_list(request):
    if request.method=='GET':
        movies=Movie.objects.all()
        # serializer=MovieSerializer(movies,many=True)
        serializer=MovieModelSerializer(movies,many=True)
        return Response(serializer.data)
    
    if request.method=='POST':
        # serializer=MovieSerializer(data=request.data)
        serializer=MovieModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
        
# function based view      
@api_view(['GET','PUT','DELETE'])
def movie_details(request,pk):
    if request.method=='GET':
        try:
            movies=Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'Error':"Movie does not found"},status=status.HTTP_404_NOT_FOUND)
        # serializer=MovieSerializer(movies)
        serializer=MovieModelSerializer(movies)
        return Response(serializer.data)
    
    if request.method=='PUT':
        movie=Movie.objects.get(pk=pk)
        # serializer=MovieSerializer(movie,data=request.data)
        serializer=MovieModelSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    if request.method=='DELETE':
        movie=Movie.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class StreamplatformAv(APIView):
    def get(self,request):
        platform=Streamplatform.objects.all()
        serializer=Streamplatformserializer(platform,many=True,context={'request':request})
        return Response(serializer.data)
    
    def post(self,request):
        serializer=Streamplatformserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamplatformdetailAv(APIView):
    def get(self,request,pk):
        try:
            platform=Streamplatform.objects.get(pk=pk)
        except Streamplatform.DoesNotExist:
            return Response({'error':'Not Found'},status=status.HTTP_404_NOT_FOUND)
        serializer=Streamplatformserializer(platform,context={'request':request})
        return Response(serializer.data)
    
    def put(self,request,pk):
        platform=Streamplatform.objects.get(pk=pk)
        serializer=Streamplatformserializer(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_fBAD_REQUEST)
        
    def delete(self,request,pk):
        platform=Streamplatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class Watchlistav(APIView):
    def get(self,request):
        movies=Watchlist.objects.all()
        serializer=Watchlistserializer(movies,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=Watchlistserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)       