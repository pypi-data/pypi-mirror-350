from os.path import (
    exists,
    join,
    dirname,
    basename,
    expanduser,
    isdir
)
import configparser, platform, json, os
import logging

from functools import lru_cache
from pathlib import Path




class Settings:
    # dev utils
    debug = False

    # if path provided leads to a repo upstream
    is_repo      : bool = False
    is_module    : bool = False
    is_ymvas     : bool = False # if repos if fetched from ymvas
    is_main      : bool = False # if repo is main git@ymvas.com/vas/vas.git

    # paths
    root         : str  = None # /root             -> folder of the repo
    git          : str  = None # /root/.git        -> folder , if module -> /root/../../.git
    ymvas        : str  = None # /root/.ymvas      -> folder

    # repo info
    url          : str  = None # example  -> git@ymvas.com/vas/ymvas.git
    name         : str  = None # from url -> ymvas
    user         : str  = None # from url -> vas
    alias        : str  = None # from url -> vas/ymvas

    # ymvas important folders
    d_references : str = None
    d_commands   : str = None
    d_settings   : str = None
    d_tasks      : str = None
    d_schedules  : str = None
    d_secrets    : str = None
    d_finance    : str = None
    d_actions    : str = None
    d_endpoints  : str = None
    d_documents  : str = None
    d_contacts   : str = None
    d_spaces     : str = None

    # where are we going to complie the endpointss
    d_compile_prefix : str = None

    # submodules asociated
    modules: dict = {}

    # ymvas important files
    f_settings            : str = None
    f_settings_endpoints  : str = None
    f_settings_references : str = None
    f_settings_secrets    : str = None
    f_settings_tasks      : str = None
    f_settings_finance    : str = None
    f_settings_actions    : str = None

    d_default_compiles    : str = None

    def __init__( self , pwd ):
        root, is_repo = Settings._find_repo_root(pwd)
        self.__logger = logging.getLogger(__name__)

        self.root = root
        if is_repo:
            self.root = pwd
            self._setup_repo_paths()

        self.is_repo = is_repo

        if not exists( self.f_global_config ):
            os.makedirs(
                dirname( self.f_global_config ),
                exist_ok = True
            )

            with open(self.f_global_config,'w') as fs:
                from .__init__ import __version__

                data = {
                    "version" : __version__ ,
                }

                if self.is_main:
                    data['main']          = self.root
                    data['main-commands'] = self.d_commands

                fs.write(json.dumps(data, indent= 10))
        else:
            with open(self.f_global_config,'r') as fs:
                data = json.loads(fs.read())
                self.d_default_compiles = data.get('global-compile-dir',None)


    def log(self,*args,**kwargs):
        if self.debug:
            print(*args)
        self.__logger.info(*args,**kwargs)

    @property
    @lru_cache(maxsize=None)
    def ymvas_server_url(self):
        stg = self.get_global_settings()
        return str(stg.get(
            'ymvas-server-url',
            'ssh://git@'+self.ymvas_domain+'/{repo}.git'
        ))

    @property
    @lru_cache(maxsize=None)
    def ymvas_domain( self ):
        stg = self.get_global_settings()
        return str(stg.get(
            'ymvas-domain',
            'ymvas.com'
        ))

    @staticmethod
    def _find_repo_root(pwd):
        _pwd_b = pwd

        ymf = join(pwd , '.ymvas' )
        ymp = join(pwd , '.ymvas' )
        git = join(pwd , '.git'   )

        _is_repo = True
        _search  = {}

        while not exists(ymf):
            _pwd_b = dirname(_pwd_b)

            _search[_pwd_b] = _search.get(_pwd_b,0) + 1
            ymf = join(_pwd_b,'.ymvas')

            if _search[_pwd_b] > 10 or exists(git):
                ymf = ymp
                _is_repo = False
                break

            git = join( _pwd_b , '.git'   )
            ymp = join( _pwd_b , '.ymvas' )

        return dirname(ymf), _is_repo


    def _setup_repo_paths( self ):
        _git      = join( self.root , '.git' )
        is_module = not isdir( _git )

        if not exists(_git):
            return

        if is_module:
            with open( _git ,'r' ) as f:
                _git = Path(f.read().split("gitdir:")[1].strip())
                _git = str( Path(self.root) / _git )

        self.git       = _git
        self.is_module = is_module

        ######### config #########
        cnf = configparser.ConfigParser()
        cnf.read( join(_git,'config') )

        _url = None
        for section in cnf.sections():
            if 'origin' in section and 'remote':
                _url = cnf[section].get('url',None)
                break


        user, name, is_ymvas = self._parse_url(_url)

        self.is_ymvas = is_ymvas
        self.user     = user
        self.name     = name
        self.url      = _url


        self.is_main = user == name
        self.alias   = f'{name}'
        if user is not None:
            self.alias = f'{user}/{name}'

        # /repo/.ymvas folders
        self.ymvas = join(self.root, '.ymvas' )

        self.d_references = join( self.ymvas, 'references' )
        self.d_commands   = join( self.ymvas, 'commands'   )
        self.d_settings   = join( self.ymvas, 'settings'   )
        self.d_tasks      = join( self.ymvas, 'tasks'      )
        self.d_schedules  = join( self.ymvas, 'schedules'  )
        self.d_secrets    = join( self.ymvas, 'secrets'    )
        self.d_finance    = join( self.ymvas, 'finance'    )
        self.d_actions    = join( self.ymvas, 'actions'    )
        self.d_endpoints  = join( self.ymvas, 'endpoints'  )

        # /repo folders if account
        if self.is_main:
            self.d_endpoints = join(self.root, 'endpoints' )
            self.d_documents = join(self.root, 'documents' )
            self.d_contacts  = join(self.root, 'contacts'  )
            self.d_finance   = join(self.root, 'finance'   )
            self.d_spaces    = join(self.root, 'spaces'    )

        # ymvas endpoints paths
        self.d_compile_prefix = self.alias
        if self.is_main:
            self.d_compile_prefix = user

        self.modules   = self.get_modules()

        # sttings files
        self.f_settings            = join(self.d_settings, 'settings.yaml'   )
        self.f_settings_endpoints  = join(self.d_settings, 'endpoints.yaml'  )
        self.f_settings_references = join(self.d_settings, 'references.yaml' )
        self.f_settings_secrets    = join(self.d_settings, 'secrets.yaml'    )
        self.f_settings_tasks      = join(self.d_settings, 'tasks.yaml'      )
        self.f_settings_finance    = join(self.d_settings, 'finance.yaml'    )
        self.f_settings_actions    = join(self.d_settings, 'actions.yaml'    )
        self.f_settings_schedules  = join(self.d_settings, 'schedules.yaml'  )



    def get_modules(self):
        file = join(self.root,'.gitmodules')

        if self.is_module:
            modules = join(".git","modules")
            fragment = modules + self.git.split(modules)[-1]
            main_path = self.git.replace(fragment,"")
            main_settings = Settings(main_path)
            return main_settings.get_modules()

        modules = {
            self.alias : {
                "root"   : True,
                "active" : True,
                "path"   : self.root ,
                "url"    : self.url  ,
                "name"   : self.name ,
                "user"   : self.user ,
            }
        }

        if not exists(file):
            return []

        cnf = configparser.ConfigParser()
        cnf.read( file )

        for s in cnf.sections():
            p = cnf[s].get('path'   , None )
            u = cnf[s].get('url'    , None )
            a = cnf[s].get('active' , 'True' ).lower().strip() == 'true'

            if not 'submodule' in s or p is None or u is None:
                continue

            user, name, is_ymvas = self._parse_url(u)
            if name is None:
                continue

            modules[f"{user}/{name}"] = {
                "root"   : False,
                "active" : a,
                "path"   : join( self.root , p ),
                "url"    : u     ,
                "name"   : name  ,
                "user"   : user  ,
            }

        return modules

    @property
    @lru_cache(maxsize=None)
    def p_global_config(self):
        system = platform.system()
        shell   = os.environ.get("SHELL", "")
        msystem = os.environ.get("MSYSTEM", "")

        # Detect Git Bash on Windows
        is_windows_git_bash = (system == "Windows") and (
            "bash" in shell or msystem.startswith("MINGW")
        )

        if is_windows_git_bash:
            _dir = expanduser("~/.config")
        elif system == "Windows":
            _dir = os.environ.get("APPDATA", expanduser("~\\AppData\\Roaming"))
        elif system == "Darwin":  # macOS
            _dir = expanduser("~/Library/Application Support")
        else:  # Linux and other Unix-like systems
            _dir = os.environ.get("XDG_CONFIG_HOME", expanduser("~/.config"))
        return join(_dir, 'ymvas')

    @property
    @lru_cache(maxsize=None)
    def f_global_config(self):
        return join(self.p_global_config, 'config.json')

    @lru_cache(maxsize=None)
    def get_global_settings(self):
        if not exists(self.f_global_config):
            return {}
        try:
            with open(self.f_global_config,'r') as f:
                return json.loads( f.read() )
        except Exception as e:
            print(e)
            return {}
        return {}

    def set_global_settings(self,stg):
        with open(self.f_global_config,'w') as fs:
            fs.write(json.dumps(stg))

    def _parse_url(self, url ):
        if url is None:
            return None, None, None

        is_ymvas = f"@{self.ymvas_domain}" in url
        name = basename(url).replace('.git','')

        # get repo user
        user1 = url.split('@')[-1]
        user  = user1.replace(basename(url),'')
        user  = basename(user.strip('/'))
        user  = user.split(':')[-1]
        user  = user.strip('/')
        user  = user if '/' not in user else None

        if user is not None:
            user  = None if user1.startswith( user ) else user

        return user, name, is_ymvas
