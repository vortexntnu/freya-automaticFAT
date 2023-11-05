import logging


# the validator of yamles
def config_yamVal(data: dict | list, log: logging.Logger) -> bool:
    # Validate root attributes
    if not any(key == "autofat" for key, _ in data.items()):
        log.error = "Config lacks root: autofat."
        return False
    else:
        if not any(key == "network" for key, _ in data["autofat"].items()):
            log.error = "Config lacks network property under root autofat."
            return False
        if not any(key == "fat" for key, _ in data["autofat"].items()):
            log.error = "Config lacks fat property under root autofat."
            return False

    # network validation
    for node in data["autofat"]["network"]:
        if not any(key == "name" for key, _ in node.items()):
            log.error = "Network segment lacks name."
            return False
        else:
            name = node["name"]

        if not any(key == "ip" for key, _ in node.items()):
            log.error = "Network segment " + name + " lacks ip config."
            return False
        
        if not any(key == "credientials" for key, _ in node.items()):
            log.error = "Network segment " + name + " lacks credientials config."
            return False
        else:
            if not any(key == "user" for key, _ in node["credientials"].items()):
                log.error = "Credientials segment for " + name + " lacks user."
                return False
            if not any(key == "pwd" for key, _ in node["credientials"].items()):
                log.error = "Credientials segment for " + name + " lacks password."
                return False

    return True