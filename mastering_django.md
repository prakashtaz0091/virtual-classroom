# Key technologies and topics to learn after this course:

## 🌐 1. Django REST Framework (DRF) — API Development

**Why:** Used to build RESTful APIs in Django projects.

**What to Learn:**

- Serializers (ModelSerializer, HyperlinkedSerializer)
- Views (APIView, GenericView, ViewSets)
- Routers
- Authentication (Token, JWT, Session)
- Permissions & Throttling

**Docs & Tutorials:**

- [Official DRF Docs](https://www.django-rest-framework.org/)
- [DRF Quickstart](https://www.django-rest-framework.org/tutorial/quickstart/)
- YouTube: [Code With Stein DRF Series](https://www.youtube.com/playlist?list=PLLRM7ROnmA9E0P8aJkFgdvE3y4Cuxqdx7)

---

## ⚡ 2. Django Channels — WebSockets / Real-time Features

**Why:** To build real-time apps like chat, notifications, and live updates.

**What to Learn:**

- ASGI vs WSGI
- Consumers (Sync and Async)
- WebSocket Protocol
- Routing for channels
- Group messaging and sessions

**Docs & Tutorials:**

- [Django Channels Official Docs](https://channels.readthedocs.io/en/stable/)
- YouTube: [Dennis Ivy Real-time Chat with Django Channels](https://www.youtube.com/watch?v=SCZF5P8lU3U)

---

## 🔁 3. Redis — In-memory Store / Message Broker

**Why:** Works with Django for caching, storing sessions, and pub-sub for Django Channels.

**Use Cases:**

- Django caching backend
- Celery message broker
- WebSocket channel layer backend

**Docs & Tutorials:**

- [Redis.io Docs](https://redis.io/docs/)
- [How to Use Redis with Django](https://realpython.com/caching-in-django-with-redis/)

---

## ⏳ 4. Celery — Task Queues / Background Jobs

**Why:** For running tasks asynchronously (e.g., sending emails, generating reports).

**What to Learn:**

- Task creation and delay()
- Periodic tasks with Celery Beat
- Integrating with Redis/RabbitMQ
- Monitoring with Flower

**Docs & Tutorials:**

- [Celery Official Docs](https://docs.celeryq.dev/en/stable/)
- [Simple Celery + Django Setup](https://realpython.com/asynchronous-tasks-with-django-and-celery/)
- YouTube: [Celery + Django Tutorial by Dennis Ivy](https://www.youtube.com/watch?v=0D5EEKH97NA)

---

## 📦 5. Django Packages Worth Exploring

| Package                        | Purpose                            | Docs                                                     |
| ------------------------------ | ---------------------------------- | -------------------------------------------------------- |
| `django-allauth`               | Authentication (social + email)    | [Docs](https://django-allauth.readthedocs.io/en/latest/) |
| `django-environ`               | Manage `.env` configs              | [GitHub](https://github.com/joke2k/django-environ)       |
| `django-filter`                | Filtering querysets in APIs        | [Docs](https://django-filter.readthedocs.io/en/stable/)  |
| `drf-yasg` / `drf-spectacular` | API Schema & Swagger UI            | [drf-yasg](https://github.com/axnsan12/drf-yasg)         |
| `whitenoise`                   | Serving static files in production | [Docs](http://whitenoise.evans.io/en/stable/)            |

---

## 📊 6. Testing and CI/CD

**Why:** To ensure code quality and automate deployments.

**Topics:**

- `pytest`, `pytest-django`
- Unit tests with Django’s TestCase
- GitHub Actions / GitLab CI
- Deployments using Docker + CI

**Docs & Tutorials:**

- [Django Testing Docs](https://docs.djangoproject.com/en/stable/topics/testing/)
- [pytest-django Docs](https://pytest-django.readthedocs.io/en/latest/)
- [GitHub Actions Django CI Tutorial](https://testdriven.io/blog/django-github-actions/)

---

## 🐳 7. Docker & Docker Compose — Containerization

**Why:** To make your Django app portable, consistent, and production-ready.

**What to Learn:**

- Dockerfile and `.dockerignore`
- `docker-compose.yml` with services: db, redis, web
- Docker volumes, ports, environment variables

**Docs & Tutorials:**

- [Dockerizing Django App](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)
- YouTube: [Docker + Django by CodeWithStein](https://www.youtube.com/watch?v=YjFkO3TnKPo)

---

## 🔐 8. JWT Authentication

**Why:** Token-based authentication for stateless APIs (esp. for mobile / SPA).

**Libraries:**

- `djangorestframework-simplejwt` – [Docs](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- `rest_framework_jwt` (older)

---

## 📈 9. Performance Optimization

- **select_related / prefetch_related**
- **Database indexing**
- **Django Debug Toolbar**
- **N+1 query issues**
- **Connection pooling** (via PgBouncer or persistent connections)

---

## 🌍 10. Deployment Platforms

| Platform               | Highlights                 | Guide                                                                                                           |
| ---------------------- | -------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Heroku**             | Beginner-friendly PaaS     | [Guide](https://devcenter.heroku.com/categories/python-support)                                                 |
| **Render**             | Free tier + simple config  | [Guide](https://render.com/docs/deploy-django)                                                                  |
| **DigitalOcean / VPS** | Full control               | [DO + Docker Guide](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-local-django-app-to-a-vps) |
| **Railway.app**        | Modern, simple deployments | [Railway](https://railway.app/)                                                                                 |

---

## 🧠 11. Bonus Topics

- **GraphQL with Django:** [`graphene-django`](https://docs.graphene-python.org/projects/django/en/latest/)
- **Signals & Middleware** in Django
- **Class-Based Views vs Function-Based Views**
- **Custom Permissions / Decorators / Mixins**
- **Multi-tenancy and SaaS-style architecture**
