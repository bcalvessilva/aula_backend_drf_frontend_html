import os
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    promo_price = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 
            'name', 
            'description', 
            'price', 
            'promo_price', 
            'stock', 
            'category', 
            'image', 
            'is_available'
        ]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("O preço do produto deve ser maior que R$ 0,00.")
        return value

 
    def validate_image(self, value):
        if value is None:
            return value

        max_size = 2 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("O tamanho da imagem não pode ultrapassar 2MB.")

        extension = os.path.splitext(value.name)[1].lower()
        valid_extensions = ['.jpg', '.jpeg', '.png']
        if extension not in valid_extensions:
            raise serializers.ValidationError(f"Extensão inválida({extension}). Use .jpg .jpeg ou .png.")

        return value
    
    def get_promo_price(self, obj):
        return round(float(obj.price) * 0.90, 2)

    def get_is_available(self, obj) -> bool:
        return obj.stock > 0
class CheckoutItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(help_text="ID númerico de produto no catálogo")
    quantity = serializers.IntegerField(min_value=1, help_text="Quantidade que deseja adquirir")

class CheckoutSerializer(serializers.Serializer):
    items = CheckoutItemSerializer(many=True, help_text="Lista de intens selecionados para a compra ")
from rest_framework import serializers

class CheckoutResponseSerializer(serializers.Serializer):
    mensagem = serializers.CharField(
        default="Checkout finalizado com sucesso!",
        help_text="Mensagem de confirmação da transação"
    )
    usuario = serializers.CharField(
        help_text="Nome do usuário autenticado que realizou a compra"
    )
    total_da_compra = serializers.FloatField(
        help_text="Valor total final do checkout formatado com duas casas decimais"
    )