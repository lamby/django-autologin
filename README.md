# django-autologin

## Installation

* Add `'django_autologin.middleware.AutomaticLoginMiddleware'` to `MIDDLEWARE` in your `settings.py`.

* Add `'django_autologin.templatetags.django_autologin'` to the `'builtins'` key in your `TEMPLATES` definition (optional).


## Usage
To generate an automatic login token first import

`from django_autologin.templatetags.django_autologin import automatic_login_token`

then pass a user object that you would like to authenticate to `automatic_login_token`

`auto_login = automatic_login_token(user)`

This will result in a parameter string like `mtkn=1:1isO4l:c1lfGUQsB7YfxSWtyKLD5eBHamF` saved in your auto_login variable.

In order to automatically authenticate the user, simply add this string as a get parameter to any request. For example:

`https://example.com/my-view?mtkn=1:1isO4l:c1lfGUQsB7YfxSWtyKLD5eBHamF`