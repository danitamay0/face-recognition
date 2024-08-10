
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from clients.models import Client

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """     def validate(self, attrs):
        data = super().validate(attrs)
        access_token = self.get_token(self.user)
        client = Client.objects.filter(user=access_token['user_id']).first()
        # Add custom claims
        access_token['custom_field'] = str(client.id)
        
        data['access'] = str(access_token) 
        return data
     """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        client = Client.objects.filter(user=user.id).first()
        token['client'] = str(client.id)
        # ...

        return token