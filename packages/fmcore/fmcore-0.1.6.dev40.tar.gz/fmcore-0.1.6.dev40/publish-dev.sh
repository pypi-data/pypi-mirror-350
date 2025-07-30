#!/bin/bash

# Create trap to restore pyproject.toml on any error or script exit
cleanup() {
  if [ -f pyproject.toml.bak ]; then
    echo "Restoring original pyproject.toml"
    mv pyproject.toml.bak pyproject.toml
  fi
}

# Set the trap for script exit or errors
trap cleanup EXIT ERR INT TERM

# Ensure script exits on failure
set -e

# Default repository is PyPI
REPOSITORY="pypi"

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
    -v|--version) DEV_VERSION="$2"; shift ;;
    -t|--test) REPOSITORY="testpypi" ;;
    *) echo "Unknown parameter: $1"; exit 1 ;;
  esac
  shift
done

# If no version provided via command line, prompt for it
if [ -z "$DEV_VERSION" ]; then
    # Prompt user for version
    echo "Enter the version number to publish (e.g., 0.1.5.dev0):"
    read DEV_VERSION

    # Validate input is not empty
    if [ -z "$DEV_VERSION" ]; then
        echo "Error: Version number cannot be empty."
        exit 1
    fi
fi

# Verify the version format
if ! [[ $DEV_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+(\.dev[0-9]+)?$ ]]; then
    echo "Error: Version must be in format X.Y.Z or X.Y.Z.devN"
    exit 1
fi

# Display selected repository
if [ "$REPOSITORY" = "testpypi" ]; then
    echo "Publishing to Test PyPI (https://test.pypi.org)"
    REPO_URL="https://test.pypi.org/pypi/fmcore/$DEV_VERSION/json"
    PUBLISH_ARGS="--repo test"
else
    echo "Publishing to PyPI (https://pypi.org)"
    REPO_URL="https://pypi.org/pypi/fmcore/$DEV_VERSION/json"
    PUBLISH_ARGS=""
fi

# Check if tag already exists
if git rev-parse "v$DEV_VERSION" >/dev/null 2>&1; then
    echo "Warning: Tag v$DEV_VERSION already exists"
    read -p "Do you want to delete and recreate this tag? (y/n): " confirm
    if [[ $confirm == [yY] ]]; then
        echo "Deleting existing tag"
        git tag -d "v$DEV_VERSION"
        git push origin --delete "v$DEV_VERSION" 2>/dev/null || true
    else
        echo "Aborting as tag already exists"
        exit 1
    fi
fi

# Check if version already exists on target repository
echo "Checking if version exists on $REPOSITORY..."
if curl -s "$REPO_URL" | grep -q "version"; then
    echo "Warning: Version $DEV_VERSION already exists on $REPOSITORY"
    echo "Please note: You need to manually delete this version"
    if [ "$REPOSITORY" = "testpypi" ]; then
        echo "1. Go to https://test.pypi.org/project/fmcore/"
    else
        echo "1. Go to https://pypi.org/project/fmcore/"
    fi
    echo "2. Click on 'Manage'"
    echo "3. Find version $DEV_VERSION and delete it via 'Options' dropdown"
    read -p "Press Enter after you have deleted the version (or Ctrl+C to abort): " _

    # Wait a moment for repository to process the deletion
    echo "Checking if deletion was successful..."
    max_attempts=5
    attempt=1
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$REPO_URL" | grep -q "version"; then
            echo "Attempt $attempt/$max_attempts: Version still exists. Waiting 10 seconds..."
            sleep 10
            attempt=$((attempt + 1))
        else
            echo "Version successfully deleted!"
            break
        fi
    done

    # Final verification
    if curl -s "$REPO_URL" | grep -q "version"; then
        echo "Error: Version $DEV_VERSION still exists after multiple checks."
        echo "Please ensure the version is completely deleted before running this script again."
        exit 1
    fi
fi

# Clean up dist directory
echo "Cleaning up dist directory"
rm -rf dist/

echo "Creating dev release: $DEV_VERSION"

# Create and push new Git tag
git tag "v$DEV_VERSION"
git push origin "v$DEV_VERSION"

# Save the original pyproject.toml as a backup
cp pyproject.toml pyproject.toml.bak

# Remove the hatch.version section completely (including the "source = vcs" line)
awk '!/\[tool.hatch.version\]/ && !/source = "vcs"/' pyproject.toml > pyproject.tmp && mv pyproject.tmp pyproject.toml

# Add the static version under the [project] section correctly
# Insert `version = "$DEV_VERSION"` directly under the [project] section
sed -i '' "/^\[project\]/a\\
version = \"$DEV_VERSION\"\\
" pyproject.toml

# Optional: Print a message confirming the build with static version
echo "Building with static version $DEV_VERSION"

# Run the build process (hatch build)
hatch build


echo "Publishing to $REPOSITORY"
# Add this before your publish command
if [ "$REPOSITORY" = "testpypi" ]; then
    echo "Enter your TestPyPI token:"
    read -s PYPI_TOKEN
    PUBLISH_ARGS="--repo test --user __token__ --auth $PYPI_TOKEN"
else
    echo "Enter your PyPI token:"
    read -s PYPI_TOKEN
    PUBLISH_ARGS="--user __token__ --auth $PYPI_TOKEN"
fi

# Then use this token in your publish command
echo "Publishing to $REPOSITORY"
hatch publish $PUBLISH_ARGS

echo "Dev release $DEV_VERSION published successfully to $REPOSITORY! 🚀"

# The cleanup function will be called automatically when the script exits