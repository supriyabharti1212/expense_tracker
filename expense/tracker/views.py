from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Handle GET request to retrieve transactions and their aggregates."""
        transactions = Transaction.objects.filter(created_by=request.user)
        transactions_data = TransactionSerializer(transactions, many=True).data

        balance = Transaction.objects.filter(created_by=request.user).aggregate(total_balance=Sum('amount'))['total_balance'] or 0
        income = Transaction.objects.filter(created_by=request.user, amount__gte=0).aggregate(income=Sum('amount'))['income'] or 0
        expense = Transaction.objects.filter(created_by=request.user, amount__lte=0).aggregate(expense=Sum('amount'))['expense'] or 0

        context = {
            'status': True,
            'message': "Transaction list with balance, income, and expense",
            'data': {
                'transactions': transactions_data,
                'balance': balance,
                'income': income,
                'expense': expense
            }
        }

        return Response(context, status=status.HTTP_200_OK)

    def post(self, request):
        """Handle POST request to create a new transaction."""
        description = request.data.get('description')
        amount = request.data.get('amount')

        # Validate description
        if not description:
            return Response({"status": False, "message": "Description cannot be blank"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate amount
        try:
            amount = float(amount)
        except ValueError:
            return Response({"status": False, "message": "Amount should be a number"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the transaction
        Transaction.objects.create(
            description=description,
            amount=amount,
            created_by=request.user
        )

        return Response({"status": True, "message": "Transaction created successfully"}, status=status.HTTP_201_CREATED)
