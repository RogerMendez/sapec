from django import forms

class EmailForm(forms.Form):
	email = forms.EmailField(label='Correo Electronico')

class CiForm(forms.Form):
	ci = forms.IntegerField(label='Cedula de Identidad')