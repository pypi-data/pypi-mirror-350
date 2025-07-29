import re
import toml


def parse_version(version):
    # Matches versions like 0.1.51 or 0.1.51b1
    match = re.match(r"(\d+)\.(\d+)\.(\d+)(b\d+)?", version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")
    major, minor, patch, beta = match.groups()
    return int(major), int(minor), int(patch), beta


def get_next_beta_version(current_version):
    major, minor, patch, beta = parse_version(current_version)
    if beta:
        # Increment beta number (e.g., b1 -> b2)
        beta_num = int(beta[1:]) + 1
        return f"{major}.{minor}.{patch}b{beta_num}"
    #else:
    #    # Append b1 to stable version (e.g., 0.1.51 -> 0.1.51b1)
    #    return f"{major}.{minor}.{patch}b1"


def update_pyproject_version():
    # Read pyproject.toml
    with open("pyproject.toml", "r") as f:
        config = toml.load(f)

    # Get current version
    current_version = config["project"]["version"]
    print(f"Current version: {current_version}")

    # Calculate next beta version
    next_version = get_next_beta_version(current_version)
    if next_version:
        print(f"Next version: {next_version}")

        # Update version in config
        config["project"]["version"] = next_version

        # Ensure beta classifier is set
        classifiers = config["project"].get("classifiers", [])
        if "Development Status :: 4 - Beta" not in classifiers:
            classifiers.append("Development Status :: 4 - Beta")
        config["project"]["classifiers"] = classifiers

        # Write back to pyproject.toml
        with open("pyproject.toml", "w") as f:
            toml.dump(config, f)

        return next_version
    else:
        return current_version


if __name__ == "__main__":
    new_version = update_pyproject_version()
    if new_version:
        print(f"Updated pyproject.toml to version: {new_version}")
    else:
        print(f"No beta version detected. Keeping unchanged: {new_version}")