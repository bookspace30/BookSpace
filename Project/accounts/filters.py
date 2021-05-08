import django_filters
from django_filters import DateFilter, CharFilter

from .models import *


class OrderFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name="date_created", lookup_expr='gte')
	# end_date = DateFilter(field_name="date_created", lookup_expr='lte')
	# note = CharFilter(field_name='note', lookup_expr='icontains')

	class Meta:
		model = Order
		fields = '__all__'


class OrderItemFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name="date_created", lookup_expr='gte')
	# end_date = DateFilter(field_name="date_created", lookup_expr='lte')
	# note = CharFilter(field_name='note', lookup_expr='icontains')
	# check = OrderFilter(Order)

	class Meta:
		model = OrderItem
		fields = '__all__'


class ShopFilter(django_filters.FilterSet):
	# start_date = DateFilter(field_name="date_created", lookup_expr='gte')
	# end_date = DateFilter(field_name="date_created", lookup_expr='lte')
	name = CharFilter(field_name='name', lookup_expr='icontains')

	class Meta:
		model = Product
		fields = ['categories', 'isbn']
		# exclude = ['image', 'price', 'author', 'isbn', 'condition', 'description', 'date_created']


