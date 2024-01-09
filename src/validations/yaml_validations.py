import logging


# the validator of yamles
def config_yamVal(data: dict, log: logging.Logger) -> bool:
    # Validate root attributes
    if "autofat" not in data:
        log.error("Config lacks root: 'autofat'.")
        return False
    else:
        autofat_data = data["autofat"]

        if "network" not in autofat_data:
            log.error("Config lacks 'network' property under root 'autofat'.")
            return False

        if "fat" not in autofat_data:
            log.error("Config lacks 'fat' property under root 'autofat'.")
            return False

    # Network validation
    for node in autofat_data.get("network", []):
        name = node.get("name")

        if "name" not in node:
            log.error("Network segment lacks 'name'.")
            return False

        if "ip" not in node:
            log.error(f"Network segment '{name}' lacks 'ip' configuration.")
            return False

        credentials = node.get("credentials")

        if not credentials:
            log.error(f"Network segment '{name}' lacks 'credentials' configuration.")
            return False
        else:
            if "user" not in credentials:
                log.error(f"Credentials segment for '{name}' lacks 'user'.")
                return False
            if "pwd" not in credentials:
                log.error(f"Credentials segment for '{name}' lacks 'password'.")
                return False

    # FAT validation
    for fat in autofat_data.get("fat", []):
        fat_name = fat.get("name")

        if "name" not in fat:
            log.error("FAT segment lacks 'name'.")
            return False

        if "file" not in fat:
            log.error(f"FAT segment '{fat_name}' lacks 'file' configuration.")
            return False

        if "order" not in fat:
            log.error(f"FAT segment '{fat_name}' lacks 'order' configuration.")
            return False

        if "steps" not in fat:
            log.error(f"FAT segment '{fat_name}' lacks 'steps' configuration.")
            return False

    return True
