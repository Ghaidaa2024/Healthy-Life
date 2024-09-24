from rest_framework import serializers
from api.models import Food

class FoodSerializer(serializers.ModelSerializer):
    amount_type = serializers.SerializerMethodField()

    class Meta:
        model = Food
        fields = ('name', 'amount', 'amount_type', 'calories', 'protein', 'fat', 'carbohydrate', 'calcium', 'cholesterol',
                  'iron', 'sodium', 'vitamin_C', 'vitamin_A')

    def get_amount_type(self, obj):
        # Convert the amount_type integer to its corresponding label
        return dict(Food.TypeAmount.choices).get(obj.amout_type)
