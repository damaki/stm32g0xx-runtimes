# This script extends bb-runtimes to define the stm32g0xx target

import sys
import os
import pathlib

# Add bb-runtimes to the search path so that we can include and extend it
sys.path.append(str(pathlib.Path(__file__).parent / "bb-runtimes"))

import arm.cortexm
import build_rts
from support import add_source_search_path


class Stm32G0(arm.cortexm.CortexM0P):
    @property
    def name(self):
        return "stm32g0xx"

    @property
    def use_semihosting_io(self):
        return True

    @property
    def loaders(self):
        return ("ROM", "RAM")

    @property
    def system_ads(self):
        return {
            "light": "system-xi-arm.ads",
            "light-tasking": "system-xi-armv6m-sfp.ads",
            "embedded": "system-xi-armv6m-full.ads",
        }

    def __init__(self):
        super(Stm32G0, self).__init__()

        self.add_linker_script("stm32g0_src/ld/common-RAM.ld")
        self.add_linker_script("stm32g0_src/ld/common-ROM.ld")

        # Common source files
        self.add_gnat_sources(
            "stm32g0_src/start-rom.S",
            "stm32g0_src/start-ram.S",
            "stm32g0_src/setup_pll.ads",
            "stm32g0_src/setup_pll.adb",
            "stm32g0_src/s-bbpara.ads",
            "stm32g0_src/s-bbbopa.ads",
            "stm32g0_src/s-bbmcpa.ads",
            "stm32g0_src/svd/i-stm32.ads",
            "stm32g0_src/svd/i-stm32-flash.ads",
            "stm32g0_src/svd/i-stm32-rcc.ads",
        )

        self.add_gnarl_sources(
            "src/s-bbbosu__armv6m.adb",
            "src/s-bcpcst__pendsv.adb",
            "stm32g0_src/svd/a-intnam-g0x0.ads",
            "stm32g0_src/svd/a-intnam-g0x1.ads",
        )


def build_configs(target):
    if target == "stm32g0xx":
        return Stm32G0()
    else:
        assert False, "unexpected target: %s" % target

def patch_bb_runtimes():
    """Patch some parts of bb-runtimes to use our own targets and data"""
    add_source_search_path(os.path.dirname(__file__))

    build_rts.build_configs = build_configs

if __name__ == "__main__":
    patch_bb_runtimes()
    build_rts.main()