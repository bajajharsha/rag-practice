import os


def create_dir_structure(base_path):
    directories = [
        "src/app/config",
        "src/app/controllers",
        "src/app/models/domain",
        "src/app/models/schemas",
        "src/app/repositories",
        "src/app/routes",
        "src/app/services",
        "src/app/usecases/auth",
        "src/app/utils",
    ]
    files = [
        "src/app/config/database.py",
        "src/app/config/settings.py",
        "src/app/controllers/auth_controller.py",
        "src/app/models/domain/user.py",
        "src/app/models/schemas/user_schema.py",
        "src/app/repositories/user_repository.py",
        "src/app/routes/auth_routes.py",
        "src/app/services/auth_service.py",
        "src/app/utils/security.py",
        "src/app/utils/error_handler.pysrc/.env",
        "src/main.py",
        # ".gitignore",
        "readme.md",
        # "track.md"
    ]
    # Create directories
    for directory in directories:
        os.makedirs(os.path.join(base_path, directory), exist_ok=True)
        # Create __init__.py in each directory
        init_path = os.path.join(base_path, directory, "__init__.py")
        with open(init_path, "w") as f:
            f.write("")
    # Create files
    for file in files:
        file_path = os.path.join(base_path, file)
        with open(file_path, "w") as f:
            f.write("# Placeholder for " + os.path.basename(file))


if __name__ == "__main__":
    create_dir_structure("vanilla_rag/")
