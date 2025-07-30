import sys
import ka_uts_com.dec as dec
from ka_uts_com.com import Com
from ka_app_cfg.parms import Parms
from ka_app_cfg.task import Task


class Do:

    @classmethod
    @dec.handle_error
    @dec.timer
    def do(cls) -> None:
        Task.do(Com.sh_kwargs(cls, Parms.d_eq, sys.argv))


if __name__ == "__main__":
    Do.do()
