from pathlib import Path

from os.path import join, exists, dirname, isfile, isdir
import sys, os, yaml, json

from .references import Ref
from .settings   import Settings
from .compiler   import Compiler
from .templates.creator import Creator


class Operator:
    _refs  :dict = {}
    _spaces:dict = {}

    def __init__(self, pwd , debug = False):
        self.settings = Settings(pwd)
        self.settings.debug = debug

    def command(self,args):

        commands_path = self.settings.d_commands
        if args.is_global or not self.settings.is_repo:
            commands_path = self.settings.get_global_settings().get(
                'main-commands',None
            )

            if commands_path is None:
                print("Global commands are not setup!")
                return

        # widnows git bash fixes
        commands_path = Path(commands_path)
        if str(commands_path).startswith("/c/") or \
           str(commands_path).startswith("\\c\\"):
            commands_path = Path("C:" + str(commands_path)[2:])

        if not commands_path.exists():
            print(f'Commands [.ymvas/commands/example.bash] is not setup for this repository!')
            return

        valid = [
            {"ext" : 'py'   , "run" : "python3" },
            {"ext" : 'bash' , "run" : "bash"    },
            {"ext" : 'sh'   , "run" : "sh"      },
        ]

        found = False
        for t in valid:
            ext  = t['ext']
            run  = t['run']

            file = join(commands_path,f"{args.command}.{ext}")

            if exists(file):
                found = True
                os.system(f'{run} {file}')

        if not found:
            raise Exception(f'Command [{args.command}] is not setup for this repository!')


    def clone(self,args):
        if args.repo is None:
            print('No repo specified!')
            return

        url = self.settings.ymvas_server_url.format(
            repo = args.repo
        )

        os.system(f"git clone {url}")

    def pull(self,argv):
        modules = self.settings.get_modules()
        modules = {k:v for k,v in modules.items() if not v['root'] and v['active']}

        os.system(
            f"git --git-dir={self.settings.git} "
            f"--work-tree={self.settings.root} fetch"
        )

        # for k,v in modules.items():
        #     p = v[ 'path' ]
        #     u = v[ 'url'  ]
        #
        #     if not exists(p):
        #         os.system(
        #             f"cd {self.settings.root} && "
        #             f"git --git-dir={self.settings.git} "
        #             f"--work-tree={self.settings.root} "
        #             f"submodule add {u} {p}"
        #         )


    def setup(self,argv):
        creator = Creator(argv)
        creator.run()

    def config(self,argv,args):
        if argv.action == 'set' and argv.is_global:
            stg = self.settings.get_global_settings()
            for a in args:
                if '=' not in a:
                    continue
                k = a.split('=')[0]
                v = a.replace(k+'=','').strip()

                if v == '':
                    continue
                k = k.strip('--')
                stg[k] = v
            self.settings.set_global_settings(stg)
            print(stg)
        elif argv.action == "show" and argv.is_global:
            print(self.settings.get_global_settings())

        elif argv.action == "get" and argv.is_global:
            for a in args:
                v = self.settings.get_global_settings().get(a,None)
                if v is None: continue
                print(v)

    def compile(self,args):
        if not exists(self.settings.d_endpoints):
            return

        self._append_refs(
            self.settings.alias,
            self.settings.d_references
        )

        self._spaces = self.settings.get_modules()
        Compiler( self , args ).run()

    def _append_refs(self, space, pref ):
        self._refs[space] = []

        if not exists(pref):
            return

        for r,_,files in os.walk( pref ):
            for f in files:
                self._refs[space].append(
                    Ref(join(r,f), self , space )
                )

        pass


    def refs(self,needle = None):
        if needle == None:
            for r in self._refs[self.alias]:
                yield r
            return

        for r in self._refs[self.alias]:
            fpath = r.fpath.replace(self.ref,'')
            if needle in fpath:
                yield r

    def __repr__(self):
        return "\n".join([
            f"config  : {self.settings.f_global_config}" ,
            "",
            f"[{self.settings.alias}]",
            f" - is-repo  : {self.settings.is_repo}",
            f" - is-ymvas : {self.settings.is_ymvas}",
            f" - is-main  : {self.settings.is_main}",
        ]) + "\n"
