from rest_framework import serializers
from .models import ProductQuestion, ProductAnswer


class ProductAnswerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ProductAnswer
        fields = ['id', 'question', 'user', 'answer', 'is_official', 'helpful_count', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductQuestionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    answers = ProductAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = ProductQuestion
        fields = ['id', 'product', 'user', 'question', 'is_answered', 'answers', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductQuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductQuestion
        fields = ['product', 'question']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ProductAnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAnswer
        fields = ['question', 'answer']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        answer = super().create(validated_data)
        question = answer.question
        question.is_answered = True
        question.save(update_fields=['is_answered'])
        return answer
