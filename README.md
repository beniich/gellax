# Gellax — Full-Stack Merchandise Management Platform

Plateforme complète de gestion de marchandise avec authentification JWT, multi-entrepôts et interface web React.

## 📋 Fonctionnalités

- **Backend FastAPI** : API REST complète avec SQLAlchemy ORM
- **Authentification JWT** : OAuth2 password flow, rôles (admin, manager, viewer)
- **Gestion de produits** : CRUD avec catégories
- **Multi-entrepôts** : création d'entrepôts, mouvements d'inventaire entre entrepôts
- **Frontend React** : interface CRUD intuitive pour produits, entrepôts, mouvements
- **Docker & Docker Compose** : déploiement simplifié
- **CI/CD GitHub Actions** : tests automatisés backend/frontend

## 🚀 Démarrage rapide

### Localement (développement)

**Backend** :
```bash
python -m venv .venv
source .venv/bin/activate  # ou .\.venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn gellax.api:app --reload
```

Backend disponible sur `http://localhost:8000`.

**Frontend** :
```bash
cd frontend
npm install
npm run dev
```

Frontend disponible sur `http://localhost:3000`.

### Avec Docker Compose

```bash
docker-compose up
```

- Backend : `http://localhost:8000`
- Frontend : `http://localhost:3000`
- API docs : `http://localhost:8000/docs`

## 📁 Structure du projet

```
.
├── src/gellax/              # Backend Python
│   ├── api.py              # FastAPI app + endpoints
│   ├── models.py           # SQLAlchemy models
│   ├── schemas.py          # Pydantic schemas
│   ├── crud.py             # CRUD helpers
│   ├── security.py         # JWT & auth
│   ├── db.py               # Database setup
│   └── cli.py              # CLI (placeholder)
├── tests/                   # Tests unitaires/intégration
├── frontend/                # React + Vite
│   ├── src/
│   │   ├── App.jsx
│   │   ├── LoginPage.jsx
│   │   ├── ProductsPage.jsx
│   │   ├── WarehousesPage.jsx
│   │   ├── MovementsPage.jsx
│   │   └── ApiContext.jsx
│   ├── package.json
│   └── vite.config.js
├── Dockerfile.backend       # Image Docker backend
├── Dockerfile.frontend      # Image Docker frontend
├── docker-compose.yml       # Orchestration
├── requirements.txt         # Dépendances Python
└── .github/workflows/       # CI/CD
```

## 🔐 Authentification

Login avec credentials de test :
- Username: `mgr`
- Password: `pass`

(Créé via les tests backend, ou utilisez `POST /users/` pour ajouter un nouvel utilisateur.)

## 📚 API Documentation

Une fois le backend lancé, visitez `http://localhost:8000/docs` (Swagger UI) ou `/redoc` (ReDoc).

### Endpoints principaux

- `POST /auth/token` : Login (OAuth2 password)
- `POST /users/` : Créer utilisateur
- `GET/POST /products/` : Lister/créer produits
- `DELETE /products/{id}` : Supprimer produit
- `GET/POST /warehouses/` : Lister/créer entrepôts
- `POST /movements/` : Créer mouvement d'inventaire
- `GET /movements/` : Lister mouvements

## 🧪 Tests

Backend :
```bash
pytest -q
```

Frontend (à implémenter) :
```bash
cd frontend
npm test
```

## 🐳 Déploiement

### Localement avec Docker Compose

```bash
docker-compose up --build
```

### Production

1. Créer un registre Docker (ex. Docker Hub, ECR, ghcr.io)
2. Configurer les secrets GitHub (DOCKER_USERNAME, DOCKER_PASSWORD)
3. Modifier `.github/workflows/ci-cd.yml` pour pousser vers le registre
4. Déployer sur un service (Heroku, AWS ECS, Kubernetes, etc.)

Exemple minimal Heroku :
```bash
heroku login
heroku create gellax-app
git push heroku main
```

## ☁️ Cloudflare Workers

Deploy sur Cloudflare Workers pour une edge deployment gratuite et performante :

```bash
# Install wrangler CLI
npm install -g wrangler

# Authenticate with Cloudflare
wrangler login

# Deploy
wrangler deploy
```

**Configuration** :
- Fichier `wrangler.jsonc` définit les paramètres de déploiement
- `src/worker.js` : Worker script qui proxy les requêtes API et sert le frontend
- Variables d'environnement configurable dans `wrangler.jsonc`

**Points clés** :
- CORS automatique sur toutes les réponses API
- Routes séparées pour API (`/api/*`) et assets statiques
- KV Namespace disponible pour le caching
- R2 Bucket pour le stockage de fichiers
- Observabilité/monitoring activé par défaut

**Configuration pour production** :
```json
{
  "route": "api.gellax.com/*",
  "zone_id": "your-cloudflare-zone-id"
}
```

## 📝 Notes

- Base de données : SQLite par défaut (fichier `gellax.db`). Pour production, utiliser PostgreSQL.
- Secret JWT : à changer dans `src/gellax/security.py` (variable `SECRET_KEY`).
- CORS : configuré automatiquement sur Cloudflare Workers ; à ajouter si frontend/backend sur domaines différents.

## 📞 Support

Pour toute question ou issue, créez une issue sur GitHub.

---

**Gellax** © 2025. MIT License.

