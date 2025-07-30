from Ecida import EcidaModule
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_module() -> EcidaModule:
    M = EcidaModule("MODULE_NAME", "v0.1.0")
    M.add_description("FILL IN THE MODULE DESCRIPTION")
    # ADD MODULE INPUTS/OUTPUTS HERE

    return M


def main(M: EcidaModule):
    print(f"START MODULE {M.name}:{M.version}")
    # LOGIC COMES HERE


if __name__ == "__main__":
    M = create_module()
    M.initialize()
    main(M)
