import requests
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authentication import get_authorization_header


def oauth_check(func):
    def decorator(request, **kwargs):
        keyword = "Bearer"
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != keyword.lower().encode():
            return JsonResponse(
                data={"error": "Header not valid."}, status=status.HTTP_401_UNAUTHORIZED
            )

        if len(auth) == 1:
            return JsonResponse(
                data={"error": "Invalid token header. No credentials provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        elif len(auth) > 2:
            return JsonResponse(
                data={
                    "error": "Invalid token header. Token string should not contain spaces."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        check = requests.get(
            url="http://oauth.infralabs.cs.ui.ac.id/oauth/resource",
            headers={"Authorization": f"Bearer {auth[1].decode()}"},
        )

        if check.status_code == status.HTTP_401_UNAUTHORIZED:
            return JsonResponse(
                data={"error": "Token expired."}, status=status.HTTP_401_UNAUTHORIZED
            )
        elif check.status_code == status.HTTP_200_OK:
            return func(request, **kwargs)

    return decorator
