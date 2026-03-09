---
title: Flask Elite Backend Architecture (2026)
date: 2026-03-08
task_ref: tech-expansion
confidence_score: 1.0
tags: [backend, python, flask, blueprints, patterns]
links: ["[[skills/backend/python-elite]]"]
---

# Flask Elite Backend Architecture (2026)

## 🎯 Purpose
Guidelines for building enterprise-grade, modular Flask applications. Use for any non-trivial Flask backend.

## 🛠️ The Process / Fact

### 1. The Application Factory (`create_app`)
- **NEVER** use a global `app` object.
- **ALWAYS** initialize within a factory function.
- **Module Structure (`app/__init__.py`):**
  ```python
  def create_app(config_name="dev"):
      app = Flask(__name__)
      db.init_app(app)  # Initialize extensions separately
      from app.modules.auth.routes import auth_bp
      app.register_blueprint(auth_bp, url_prefix="/auth")
      return app
  ```

### 2. Feature-Based Organization (Domain Logic)
Instead of grouping by layer (models, routes), group by **Feature (Domain)**.
- **Example Directory:**
  - `app/modules/auth/`
    - `routes.py`: Blueprint routes (thin layer).
    - `services.py`: Business logic and orchestration (the "Meat").
    - `models.py`: Module-specific models.

### 3. Extension Isolation (`extensions.py`)
- Define global instances (e.g., `db = SQLAlchemy()`) in an `extensions.py` file.
- **Prevents Circular Imports:** Your models and factory function both reference this file, not each other.

### 4. 2026 Best Practices
- **Environment Management:** Use `python-dotenv` for settings.
- **Configuration Classes:** Use a `config.py` with environment-specific subclasses (DevConfig, ProdConfig).
- **Service Layer Pattern:** Move complex logic from routes to services. This allows for easier unit testing of core logic without mocks.

## ⚠️ Known Quirks or Edge Cases
- **Blueprint Prefixing:** Use `url_prefix` for namespacing and consistency.
- **Template Inheritance:** Centralize the `base.html` in a global `templates/` folder, with module-specific templates in `modules/<feature>/templates`.

## 🔗 Related Memories
- [[skills/backend/python-elite]]
