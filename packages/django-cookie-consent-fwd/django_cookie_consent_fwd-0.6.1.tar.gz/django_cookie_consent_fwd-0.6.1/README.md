This package is a fork of [django-cookie-consent](https://github.com/jazzband/django-cookie-consent) with additional features and improvements.


**Original Package documentation:**

Django cookie consent
=====================

Manage cookie information and let visitors give or reject consent for them.

[![Jazzband][badge:jazzband]][jazzband]

![License](https://img.shields.io/pypi/l/django-cookie-consent)
[![Build status][badge:GithubActions:CI]][GithubActions:CI]
[![Code Quality][badge:GithubActions:CQ]][GithubActions:CQ]
[![Code style: black][badge:black]][black]
[![Test coverage][badge:codecov]][codecov]
[![Documentation][badge:docs]][docs]

![Supported python versions](https://img.shields.io/pypi/pyversions/django-cookie-consent)
![Supported Django versions](https://img.shields.io/pypi/djversions/django-cookie-consent)
[![PyPI version][badge:pypi]][pypi]

**Features**

* cookies and cookie groups are stored in models for easy management
  through Django admin interface
* support for both opt-in and opt-out cookie consent schemes
* removing declined cookies (or non accepted when opt-in scheme is used)
* logging user actions when they accept and decline various cookies
* easy adding new cookies and seamlessly re-asking for consent for new cookies

Documentation
-------------

The documentation is hosted on [readthedocs][docs] and contains all instructions
to get started.

Alternatively, if the documentation is not available, you can consult or build the docs
from the `docs` directory in this repository.

[jazzband]: https://jazzband.co/
[badge:jazzband]: https://jazzband.co/static/img/badge.svg
[GithubActions:CI]: https://github.com/jazzband/django-cookie-consent/actions?query=workflow%3A%22Run+CI%22
[badge:GithubActions:CI]: https://github.com/jazzband/django-cookie-consent/workflows/Run%20CI/badge.svg
[GithubActions:CQ]: https://github.com/jazzband/django-cookie-consent/actions?query=workflow%3A%22Code+quality+checks%22
[badge:GithubActions:CQ]: https://github.com/jazzband/django-cookie-consent/workflows/Code%20quality%20checks/badge.svg
[black]: https://github.com/psf/black
[badge:black]: https://img.shields.io/badge/code%20style-black-000000.svg
[codecov]: https://codecov.io/gh/jazzband/django-cookie-consent
[badge:codecov]: https://codecov.io/gh/jazzband/django-cookie-consent/branch/master/graph/badge.svg
[docs]: https://django-cookie-consent.readthedocs.io/en/latest/?badge=latest
[badge:docs]: https://readthedocs.org/projects/django-cookie-consent/badge/?version=latest
[pypi]: https://pypi.org/project/django-cookie-consent/
[badge:pypi]: https://img.shields.io/pypi/v/django-cookie-consent.svg



**Documentation for django-cookie-consent-fwd forked package:**
---------------------------------------------------------------

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Adapting for specific use cases](#adapting-for-specific-use-cases)
- [Troubleshooting](#troubleshooting)

## Installation

1. Install the [django-cookie-consent-fwd](https://test.pypi.org/project/django-cookie-consent-fwd/) package in your virtual environment:

    ```bash
    pip install -i https://test.pypi.org/simple/ django-cookie-consent-fwd
    ```

2. Add the following to your requirements.txt:
    ```python
    django-cookie-consent-fwd
    ```

3. Add `cookie_consent` app to your `INSTALLED_APPS` in settings:

    ```python
    "cookie_consent"
    ```

4. Add `django.template.context_processors.request` to `TEMPLATE_CONTEXT_PROCESSORS` if not already present, and add `cookie_consent.middleware.CleanCookiesMiddleware` to MIDDLEWARE:

    ```python
    TEMPLATES = [
        {
            'OPTIONS': {
                'context_processors':
                (
                    'django.template.context_processors.request',
                )
            }
        },
    ]

    MIDDLEWARE = [
        ...
        "cookie_consent.middleware.CleanCookiesMiddleware",
    ]
    ```

5. Add the following configuration lines to your Django `settings.py` file:

    ```python
    COOKIE_CONSENT_SECURE = True
    COOKIE_CONSENT_SAMESITE = 'Strict'
    # Optionally show all cookie names under cookie group description:
    SHOW_COOKIE_NAMES_IN_MODAL = True  # Default: False
    ```

6. Include `django-cookie-consent` URLs in your `urls.py`:

    ```python
    from django.urls import path

    urlpatterns = [
        ...,
        path("cookies/", include("cookie_consent.urls")),
        ...,
    ]
    ```

7. Run the following management commands to update your database tables with the new modeltranslation fields:

    ```bash
    python manage.py makemigrations cookie_consent
    python manage.py migrate
    ```

## Configuration

1. Add cookie groups through the Django admin panel.

2. Create a `static/cookie_consent/` directory in your project and add your cookie scripts to the `static/cookie_consent/cookies/` folder. The script filenames must match the `Variable name` specified in the corresponding cookie group.

3. To modify the default templates and JavaScript, copy the `templates/cookie_consent/` files to your project and make the desired changes.

4. Add the following line near the top of the `<head>` section in your `base.html` template:

    ```python
    {% include 'cookie_consent/include/header.html' %}
    ```

5. Add the JavaScript function call to trigger cookie handling on page load. You can do this in one of two ways:

    Option 1 - Using the body onload attribute:
    ```html
    <body onLoad="handleCookies()">
    ```

    If Option 1 is not working, try Option 2.
    
    Option 2 - Using DOMContentLoaded event listener (add this in the `<head>` tag):
    ```html
    <head>
        ...
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                handleCookies();
            });
        </script>
        ...
    </head>
    ```

6. Near the end of the `body` in your `base.html` template, include one of the cookie consent templates:

    ```python
    {% include 'cookie_consent/include/cookie_bar_body.html' %}
    {% include 'cookie_consent/include/cookie_modal_body.html' %}
    ```

7. Configure non-essential group cookies in the Django admin panel with the correct cookie name and domain (if different from your actual domain) so that the middleware can properly delete these cookies when declined.

## Adapting for specific use cases

The JavaScript if/else cases are automatically generated by Django for each cookie group variable name. However, you can also hardcode them for specific cookie groups by replacing `{{ cookie_group_varname }}` with the respective cookie group variable name and adding custom operations in the if/else cases for each cookie group.


```js
// templates/cookie_consent/include/cookie_modal_body.html

{% for cookie_group_varname in cookie_groups %}
    console.log("Checking {{ cookie_group_varname }} cookies");
    if (data.acceptedCookieGroups.includes("{{ cookie_group_varname }}")) {
        // Load cookie scripts if not already loaded
        if (!document.querySelector('script[data-cookie-group="{{ cookie_group_varname }}"]')) {
            const script = document.createElement("script");
            script.src = "{% static 'cookie_consent/cookies/' %}{{ cookie_group_varname }}.js";
            script.setAttribute("data-cookie-group", "{{ cookie_group_varname }}");
            script.onload = function() {
                console.log("{{ cookie_group_varname }} cookies script loaded");
            };
            head.appendChild(script);
        } else {
            // If script is already loaded, just run checkCookie()
            console.log("{{ cookie_group_varname }} cookies script already loaded");
        }
    } else if (data.declinedCookieGroups.includes("{{ cookie_group_varname }}")) {
        // Remove existing cookie scripts if cookies are declined
        const existingScripts = document.querySelectorAll('script[data-cookie-group="{{ cookie_group_varname }}"]');
        existingScripts.forEach(script => script.remove());
        console.log("{{ cookie_group_varname }} cookies script removed");
    } else {
        // Optionally handle not set state
        console.log("{{ cookie_group_varname }} cookies script not set");
    }
{% endfor %}
```

Example of hardcoded if/else cases for cookie groups:
```js
<script>
    function handleCookies() {
        cookiesStatusUrl = "{% url 'cookie_consent_status' %}";

        fetch(cookiesStatusUrl)
            .then(response => response.json())
            .then(data => {
                const head = document.head;

                if (data.acceptedCookieGroups.includes("analytics_variable")) {
                    gtagGrantConsent();
                }
                else if (data.declinedCookieGroups.includes("analytics_variable")) {
                    gtagRevokeConsent();
                } else {
                    // Optionally handle not set state
                }
            })
            .catch(error => console.error("Error fetching cookie status:", error));
    }
</script>
```

When adding additional cookie scripts in `/static/cookie_consent/cookies/{{ cookie_group_varname }}.js`, set the `data-cookie-group` attribute to match the `{{ cookie_group_varname }}` value. This ensures the script is removed when cookies for that group are declined. Here's an example of an `analytics_variable.js` file:

```js
// Initialize the dataLayer and gtag function
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}

gtag('consent', 'default', {
  'ad_storage': 'denied',
  'ad_user_data': 'denied',
  'ad_personalization': 'denied',
  'analytics_storage': 'granted',
  'wait_for_update': 500
});

// Configure gtag
function loadGoogleAnalytics() {
    gtag('js', new Date());
    // Replace G-XXXXXXXXXX with your actual Google Analytics ID
    gtag('config', 'G-XXXXXXXXXX');
    gtag('consent', 'update', {
      'analytics_storage': 'granted'
    });
}

// Load the Google Analytics script asynchronously
var script_google_analytics = document.createElement('script');
script_google_analytics.async = true;
script_google_analytics.src = 'https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX';
// Add the same data-cookie-group attribute as the cookie group varname
script_google_analytics.setAttribute("data-cookie-group", "analytics_variable");
script_google_analytics.onload = loadGoogleAnalytics;
document.head.appendChild(script_google_analytics);
```

To use the `cookie_bar` in addition to or instead of the `cookie_modal`, uncomment the following code in `/templates/cookie_consent/include/header.html` and style the component as desired:

```js
{% load cookie_consent_tags %}
{% if not request|all_cookies_accepted %}
    {% static "cookie_consent/cookiebar.module.js" as cookiebar_src %}
    {% url 'cookie_consent_status' as status_url %}
    <script type="module">
        import {showCookieBar} from '{{ cookiebar_src }}';
        showCookieBar({
            statusUrl: '{{ status_url|escapejs }}',
            templateSelector: '#cookie-consent__cookie-bar',
            cookieGroupsSelector: '#cookie-consent__cookie-groups',
            onShow: () => document.querySelector('body').classList.add('with-cookie-bar'),
            onAccept: () => document.querySelector('body').classList.remove('with-cookie-bar'),
            onDecline: () => document.querySelector('body').classList.remove('with-cookie-bar'),
        });
    </script>
    {% all_cookie_groups 'cookie-consent__cookie-groups' %}
{% endif %}
```
