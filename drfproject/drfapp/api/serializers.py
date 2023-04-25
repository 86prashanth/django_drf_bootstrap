from rest_framework import serializers
from drfapp.models import *




# model serializer
class MovieModelSerializer(serializers.ModelSerializer):
    len_name=serializers.SerializerMethodField()
    
    
    class Meta:
        model=Movie
        fields="__all__"
        # fields=['id','name','description','active']
        # exclude=['active']
    
    def get_len_name(self,object):
        return len(object.name)

# validation
def name_length(value):
    if len(value)<2:
        raise serializers.ValidationError("Name should be greater than 2")

class MovieSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField(validators=[name_length])
    description=serializers.CharField()
    active=serializers.BooleanField()
    
    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
    
    def update(self,instance,validated_data):
        instance.name=validated_data.get('name',instance.name)
        instance.description=validated_data.get('description',instance.description)
        instance.active=validated_data.get('active',instance.active)
        instance.save()
        return instance
    
    # validate data
    def validate(self,data):
        if data['name']==data['description']:
            raise serializers.ValidationError("Title and description should be different")
        else:
            return data
    
    # def validate_name(self,value):
    #     if len(value) <2:
    #         raise serializers.ValidationError("name should be greater than 2")
    #     else:
    #         return value
        
class ReviewSerializer(serializers.ModelSerializer):
    review_user=serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model=Review
        # fields="__all__"
        exclude=('watchlist',)


class Watchlistserializer(serializers.ModelSerializer):
    reviews=ReviewSerializer(many=True,read_only=True)
    class Meta:
        model=Watchlist
        fields="__all__" 


# nested serializer        
class Streamplatformserializer(serializers.ModelSerializer):
# Hyperlinked modelserialized
# class Streamplatformserializer(serializers.HyperlinkedModelSerializer):
    watchlist=Watchlistserializer(many=True,read_only=True)
    # serializer Relations
    # # watchlist=serializers.StringRelatedField(many=True)
    # # watchlist=serializers.PrimaryKeyRelatedField(many=True,read_only=True)    
    # watchlist=serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name=
    #                                               'movie_detail')
    
    class Meta:
        model=Streamplatform   
        fields="__all__"    
