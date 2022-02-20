# https://django-oidc-provider.readthedocs.io/en/latest/sections/scopesclaims.html#scopes-and-claims
def userinfo(claims, user):
    # Populate claims dict.
    claims['name'] = '{0} {1}'.format(user.first_name, user.last_name)
    claims['given_name'] = user.first_name
    claims['family_name'] = user.last_name
    claims['preferred_username'] = user.username

    claims['email'] = user.email

    return claims
