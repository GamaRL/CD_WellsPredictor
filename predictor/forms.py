from django import forms


class WellPredictionForm(forms.Form):
    wellname = forms.CharField(
        label='Well Name',
        max_length=20,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-sm', 'placeholder': 'e.g., Well A1'})
    )
    spuddate = forms.DateField(
        label='Spud Date',
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    completiondate = forms.DateField(
        label='Completion Date',
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control form-control-sm'})
    )
    function = forms.ChoiceField(
        label='Function',
        choices=[
            ('Domestic', 'Domestic'),
            ('Exploration', 'Exploration'),
            ('Injection', 'Injection'),
            ('Irrigation/Agriculture', 'Irrigation/Agriculture'),
            ('Mining/Leaching/Milling', 'Mining/Leaching/Milling'),
            ('Observation', 'Observation'),
            ('Production', 'Production'),
            ('Public Submunicipal', 'Public Submunicipal'),
            ('Test', 'Test'),
            ('Thermal Gradient', 'Thermal Gradient'),
            ('Unknown', 'Unknown'),
        ],
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
    latitude = forms.FloatField(
        label='Latitude',
        widget=forms.NumberInput(
            attrs={'class': 'form-control form-control-sm', 'placeholder': 'e.g., 32.624', 'step': 'any'})
    )
    longitude = forms.FloatField(
        label='Longitude',
        widget=forms.NumberInput(
            attrs={'class': 'form-control form-control-sm', 'placeholder': 'e.g., -115.403', 'step': 'any'})
    )
    elevationgl_m = forms.FloatField(
        label='Elevation Ground Level (m)',
        min_value=0,
        widget=forms.NumberInput(
            attrs={'class': 'form-control form-control-sm', 'placeholder': 'e.g., 3000'})
    )
    drillertotaldepth_m = forms.FloatField(
        label='Driller Total Depth (m)',
        min_value=0,
        widget=forms.NumberInput(
            attrs={'class': 'form-control form-control-sm', 'placeholder': 'e.g., 3000'})
    )
    maxmeasuredtemp_c = forms.FloatField(
        label='Max Measured Temperature (°C)',
        widget=forms.NumberInput(
            attrs={'class': 'form-control form-control-sm', 'placeholder': 'e.g., 127', 'step': 'any'})
    )
    bottommeasuredtemp_c = forms.FloatField(
        label='Bottom Measured Temperature (°C)',
        widget=forms.NumberInput(
            attrs={'class': 'form-control form-control-sm', 'placeholder': 'e.g., 120', 'step': 'any'})
    )
