from django import forms
from django.contrib.auth import get_user_model



from comercial.models import *

User = get_user_model()

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = ['user__first_name', 'user__last_name', 'user__email', 'address']
#         widgets = {
#             'user__first_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'user__last_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'user__email': forms.EmailInput(attrs={'class': 'form-control'}),
#         }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'number', 'complement', 'city', 'state', 'zip_code', 'country']
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'complement': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
        }

class OrderUpdateForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('confirmed', 'Confirmado'),
        ('processing', 'Processando'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregue'),
        ('cancelled', 'Cancelado'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Order
        fields = ['customer', 'status', 'notes']
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações sobre o pedido...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.select_related('user').all()
        self.fields['customer'].empty_label = "Selecione um cliente..."

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

# class DeliveryForm(forms.ModelForm):
#     class Meta:
#         model = Delivery
#         fields = ['order', 'delivery_date', 'employee', 'vehicle']
#         widgets = {
#             'order': forms.Select(attrs={'class': 'form-control'}),
#             'delivery_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
#             'employee': forms.Select(attrs={'class': 'form-control'}),
#             'vehicle': forms.Select(attrs={'class': 'form-control'}),
#         }

# class VehicleForm(forms.ModelForm):
#     class Meta:
#         model = Vehicle
#         fields = ['license_plate', 'model', 'year', 'value']
#         widgets = {
#             'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
#             'model': forms.TextInput(attrs={'class': 'form-control'}),
#             'year': forms.NumberInput(attrs={'class': 'form-control'}),
#             'value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
#         }

class CustomerCreateForm(forms.ModelForm):
    # Campos do usuário
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome do cliente'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sobrenome do cliente'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@exemplo.com'
        })
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome de usuário único'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(11) 99999-9999'
        })
    )
    
    # Campos do endereço
    street = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome da rua'
        })
    )
    number = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número'
        })
    )
    complement = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apartamento, bloco, etc.'
        })
    )
    city = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cidade'
        })
    )
    state = forms.CharField(
        max_length=2,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'SP'
        })
    )
    zip_code = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '00000-000'
        })
    )
    country = forms.CharField(
        max_length=100,
        initial='Brasil',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Customer
        fields = [] 

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email já está em uso.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nome de usuário já está em uso.')
        return username

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        # Remove caracteres não numéricos
        zip_code = ''.join(filter(str.isdigit, zip_code))
        if len(zip_code) != 8:
            raise forms.ValidationError('CEP deve ter 8 dígitos.')
        # Formata o CEP
        return f"{zip_code[:5]}-{zip_code[5:]}"

    def save(self, commit=True):
        # Criar o usuário
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        
        # Criar o endereço
        address = Address.objects.create(
            street=self.cleaned_data['street'],
            number=self.cleaned_data['number'],
            complement=self.cleaned_data.get('complement', ''),
            city=self.cleaned_data['city'],
            state=self.cleaned_data['state'],
            zip_code=self.cleaned_data['zip_code'],
            country=self.cleaned_data['country']
        )
        
        # Criar o cliente
        customer = Customer.objects.create(
            user=user,
            address=address
        )
        
        return customer


class CustomerUpdateForm(forms.ModelForm):
    # Campos do usuário
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome do cliente'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sobrenome do cliente'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@exemplo.com'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(11) 99999-9999'
        })
    )
    
    # Campos do endereço
    street = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome da rua'
        })
    )
    number = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número'
        })
    )
    complement = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apartamento, bloco, etc.'
        })
    )
    city = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cidade'
        })
    )
    state = forms.CharField(
        max_length=2,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'SP'
        })
    )
    zip_code = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '00000-000'
        })
    )
    country = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Customer
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Preencher campos com dados existentes
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['street'].initial = self.instance.address.street
            self.fields['number'].initial = self.instance.address.number
            self.fields['complement'].initial = self.instance.address.complement
            self.fields['city'].initial = self.instance.address.city
            self.fields['state'].initial = self.instance.address.state
            self.fields['zip_code'].initial = self.instance.address.zip_code
            self.fields['country'].initial = self.instance.address.country

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance and self.instance.pk:
            # Permitir o mesmo email se for o mesmo usuário
            if User.objects.filter(email=email).exclude(pk=self.instance.user.pk).exists():
                raise forms.ValidationError('Este email já está em uso.')
        else:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('Este email já está em uso.')
        return email

    def save(self, commit=True):
        customer = self.instance
        
        # Atualizar usuário
        customer.user.first_name = self.cleaned_data['first_name']
        customer.user.last_name = self.cleaned_data['last_name']
        customer.user.email = self.cleaned_data['email']
        if commit:
            customer.user.save()
        
        # Atualizar endereço
        customer.address.street = self.cleaned_data['street']
        customer.address.number = self.cleaned_data['number']
        customer.address.complement = self.cleaned_data.get('complement', '')
        customer.address.city = self.cleaned_data['city']
        customer.address.state = self.cleaned_data['state']
        customer.address.zip_code = self.cleaned_data['zip_code']
        customer.address.country = self.cleaned_data['country']
        if commit:
            customer.address.save()
        
        return customer


class EmployeeCreateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome do funcionario'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sobrenome do Funcionário'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@exemplo.com'
        })
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome de usuário único'
        })
    )
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        input_formats=['%Y-%m-%d']
    )
    departament = forms.ModelChoiceField(  # (Note: same spelling as model)
        queryset=Department.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    class Meta:
        model = Employee
        fields = ['birthdate', 'departament']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email já está em uso.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nome de usuário já está em uso.')
        return username

    def save(self, commit=True):
        # Create user
        user = CustomUser.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        
        # Create employee
        employee = Employee.objects.create(
            user=user,
            birthdate=self.cleaned_data['birthdate'],
            departament=self.cleaned_data['departament']
        )
        return employee