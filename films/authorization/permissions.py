from rest_framework.permissions import IsAuthenticated


class CustomIsAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        excluded_endpoints = ['registration', 'token_obtain_pair', 'token_refresh']  
        if request.resolver_match.url_name in excluded_endpoints:
            return True  
        
        return super().has_permission(request, view)