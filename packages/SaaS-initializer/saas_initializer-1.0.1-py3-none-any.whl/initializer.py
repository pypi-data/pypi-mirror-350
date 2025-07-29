import questionary
from git import Repo
import os
import shutil
import subprocess
from initializer_pkg.utils import log, RequiredValidator, edit_line_containing, success, error

def get_packages(selected_features: list[str]) -> str:
    """
    Get the list of packages to be installed based on the selected features.
    """
    # Default packages
    python_packages = [
        "djangorestframework",
        "django",
        "django-cors-headers",
        "python-dotenv",
    ]
    react_packages = [
        "react-router",
        "axios",
        "tailwindcss",
        "@tailwindcss/vite",
    ]
    # Adding packages based on selected features
    for feature in selected_features:
        match feature:
            case "Authentication":
                python_packages.append("djangorestframework_simplejwt")
                react_packages.append("zustand")
            
    return " ".join(python_packages), " ".join(react_packages)

def init_project(selected_features: list[str]):
    """
    Initialize the project with packages for selected features.
    """
    log("Initializing the project...")
    python_str_packages, react_str_packages = get_packages(selected_features)
    # Django project initialization
    os.makedirs(DST_BACKEND_DIR)
    subprocess.run(
        f"\
        python -m venv .venv\
        && source .venv/bin/activate\
        && pip install --upgrade pip\
        && pip install {python_str_packages}\
        && pip freeze > requirements.txt\
        && django-admin startproject backend .\
        ",
        shell=True,
        cwd=DST_BACKEND_DIR
    )
    shutil.move(f"{SRC_BACKEND_DIR}/utils", f"{DST_BACKEND_DIR}/utils")
    shutil.move(f"{SRC_BACKEND_DIR}/.gitignore", f"{DST_BACKEND_DIR}/.gitignore")
    os.remove(f"{DST_BACKEND_DIR}/backend/settings.py")
    os.mkdir(f"{DST_BACKEND_DIR}/backend/settings")
    shutil.move(f"{SRC_BACKEND_DIR}/backend/settings/__init__.py", f"{DST_BACKEND_DIR}/backend/settings/__init__.py")
    shutil.move(f"{SRC_BACKEND_DIR}/backend/settings/base.py", f"{DST_BACKEND_DIR}/backend/settings/base.py")
    with open(f"{DST_BACKEND_DIR}/.env", "w") as file:
       pass
    with open(f"{DST_BACKEND_DIR}/backend/settings/settings.py", "w") as file:
        file.write("from .base import *\n")
    edit_line_containing(
        f"{DST_BACKEND_DIR}/backend/asgi.py",
        [f"os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"backend.settings\")"],
        [f"os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"backend.settings.settings\")\n"]
    )
    edit_line_containing(
        f"{DST_BACKEND_DIR}/backend/wsgi.py",
        [f"os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"backend.settings\")"],
        [f"os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"backend.settings.settings\")\n"]
    )
    edit_line_containing(
        f"{DST_BACKEND_DIR}/manage.py",
        [f"os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"backend.settings\")"],
        [f"    os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"backend.settings.settings\")\n"]
    )
    edit_line_containing(
        f"{DST_BACKEND_DIR}/backend//urls.py",
        ["from django.urls import path"],
        ["from django.urls import path, include\n"]
    )
   
    # React project initialization
    os.makedirs(DST_FRONTEND_DIR)
    subprocess.run(f"\
        yarn create vite . --template react-swc-ts\
        && yarn add {react_str_packages}\
        ",
        shell=True,
        cwd=DST_FRONTEND_DIR
    )
    shutil.move(f"{SRC_FRONTEND_DIR}/vite.config.ts", f"{DST_FRONTEND_DIR}/vite.config.ts")
    shutil.move(f"{SRC_FRONTEND_DIR}/.gitignore", f"{DST_FRONTEND_DIR}/.gitignore")
    shutil.move(f"{SRC_FRONTEND_DIR}/.env", f"{DST_FRONTEND_DIR}/.env")
    shutil.move(f"{SRC_FRONTEND_DIR_SRC}/index.css", f"{DST_FRONTEND_DIR_SRC}/index.css")
    shutil.move(f"{SRC_FRONTEND_DIR_SRC}/main.tsx", f"{DST_FRONTEND_DIR_SRC}/main.tsx")
    shutil.move(f"{SRC_FRONTEND_DIR_SRC}/PATHS.tsx", f"{DST_FRONTEND_DIR_SRC}/PATHS.tsx")
    os.mkdir(f"{DST_FRONTEND_DIR_SRC}/components")
    os.mkdir(f"{DST_FRONTEND_DIR_SRC}/features")
    os.mkdir(f"{DST_FRONTEND_DIR_SRC}/hooks")
    shutil.move(f"{SRC_FRONTEND_DIR_SRC}/hooks/useAxios.tsx", f"{DST_FRONTEND_DIR_SRC}/hooks/useAxios.tsx")
    os.mkdir(f"{DST_FRONTEND_DIR_SRC}/pages")
    os.mkdir(f"{DST_FRONTEND_DIR_SRC}/services")
    shutil.move(f"{SRC_FRONTEND_DIR_SRC}/services/backend.tsx", f"{DST_FRONTEND_DIR_SRC}/services/backend.tsx")
    os.mkdir(f"{DST_FRONTEND_DIR_SRC}/stores")
    os.mkdir(f"{DST_FRONTEND_DIR_SRC}/types")
    os.mkdir(f"{DST_FRONTEND_DIR_SRC}/layouts")
    os.remove(f"{DST_FRONTEND_DIR_SRC}/assets/react.svg")
    os.remove(f"{DST_FRONTEND_DIR_SRC}/App.css")

    success("Project initialized successfully.")
    
def add_features(selected_features: list[str]):
    """
    Add files based on selected features.
    """

    for feature in FEATURES:
        # Adding files based on selected features
        if feature in selected_features:
            log(f"Adding {feature} feature...")
            match feature:
                case "Authentication":
                    # Backend
                    shutil.move(f"{SRC_BACKEND_DIR}/authentification", f"{DST_BACKEND_DIR}/authentification")
                    shutil.move(f"{SRC_BACKEND_DIR}/backend/settings/auth.py", f"{DST_BACKEND_DIR}/backend/settings/auth.py")
                    with open(f"{DST_BACKEND_DIR}/backend/settings/settings.py", "a") as file:
                        file.write("from .auth import *\n")
                    edit_line_containing(
                        f"{DST_BACKEND_DIR}/backend/urls.py",
                        ["]"],
                        ["    path(\"auth/\", include(\"authentification.urls\")),\n]"]
                    )
                    # Frontend
                    shutil.move(f"{SRC_FRONTEND_DIR_SRC}/components/Logout.tsx", f"{DST_FRONTEND_DIR_SRC}/components/Logout.tsx")
                    shutil.move(f"{SRC_FRONTEND_DIR_SRC}/components/ProtectedRoute.tsx", f"{DST_FRONTEND_DIR_SRC}/components/ProtectedRoute.tsx")
                    shutil.move(f"{SRC_FRONTEND_DIR_SRC}/features/auth", f"{DST_FRONTEND_DIR_SRC}/features/auth")
                    shutil.move(f"{SRC_FRONTEND_DIR_SRC}/pages/Home.tsx", f"{DST_FRONTEND_DIR_SRC}/pages/Home.tsx")
                    shutil.move(f"{SRC_FRONTEND_DIR_SRC}/pages/Login.tsx", f"{DST_FRONTEND_DIR_SRC}/pages/Login.tsx")
                    shutil.move(f"{SRC_FRONTEND_DIR_SRC}/stores/useUserStore.tsx", f"{DST_FRONTEND_DIR_SRC}/stores/useUserStore.tsx")
                    shutil.move(f"{SRC_FRONTEND_DIR_SRC}/types/User.tsx", f"{DST_FRONTEND_DIR_SRC}/types/User.tsx")
                    shutil.move(f"{SRC_FRONTEND_DIR_SRC}/App.tsx", f"{DST_FRONTEND_DIR_SRC}/App.tsx")
                case "API":
                    # Backend
                    shutil.move(f"{SRC_BACKEND_DIR}/api", f"{DST_BACKEND_DIR}/api")
                    shutil.move(f"{SRC_BACKEND_DIR}/backend/settings/api.py", f"{DST_BACKEND_DIR}/backend/settings/api.py")
                    with open(f"{DST_BACKEND_DIR}/backend/settings/settings.py", "a") as file:
                        file.write("from .api import *\n")
                    edit_line_containing(
                        f"{DST_BACKEND_DIR}/backend/urls.py",
                        ["]"],
                        ["    path(\"api/\", include(\"api.urls\")),\n]"]
                    )
            success(f"{feature} feature added successfully.")         

def main():
    global FEATURES, SRC_BACKEND_DIR, DST_BACKEND_DIR, SRC_FRONTEND_DIR_SRC, DST_FRONTEND_DIR_SRC, SRC_FRONTEND_DIR, DST_FRONTEND_DIR
    FEATURES = [
        "Authentication", 
        "API",
    ]

    try:
        answers = questionary.form(
            project_name = questionary.text("What is the name of your project?", validate=RequiredValidator),
            features = questionary.checkbox("Select the features you want to include in your project:", choices=FEATURES),
        ).ask()
        project_name = answers['project_name']
        selected_features = answers['features']
        SRC_BACKEND_DIR = "template_repo/backend"
        DST_BACKEND_DIR = f"{project_name}/backend"
        SRC_FRONTEND_DIR_SRC = "template_repo/frontend/src"
        DST_FRONTEND_DIR_SRC = f"{project_name}/frontend/src"
        SRC_FRONTEND_DIR = "template_repo/frontend"
        DST_FRONTEND_DIR = f"{project_name}/frontend"
        
       
        log("Cloning the repository...")
        Repo.clone_from("https://github.com/Soulflys02/web-dev-framework.git", "template_repo")
        success("Repository cloned successfully.")
        init_project(selected_features)
        add_features(selected_features)
        shutil.rmtree("template_repo")
        success("Project setup completed successfully.")


    except Exception as e:
        error(e)
    
if __name__ == "__main__":
    main()