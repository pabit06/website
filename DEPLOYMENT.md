# Deployment Guide

This guide outlines how to deploy the **Bhanjyang Cooperative** website to production. Since the project is currently a lightweight Django application (without a production database configured), platforms like **Render** or **Vercel** are excellent, cost-effective choices.

---

## 1. Preparation (Before You Deploy)

To serve the application and static files (CSS/JS) reliably in production, you need to add a few dependencies.

## 1. Preparation (Already Configured)

I have already configured your project for production:

1.  **Installed Production Helpers**: `gunicorn` and `whitenoise` are installed.
2.  **Updated `requirements.txt`**: Includes these new packages.
3.  **Configured `settings.py`**: Added `WhiteNoiseMiddleware` and set static storage.

**You are ready to proceed to Step 2!**

---

## 2. Option A: Deploy to Render (Recommended)

Render is great for Django apps. It connects to your GitHub repository and updates automatically when you push code.

1.  **Push to GitHub**: Make sure your latest code (with the changes above) is on GitHub.
2.  **Create Web Service**:
    -   Log in to [Render.com](https://render.com).
    -   Click **New +** -> **Web Service**.
    -   Connect your GitHub repository.
3.  **Configure Settings**:
    -   **Name**: `bhanjyang-website`
    -   **Runtime**: `Python 3`
    -   **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
    -   **Start Command**: `gunicorn config.wsgi:application`
4.  **Environment Variables**:
    Add the following in the **Environment** tab:
    -   `PYTHON_VERSION`: `3.10.0` (or your local version)
    -   `SECRET_KEY`: (Generate a long random string)
    -   `DEBUG`: `False`
    -   `ALLOWED_HOSTS`: `*` (or your render URL, e.g., `bhanjyang.onrender.com`)

Render will build and deploy your site. It implies SSL (HTTPS) automatically.

---

## 3. Option B: Deploy to Vercel

Vercel is excellent for static-like sites and offers a generous free tier.

1.  Create a file named `vercel.json` in the root directory:
    ```json
    {
      "builds": [{
        "src": "config/wsgi.py",
        "use": "@vercel/python",
        "config": { "maxLambdaSize": "15mb", "runtime": "python3.9" }
      }],
      "routes": [
        {
          "src": "/(.*)",
          "dest": "config/wsgi.py"
        }
      ]
    }
    ```
2.  Install the Vercel CLI or connect your GitHub repo to Vercel.
3.  In Vercel **Project Settings** -> **Environment Variables**, add:
    -   `DEBUG`: `False`
    -   `SECRET_KEY`: (Your secret key)
    -   `ALLOWED_HOSTS`: `.vercel.app`

---

## 4. Post-Deployment Checks

-   **Visit your URL**: Ensure the site loads.
-   **Check Styles**: If CSS is missing, double-check that you added `whitenoise` to your Middleware and ran `collectstatic` (Render does this in the Build Command).
-   **Security**: Ensure `DEBUG` is definitely `False` in your environment variables.
