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

## 4. Option C: Deploy to Babal Host (Nepal, cPanel)

[Babal Host](https://babal.host/python-hosting) offers Python/Django hosting with cPanel and **Install Python App**. Use this to run the site on your own domain in Nepal.

### 4.1 Upload code

**Note:** “SSH Access” in cPanel is only for managing SSH keys. To upload code, use **File Manager** (easiest) or **Terminal** (after SSH is set up).

- **Option A – File Manager (sajilo):**
  1. cPanel मा **Files** → **File Manager** खोल्नुहोस्।
  2. `home` वा आफ्नो username को folder भित्र जानुहोस्। नया folder बनाउनुहोस् जस्तै `website`।
  3. त्यो `website` folder भित्र **Upload** क्लिक गरेर सबै project files upload गर्नुहोस्: `manage.py`, `passenger_wsgi.py`, `requirements.txt`, र `config/`, `apps/`, `templates/`, `static/` पूरा folders (त्यसै structure)। **नउpload गर्नु:** `venv/`, `__pycache__/`, `.env`, `.git`।
- **Option B – Git (Terminal):** cPanel मा **Terminal** (वा SSH) खोलेर project folder बनाउनुहोस्, त्यहाँ जानुहोस्, अनि:
  ```bash
  git clone https://github.com/pabit06/website.git .
  ```
  (SSH Access पेजले key मात्र manage गर्छ; Terminal/SSH बाट login गर्दा त्यो key use हुन्छ।)

### 4.2 Create Python app in cPanel

1. Log in to **cPanel** (Babal Host login).
2. Open **Setup Python App** or **Install Python App** (under Software).
3. **Create Application**:
   - **Python version:** 3.10 or 3.11 (whatever is available).
   - **Application root:** Folder where you uploaded the project (e.g. `website` or `djangoapps`).
   - **Application URL:** Your domain or subdomain (e.g. `yourdomain.com` or `www.yourdomain.com`).
4. Save. cPanel will create a virtualenv and show you its path (e.g. `~/virtualenv/website/3.10`).

### 4.3 Install dependencies and collect static

In cPanel open **Terminal** (or use SSH). Then:

```bash
# Activate the virtualenv (path may differ; use the one cPanel showed)
source ~/virtualenv/website/3.10/bin/activate   # adjust path/version

# Go to project root (where manage.py and passenger_wsgi.py are)
cd ~/website   # or ~/djangoapps, etc.

# Install packages
pip install -r requirements.txt

# Collect static files (CSS/JS) for WhiteNoise
python manage.py collectstatic --noinput
```

### 4.4 Point app to Django (Passenger)

- In **Setup Python App** / **Application Manager**, set:
  - **Application startup file** or **WSGI file:** `passenger_wsgi.py`
  - **Application root:** Same folder that contains `passenger_wsgi.py` and `manage.py`.
- If there is a field for “Application entry point”, use: `application` (the variable name in `passenger_wsgi.py`).
- Save and **Restart** the application.

### 4.5 Environment variables (production)

Set these so the site runs in production mode. In cPanel’s Python app settings, add **Environment Variables** (or use a `.env` file in the application root **only if** you don’t upload it to public places and your host allows it):

| Variable        | Value |
|----------------|--------|
| `DEBUG`        | `False` |
| `SECRET_KEY`   | A long random secret (generate one and keep it private) |
| `ALLOWED_HOSTS`| Your domain, e.g. `yourdomain.com,www.yourdomain.com` |

Replace `yourdomain.com` with the actual domain you set in **Application URL**.

### 4.6 Restart and test

- Restart the Python app from cPanel.
- Open **https://yourdomain.com** (with the domain you set). If CSS is missing, run `python manage.py collectstatic --noinput` again from the project root inside the virtualenv.

---

## 5. Post-Deployment Checks

-   **Visit your URL**: Ensure the site loads.
-   **Check Styles**: If CSS is missing, run `python manage.py collectstatic --noinput` (Render does this in the Build Command; on Babal Host run it in Terminal after activating the virtualenv).
-   **Security**: Ensure `DEBUG` is `False` and `SECRET_KEY` is set in your environment variables.
