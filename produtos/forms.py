from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto 
        fields = ['nome', 'descricao', 'preco', 'quantidade']

    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get("quantidade")
        if quantidade < 0:
            raise forms.ValidationError("Quantidade não pode ser negativa.")
        return quantidade

    def clean_preco(self):
        preco = self.cleaned_data.get("preco")
        if preco < 0:
            raise forms.ValidationError("Preço não pode ser negativo.")
        return preco