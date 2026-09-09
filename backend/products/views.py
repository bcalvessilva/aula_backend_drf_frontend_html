from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Product
from .permissions import IsGerenteGroup
from .serializers import ProductSerializer, CheckoutSerializer, CheckoutResponseSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Habilita suporte a upload de arquivos e formulários multipart
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        # Operações de escrita exigem permissão de Gerente
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsGerenteGroup()]
        return [IsAuthenticatedOrReadOnly()]
# Create your views here.
class CheckoutView(APIView):
    permision_classes = [IsAuthenticated]

    @extend_schema(
        request= CheckoutSerializer,
        responses={200: CheckoutResponseSerializer,400: OpenApiResponse(description="erro de validação do payload,produto inexistente,estoque insuficiente")},
        description='Recebe os itens selecionados do carrinho, valida as regras de estoque e calcula o valor total geral.'
    )
    def post(self,request):
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        items_data = serializer.validated_data['items']
        total_geral = 0.0
        produtos_atualizar = []

        for item in items_data:
            prod_id = item['product_id']
            qtd = item['quantity']

            try:
                produto = Product.objects.get(id=prod_id)
            except Product.DoesNotExist:
                return Response(
                    {"detail":f'Produto com ID {prod_id} não existe no catálogo'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if produto.stock<qtd:
                  return Response(
                    {"detail": f"Estoque insuficiente para o produto '{produto.name}'. Quantidade disponível: {produto.stock}."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            total_geral += float(produto.price) * qtd
            produto.stock -= qtd
            produtos_atualizar.append(produto)

        # Etapa de Persistência (Executa o salvamento apenas se todas as validações passarem)
        for produto in produtos_atualizar:
            produto.save()

        return Response({
            "mensagem": "Checkout finalizado com sucesso!",
            "usuario": request.user.username,
            "total_da_compra": round(total_geral, 2)
        }, status=status.HTTP_200_OK)


