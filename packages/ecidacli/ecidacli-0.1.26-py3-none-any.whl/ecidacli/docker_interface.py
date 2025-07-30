import os
import requests
from packaging import version
import requests.auth

DOCKER_REGISTRY = "https://registry-1.docker.io"


def parse_image_name(image_name: str) -> tuple[str, str]:
    """Parses the image name to extract the registry (if any) and the repository name.

    Args:
        image_name (str): The image name in full format, for example, 'my-registry.com/this/image'.

    Returns:
        tuple[str, str]: registry URL, repository name.
    """

    if ":" in image_name or "." in image_name.split("/")[0]:
        # Assume Custom or local registry
        registry_host = image_name.split("/")[0]
        registry = f"http://{registry_host}"
        repository = "/".join(image_name.split("/")[1:])
    else:
        # Assume Docker Hub
        registry = DOCKER_REGISTRY
        repository = image_name

    return registry, repository


def get_credentials() -> tuple[str, str]:
    """
    Retrieves Docker credentials from environment variables [REGISTRY_USERNAME,REGISTRY_PASSWORD].
    """
    username = os.environ.get("REGISTRY_USERNAME")
    password = os.environ.get("REGISTRY_PASSWORD")
    return username, password


def authenticate_docker_hub(
    repository, username, password
) -> tuple[dict[str, str], ValueError]:
    """
    Authenticates with Docker Hub and retrieves a token.

    returns:
        Header (dict[str,str])
        Error (ValueError)
    """
    auth_url = "https://auth.docker.io/token"
    service = "registry.docker.io"
    scope = f"repository:{repository}:pull"
    params = {"service": service, "scope": scope}

    auth = (username, password) if username and password else None

    try:
        response = requests.get(auth_url, params=params, auth=auth)
        if response.status_code == 401:
            return None, ValueError("Unauthorized: Check your Docker credentials.")
        response.raise_for_status()
        token = response.json().get("token")
        if not token:
            return None, ValueError("Token not found in the authentication response.")
        headers = {"Authorization": f"Bearer {token}"}
        return headers, None
    except requests.exceptions.RequestException as e:
        return None, ValueError(f"Failed to fetch token: {e}")


def authenticate_custom_registry(username, password) -> dict[str, str]:
    """
    Authenticates with a custom registry using Basic authentication.
    returns:
        Header (dict[str,str])
    """
    if username and password:
        auth_str = requests.auth._basic_auth_str(username, password)
        headers = {"Authorization": auth_str}
        return headers
    return {}


def fetch_tags(registry_url, repository, headers) -> tuple[list, ValueError]:
    """
    Fetches the list of tags from the registry.
    """
    tags_url = f"{registry_url}/v2/{repository}/tags/list"
    try:
        response = requests.get(tags_url, headers=headers, verify=True)
        if response.status_code == 401:
            return None, ValueError(
                "Unauthorized: Check your Docker credentials or registry permissions."
            )
        response.raise_for_status()
        tags = response.json().get("tags", [])
        if not tags:
            return None, ValueError("No tags found for the image.")
        return tags, None
    except requests.exceptions.RequestException as e:
        return None, ValueError(f"Failed to fetch tags: {e}")
    except ValueError:
        return None, ValueError("Invalid JSON response while fetching tags.")


def latest_semver_tags(tags) -> str:
    """
    Filters and sorts tags based on semantic versioning.

    returns:
        tag(str): the latest tag in semantic versioning.
    """
    semver_tags = []
    for tag in tags:
        try:
            semver = version.parse(tag.lstrip("v"))
            semver_tags.append((semver, tag))
        except version.InvalidVersion:
            continue  # Ignore tags that aren't semantic versions

    if semver_tags:
        sorted_tags = sorted(semver_tags, key=lambda x: x[0], reverse=True)
        return sorted_tags[0][1]
    return None


def determine_latest_tag(tags) -> str:
    """
    Determines the latest tag from the list of tags.

    returns:
        tag(str): latest tag either semantic or lexicographical
    """
    latest_tag = latest_semver_tags(tags)
    if latest_tag:
        return latest_tag
    # Fallback to lexicographical sorting
    return sorted(tags, key=lambda x: x.lower())[-1]


def fetch_latest_tag(image_name: str) -> tuple[str, ValueError]:
    """
    Fetches the latest tag of the given Docker image.

    Works with:
    - Public Docker Hub repositories
    - Private Docker Hub repositories (requires authentication)
    - Custom/private registries (authentication depends on the registry's setup)
    args:
        image_name (str): The image name in full format, for example, 'my-registry.com/this/image'.

    returns:
        latest_tag (str)
    """
    registry_url, repository = parse_image_name(image_name)

    username, password = get_credentials()
    headers = {}

    if registry_url == DOCKER_REGISTRY:
        headers, error = authenticate_docker_hub(repository, username, password)
        if error:
            return None, error
    else:
        headers = authenticate_custom_registry(username, password)

    tags, error = fetch_tags(registry_url, repository, headers)
    if error:
        return None, error

    latest_tag = determine_latest_tag(tags)
    if not latest_tag:
        return None, ValueError("No valid semantic version tags found.")

    return latest_tag, None


def increment_tag(tag: str) -> tuple[str, ValueError]:
    """
    Increments the latest semantic version tag.

    args:
        tag (str): The latest tag in semantic versioning format.

    returns:
        The incremented tag (str)
        Error (ValueError)
    """
    try:
        # Remove any leading 'v'
        clean_tag = tag.lstrip("v")
        semver = version.parse(clean_tag)
        if not isinstance(semver, version.Version):
            raise ValueError

        # Increment the patch version
        new_version = version.Version(
            f"{semver.major}.{semver.minor}.{semver.micro + 1}"
        )
        return f"v{new_version}", None
    except Exception:
        return None, ValueError(f"Invalid tag format: {tag}")


if __name__ == "__main__":
    # Example usage:
    # image_name = 'ecida/producer'  # Docker Hub
    # image_name = 'localhost:32000/producer'  # Local registry
    # image_name = 'your-registry.com/your-image'  # Custom registry

    image_name = "ecida/producer"  # Replace with your image name
    latest_tag, err = fetch_latest_tag(image_name)
    print(f'Latest tag for "{image_name}": {latest_tag}')
    if err is None:
        incremented_tag, err = increment_tag(latest_tag)
        if err is None:
            print(f"Incremented tag: {incremented_tag}")
        else:
            print(err)
    else:
        print(err)
