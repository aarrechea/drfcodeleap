# Heroku Deployment Guide

This guide will help you deploy your Django REST Framework application to Heroku.

## Prerequisites

- Heroku CLI installed ([Download here](https://devcenter.heroku.com/articles/heroku-cli))
- Git repository initialized
- Heroku account created

## Deployment Steps

### 1. Login to Heroku

```bash
heroku login
```

### 2. Create a Heroku App

```bash
heroku create your-app-name
```

Or let Heroku generate a name:

```bash
heroku create
```

### 3. Add PostgreSQL Database

```bash
heroku addons:create heroku-postgresql:essential-0
```

### 4. Set Environment Variables

Set all required environment variables on Heroku:

```bash
# Required: Secret key for Django
heroku config:set SECRET_KEY="your-secret-key-here"

# Required: Set DEBUG to False in production
heroku config:set DEBUG=False

# Required: Add your Heroku app domain
heroku config:set ALLOWED_HOSTS=".herokuapp.com,your-custom-domain.com"

# Required: CORS allowed origins (your frontend URL)
heroku config:set CORS_ALLOWED_ORIGINS="https://your-frontend.com,https://www.your-frontend.com"

# Note: DATABASE_URL is automatically set by Heroku PostgreSQL addon
```

### 5. Deploy to Heroku

```bash
# Add all files to git
git add .

# Commit your changes
git commit -m "Prepare for Heroku deployment"

# Push to Heroku
git push heroku main
```

If your main branch is named `master`:

```bash
git push heroku master
```

### 6. Run Database Migrations

```bash
heroku run python manage.py migrate
```

### 7. Create a Superuser (Optional)

```bash
heroku run python manage.py createsuperuser
```

### 8. Collect Static Files

This happens automatically during deployment, but you can run it manually:

```bash
heroku run python manage.py collectstatic --noinput
```

## Verify Deployment

### Check if the app is running

```bash
heroku open
```

Or visit: `https://your-app-name.herokuapp.com/`

### View Logs

```bash
heroku logs --tail
```

### Test API Endpoints

- API Docs: `https://your-app-name.herokuapp.com/api/docs/`
- Posts: `https://your-app-name.herokuapp.com/api/post/`
- Register: `https://your-app-name.herokuapp.com/api/auth/register/`

## Environment Variables Reference

Configure these in Heroku dashboard or via CLI:

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `django-insecure-xyz...` |
| `DEBUG` | Debug mode (False in production) | `False` |
| `ALLOWED_HOSTS` | Allowed host domains | `.herokuapp.com,example.com` |
| `CORS_ALLOWED_ORIGINS` | Frontend URLs for CORS | `https://frontend.com` |
| `DATABASE_URL` | PostgreSQL connection (auto-set) | `postgres://user:pass@host/db` |

## Troubleshooting

### Application Error (H10)

Check logs: `heroku logs --tail`

Common causes:
- Missing environment variables
- Database not migrated
- Errors in code

### Static Files Not Loading

Run collectstatic:

```bash
heroku run python manage.py collectstatic --noinput
```

### Database Connection Issues

Verify DATABASE_URL is set:

```bash
heroku config:get DATABASE_URL
```

### CORS Errors

Ensure `CORS_ALLOWED_ORIGINS` includes your frontend URL:

```bash
heroku config:set CORS_ALLOWED_ORIGINS="https://your-frontend.com"
```

## Updating Your App

After making code changes:

```bash
git add .
git commit -m "Your commit message"
git push heroku main
```

If you changed models, run migrations:

```bash
heroku run python manage.py migrate
```

## Useful Heroku Commands

```bash
# View app info
heroku info

# Open app in browser
heroku open

# View logs
heroku logs --tail

# Run Django shell
heroku run python manage.py shell

# Restart the app
heroku restart

# View config vars
heroku config

# Scale dynos
heroku ps:scale web=1
```

## Next Steps

1. Set up a custom domain
2. Configure SSL (automatic with Heroku)
3. Set up monitoring and alerts
4. Configure automated backups for PostgreSQL
5. Set up CI/CD pipeline

## Additional Resources

- [Heroku Django Deployment Guide](https://devcenter.heroku.com/articles/django-app-configuration)
- [Heroku Postgres Documentation](https://devcenter.heroku.com/articles/heroku-postgresql)
- [Heroku CLI Commands](https://devcenter.heroku.com/articles/heroku-cli-commands)
