from django.contrib import admin


from .models import (
    Account,
    Company,
    BlacklistedToken,
)


admin.site.register(
    [
        Account,
        Company,
        BlacklistedToken,
    
    ]
)