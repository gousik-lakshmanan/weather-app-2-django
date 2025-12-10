import os

# CORRECTED PATH: Removed the extra 'weather_project' folder
settings_path = os.path.join('weather_project', 'settings.py')

# Verify file exists before trying to open
if not os.path.exists(settings_path):
    print(f"❌ Error: Could not find settings.py at: {settings_path}")
    print("Please check if your main project folder is named 'weather_project'.")
    exit(1)

# Read the file
with open(settings_path, 'r') as f:
    lines = f.readlines()

new_lines = []
middleware_added = False
static_configured = False

for line in lines:
    # 1. Update ALLOWED_HOSTS
    if line.startswith('ALLOWED_HOSTS'):
        new_lines.append("ALLOWED_HOSTS = ['*']\n")
        print("✅ Updated ALLOWED_HOSTS")
        continue

    # 2. Add WhiteNoise Middleware
    if 'django.middleware.security.SecurityMiddleware' in line and not middleware_added:
        new_lines.append(line)
        # Add WhiteNoise right after SecurityMiddleware
        new_lines.append("    'whitenoise.middleware.WhiteNoiseMiddleware',\n")
        middleware_added = True
        print("✅ Added WhiteNoise Middleware")
        continue

    # Check if static config already exists to avoid duplicates
    if 'STATIC_ROOT' in line:
        static_configured = True

    new_lines.append(line)

# 3. Add Static Files Configuration at the end
if not static_configured:
    new_lines.append("\n")
    new_lines.append("# Production Static Files Config\n")
    new_lines.append("STATIC_ROOT = BASE_DIR / 'staticfiles'\n")
    new_lines.append("STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'\n")
    print("✅ Added Static Files Configuration")

# Save the file
with open(settings_path, 'w') as f:
    f.writelines(new_lines)

print("\nSuccess! settings.py is ready for Render.")