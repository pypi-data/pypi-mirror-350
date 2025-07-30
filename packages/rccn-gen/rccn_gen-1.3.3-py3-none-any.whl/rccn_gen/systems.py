from yamcs.pymdb import *
import shutil
import difflib
import datetime
from caseconverter import *
from importlib.resources import files
from .utils import *
from collections.abc import Mapping, Sequence
from typing import Union, Any, Literal
from yamcs.pymdb.alarms import EnumerationAlarm, ThresholdAlarm
from yamcs.pymdb.alarms import EnumerationContextAlarm, ThresholdContextAlarm
from yamcs.pymdb.datatypes import Epoch, Member, DataType, DynamicInteger
from yamcs.pymdb.encodings import Encoding, TimeEncoding
from yamcs.pymdb.calibrators import Calibrator
from yamcs.pymdb.parameters import (
    AbsoluteTimeParameter, AggregateParameter, ArrayParameter,
    BinaryParameter, BooleanParameter, DataSource,
    EnumeratedParameter, FloatParameter, IntegerParameter, Parameter,
    StringParameter
)
from yamcs.pymdb.commands import Command, CommandLevel, CommandEntry, Argument, TransmissionConstraint

class Application(Subsystem):
    """
    A PUS application.
    
    This class represents a Protocol Utilization Standard (PUS) application in the context 
    of space systems. It extends the Subsystem class of pymdb and provides functionality for managing 
    services, generating Rust code for the application, and handling snapshots and diffs of 
    the generated code.
    
    The Application class is responsible for creating and organizing the directory structure 
    for Rust code generation, managing services and their associated commands and telemetry,
    and facilitating the generation of Rust code files for the entire application.
    """
    def __init__(
        self,
        system: System,
        name: str,
        apid: int,
        vcid: int = 0,
        export_directory = '.',
        snapshot_directory = './.rccn_snapshots',
        diff_directory = './.rccn_diffs',
        snapshots = True,
        *args,
        **kwargs
    ):
        """
        Initialize a new PUS application.
        
        Parameters:
        -----------
        system : System
            The parent system that this application belongs to.
        name : str
            The name of the application.
        apid : int
            The Application Process ID (APID) for this application.
        vcid : int, optional
            The Virtual Channel ID (VCID) for this application. Default is 0.
        export_directory : str, optional
            The directory where generated Rust code will be exported. Default is current directory.
        snapshot_directory : str, optional
            The directory where snapshots of generated code will be stored. Default is './.rccn_snapshots'.
        diff_directory : str, optional
            The directory where diffs between generated code versions will be stored. Default is './.rccn_diffs'.
        snapshots : bool, optional
            Whether to create snapshots of generated code. Default is True.
        *args, **kwargs
            Additional arguments and keyword arguments passed to the parent class constructor.
        """
        super().__init__(system=system, name=name, *args, **kwargs)

        self.apid = apid
        self.vcid = vcid
        self.export_directory = export_directory
        system._subsystems_by_name[name] = self
        self.snapshot_directory = snapshot_directory
        self.snapshot_generated_file_path = os.path.join(snapshot_directory, 'auto_generated')
        self.diff_directory = diff_directory
        self.text_modules_path = files('rccn_gen').joinpath('text_modules')
        self.text_modules_main_path = os.path.join(self.text_modules_path, 'main')
        self.snapshots = snapshots
        self.keep_snapshots = 10
    
    def add_service(self, service):
        """
        Add a service to this application.
        
        Parameters:
        -----------
        service : Service
            The service to add to this application.
            
        Raises:
        -------
        TypeError
            If the provided service is not an instance of Service.
        """
        if not isinstance(service, Service):
            raise TypeError('Service '+service.name+' is not a RCCNCommand.')
        service.add_to_application(self)

    def create_and_add_service(
            self,
            name: str,
            service_id: int,
            aliases: Mapping[str, str] | None = None,
            short_description: str | None = None,
            long_description: str | None = None,
            extra: Mapping[str, str] | None = None,
            *args, 
            **kwargs
    ):
        """
        Create a new service and add it to this application.
        
        Parameters:
        -----------
        name : str
            The name of the service.
        service_id : int
            The service ID.
        aliases : Mapping[str, str], optional
            Alternative names for the service, keyed by namespace.
        short_description : str, optional
            A short description of the service.
        long_description : str, optional
            A longer description of the service.
        extra : Mapping[str, str], optional
            Arbitrary information about the service, keyed by name.
        *args, **kwargs
            Additional arguments and keyword arguments passed to the Service constructor.
            
        Raises:
        -------
        ValueError
            If 'system' is provided in kwargs.
        """
        if 'system' not in kwargs:
            kwargs['system'] = self
        else:
            raise ValueError('RCCN-Error: \'create_and_add_service\' function can not be called with a \'system\' argument.')
        Service(
            name=name, 
            service_id=service_id, 
            aliases=aliases, 
            short_description=short_description, 
            long_description=long_description, 
            *args, 
            **kwargs
        )

    def file_paths(self):
        """
        Get the file paths for various files used by this application.
        
        Returns:
        --------
        dict
            A dictionary mapping file types to their absolute paths.
        """
        paths = {
            'main': os.path.join(self.export_directory, 'rccn_usr_'+snakecase(self.name), 'src', 'main.rs'),
            'main_generated_snapshot': os.path.join(self.snapshot_directory, 'generated', 'rccn_usr_'+snakecase(self.name), 'src', 'main.rs'),
            'main_user_snapshot': os.path.join(self.user_snapshot_path(), 'rccn_usr_'+snakecase(self.name), 'src', 'main.rs'),
            'main_diff': os.path.join(self.diff_directory, 'rccn_usr_'+snakecase(self.name), 'src', 'main.diff'),
            'main_template': os.path.join(self.text_modules_main_path, 'main.txt'),
            'cargo_toml': os.path.join(self.export_directory, 'rccn_usr_'+snakecase(self.name), 'Cargo.toml'),
            'cargo_toml_template': os.path.join(self.text_modules_path, 'cargo_toml', 'cargo.txt'),
            'cargo_toml_generated_snapshot': os.path.join(self.snapshot_directory, 'generated', 'rccn_usr_'+snakecase(self.name), 'cargo.toml'),
            'cargo_toml_user_snapshot': os.path.join(self.user_snapshot_path(), 'rccn_usr_'+snakecase(self.name), 'cargo.toml'),
            'cargo_toml_diff': os.path.join(self.diff_directory, 'rccn_usr_'+snakecase(self.name), 'cargo.diff'),
        }
        return paths

    def user_snapshot_path(self):
        """
        Get the path for user snapshots with current timestamp.
        
        Returns:
        --------
        str
            The path where user snapshots are stored.
        """
        return os.path.join(self.snapshot_directory, 'user', datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

    def services(self):
        """
        Get all services belonging to this application.
        
        Returns:
        --------
        list[Service]
            A list of Service objects that are subsystems of this application.
        """
        return [subsystem for subsystem in self.subsystems if isinstance(subsystem, Service)]

    def create_rccn_directories(self):
        """
        Create directory structure for Rust code generation.
        
        Creates the necessary directory structure for the application and its services
        in the export directory.
        """
        app_src_dir = os.path.join(self.export_directory, 'rccn_usr_'+snakecase(self.name), 'src')
        if not os.path.exists(app_src_dir):
            os.makedirs(app_src_dir)
        for service in self.services():
            service_dir = os.path.join(app_src_dir, snakecase(service.name))
            if not os.path.exists(service_dir):
                os.makedirs(service_dir)

    def generate_rccn_main_file(self):
        """
        Generate the main.rs file for the application.
        
        Performs several tasks:
        1. Creates diff file if both current and snapshot files exist
        2. Creates snapshot of current main.rs with user changes if snapshots are enabled
        3. Generates new main.rs file from template
        4. Creates snapshot of newly generated main.rs if snapshots are enabled
        5. Applies user changes from diff file if rebase_changes is enabled
        """
        # Create main.diff file
        if os.path.exists(self.file_paths()['main']) and os.path.exists(self.file_paths()['main_generated_snapshot']):
            os.makedirs(os.path.dirname(self.file_paths()['main_diff']), exist_ok=True)
            self.generate_diff_file('main', 'main_generated_snapshot', 'main_diff')
        # Create snapshot of main.rs with user changes if instructed
        if self.snapshots and os.path.exists(self.file_paths()['main']):
            self.generate_snapshot('main', 'main_user_snapshot')
        # Generate main.rs file
        with open(self.file_paths()['main_template'], 'r') as file:
            main_template_text = file.read()
        with open(self.file_paths()['main'], 'w') as file:
            new_main_text = self.find_and_replace_keywords(main_template_text)
            file.write("".join(new_main_text))
        # Create snapshot of newly generated main.rs if instructed
        if self.snapshots:
            self.generate_snapshot('main', 'main_generated_snapshot')
        # Rebase main.diff on main.rs if instructed
        if self.rebase_changes and os.path.exists(self.file_paths()['main_diff']):
            os.system('patch '+self.file_paths()['main']+' <  '+self.file_paths()['main_diff'])
    
    def find_and_replace_keywords(self, text):
        """
        Replace template keywords with actual values.
        
        Parameters:
        -----------
        text : str
            Template text containing keywords to be replaced.
            
        Returns:
        --------
        str
            Text with all keywords replaced with actual values.
            
        Raises:
        -------
        KeyError
            If a keyword in the template text is not found in the translation dictionary.
        """
        # Call keyword replacement for all associated services (Later, there needs to be checking to account for user changes to the generated files)
        for service in self.services():
            text = service.find_and_replace_keywords(text, self.text_modules_main_path)
        # Find and replace service variable keywords
        var_translation = {
            '<<VAR_APID>>':str(self.apid),
            '<<VAR_VCID>>':str(self.vcid),
            '<<VAR_APP_NAME_SCASE>>':snakecase(self.name),
        }
        var_keywords = get_var_keywords(text)
        for var_keyword in var_keywords:
            if var_keyword in var_translation.keys():
                text = text.replace(var_keyword, var_translation[var_keyword])
            else:
                raise KeyError('Keyword '+var_keyword+' is not in translation dictionary.')
        text = delete_all_keywords(text)
        return text 
    
    def generate_rccn_code(self, export_directory:str, snapshot_directory='', diff_directory='', rebase_changes=True, check=True):
        """
        Generate Rust code for the application and its services.
        
        Parameters:
        -----------
        export_directory : str
            Directory where the generated code will be exported.
        snapshot_directory : str, optional
            Directory where snapshots of generated code will be stored. Default is a subdirectory of export_directory.
        diff_directory : str, optional
            Directory where diffs between generated code versions will be stored. Default is a subdirectory of export_directory.
        rebase_changes : bool, optional
            Whether to apply user changes from diff files. Default is True.
        check : bool, optional
            Whether to perform checks on user input. Default is True.
        """
        # Update export, snapshot and diff directory for the Application and all Services
        self.export_directory = export_directory
        if snapshot_directory == '':
            snapshot_directory = os.path.join(self.export_directory, '.rccn-snapshots')
        if diff_directory == '':
            diff_directory = os.path.join(self.export_directory, '.rccn-diffs')
        self.snapshot_directory = snapshot_directory
        self.diff_directory = diff_directory
        for service in self.services():
            service.export_directory = self.export_directory
            service.diff_directory = self.diff_directory
            service.snapshot_directory = self.snapshot_directory
        
        if check:
            self.check_user_input()
        self.rebase_changes = rebase_changes
        self.create_rccn_directories()
        self.generate_rccn_main_file()
        self.generate_rccn_main_file()
        if not os.path.exists(self.file_paths()['cargo_toml']):
            self.generate_cargo_toml_file()
        for service in self.services():
            service.export_directory = self.export_directory
            service.generate_rccn_service_file()
            if not os.path.exists(service.file_paths()['mod']):
                service.generate_mod_file()
            service.generate_telemetry_file()
            service.generate_rccn_command_file(os.path.join(self.export_directory, 'rccn_usr_'+snakecase(self.name), 'src'), os.path.join(self.text_modules_path, 'command'))
        self.delete_old_snapshots()

    def generate_snapshot(self, current_file_reference, snapshot_file_reference):
        """
        Create a snapshot of a file.
        
        Parameters:
        -----------
        current_file_reference : str
            Reference to the current file in the file_paths dictionary.
        snapshot_file_reference : str
            Reference to the snapshot file in the file_paths dictionary.
        """
        os.makedirs(os.path.dirname(self.file_paths()[snapshot_file_reference]), exist_ok=True)
        shutil.copyfile(self.file_paths()[current_file_reference], self.file_paths()[snapshot_file_reference])
    
    def generate_diff_file(self, current_file_reference, snapshot_file_reference, diff_file_reference):
        """
        Generate a diff file between current and snapshot files.
        
        Parameters:
        -----------
        current_file_reference : str
            Reference to the current file in the file_paths dictionary.
        snapshot_file_reference : str
            Reference to the snapshot file in the file_paths dictionary.
        diff_file_reference : str
            Reference to the diff file in the file_paths dictionary.
        """
        with open(self.file_paths()[current_file_reference], 'r') as current_file:
            current_text = current_file.readlines()
        with open(self.file_paths()[snapshot_file_reference], 'r') as snapshot_file:
            snapshot_text = snapshot_file.readlines()
        diff = difflib.unified_diff(snapshot_text, current_text, fromfile='snapshot', tofile='current')
        diff_text = ''.join(diff)
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.file_paths()[diff_file_reference], 'w') as diff_file:
            diff_file.write(diff_text)
    
    def delete_old_snapshots(self):
        """
        Delete old user snapshots exceeding the keep_snapshots limit.
        """
        if os.path.exists(os.path.join(self.snapshot_directory, 'user')):
            user_snapshots_path = os.path.join(self.snapshot_directory, 'user')
            snapshots = [os.path.join(user_snapshots_path, d) for d in os.listdir(user_snapshots_path) if os.path.isdir(os.path.join(user_snapshots_path, d))]
            snapshots.sort(key=os.path.getctime)
            while len(snapshots) > self.keep_snapshots:
                shutil.rmtree(snapshots.pop(0))
    
    def check_user_input(self):
        """
        Perform checks on user input to ensure consistency and uniqueness.
        
        Raises:
        -------
        ValueError
            If there are duplicate service names, service IDs, command names, or command subtypes.
        """
        # Check if all services in the application have unique names
        service_names = [service.name for service in self.services()]
        if len(service_names) != len(set(service_names)):
            raise ValueError('RCCN-Error: App \''+self.name+'\' has multiple services with the same name.')
        
        # Check if all services in the application have unique service_ids
        service_ids = [service.service_id for service in self.services()]
        if len(service_ids) != len(set(service_ids)):
            raise ValueError('RCCN-Error: App \''+self.name+'\' has multiple services with the same ID.')
        
        # Check if all commands in each service have unique names
        for service in self.services():
            command_names = []
            command_names += [command.name for command in service.rccn_commands()]
            if len(command_names) != len(set(command_names)):
                raise ValueError('RCCN-Error: Service \''+service.name+'\' has multiple commands with the same name.')
        
        # Check if all commands in each service have unique subtypes
        for service in self.services():
            command_subtypes = []
            command_subtypes += [command.assignments['subtype'] for command in service.rccn_commands()]
            if len(command_subtypes) != len(set(command_subtypes)):
                raise ValueError('RCCN-Error: Service \''+service.name+'\' has multiple commands with the same subtype.')
        
    def generate_cargo_toml_file(self):
        """
        Generate the cargo.toml file for the application.
        
        Performs several tasks:
        1. Creates diff file if both current and snapshot files exist
        2. Creates snapshot of current main with user changes if snapshots are enabled
        3. Generates new cargo.toml file from template
        4. Creates snapshot of newly generated main if snapshots are enabled
        5. Applies user changes from diff file if rebase_changes is enabled
        """
        # Create cargo_toml.diff file
        if os.path.exists(self.file_paths()['cargo_toml']) and os.path.exists(self.file_paths()['cargo_toml_generated_snapshot']):
            os.maked(os.path.dirname(self.file_paths()['cargo_toml_diff']), exist_ok=True)
            self.generate_diff_file('cargo_toml', 'cargo_toml_generated_snapshot', 'cargo_toml_diff')
        # Create snapshot of cargo_toml with user changes if instructed
        if self.snapshots and os.path.exists(self.file_paths()['cargo_toml']):
            self.generate_snapshot('cargo_toml', 'cargo_toml_user_snapshot')
        # Generate cargo_toml file
        with open(self.file_paths()['cargo_toml_template'], 'r') as file:
            cargo_toml_template_text = file.read()
        with open(self.file_paths()['cargo_toml'], 'w') as file:
            new_cargo_toml_text = self.find_and_replace_keywords(cargo_toml_template_text)
            file.write("".join(new_cargo_toml_text))
        # Create snapshot of newly generated cargo_toml if instructed
        if self.snapshots:
            self.generate_snapshot('cargo_toml', 'cargo_toml_generated_snapshot')
        # Rebase cargo_toml.diff on cargo_toml if instructed
        if self.rebase_changes and os.path.exists(self.file_paths()['cargo_toml_diff']):
            os.system('patch '+self.file_paths()['cargo_toml']+' <  '+self.file_paths()['cargo_toml_diff'])


class Service(Subsystem):
    """
    A PUS service that belongs to an Application.
    
    This class represents a Protocol Utilization Standard (PUS) service, which is a collection of 
    related functionality within a space application. It extends the Subsystem class of pymdb and provides 
    functionality for managing commands, telemetry containers, and generating Rust code.
    
    Each service has a unique service ID within its parent application and is responsible for
    organizing related commands and telemetry into logical groups. The class facilitates the 
    generation of Rust code files for the service: service.rs, command.rs, and telemetry.rs.
    """
    def __init__(
        self,
        name: str,
        service_id: int,
        *args,
        **kwargs
    ):
        """
        Initialize a new PUS service.
        
        Parameters:
        -----------
        name : str
            The name of the service.
        service_id : int
            The unique service ID for this service within its parent application.
        *args, **kwargs
            Additional arguments and keyword arguments passed to the parent class constructor.
            A 'system' parameter can be provided if the service is being created directly.
        """
        self.init_args = args
        self.init_kwargs = kwargs
        self.init_args = args
        self.init_kwargs = kwargs
        self.name = name
        self.service_id = service_id
        self.text_modules_path = files('rccn_gen').joinpath('text_modules')
        self.text_modules_service_path = os.path.join(self.text_modules_path, 'service')
        self.text_modules_command_path = os.path.join(self.text_modules_path, 'command')
        self.text_modules_telemetry_path = os.path.join(self.text_modules_path, 'telemetry')
        if 'system' in kwargs and isinstance(kwargs['system'], Application):
            self.add_to_application(kwargs['system'])
    
    def add_to_application(self, application):
        """
        Add this service to an Application.
        
        This method initializes the Service as a Subsystem and sets it as a child
        of the provided application.
        
        Parameters:
        -----------
        application : Application
            The parent application that this service will belong to.
        """
        if 'system' in self.init_kwargs and isinstance(self.init_kwargs['system'], Application):
            super().__init__(
                name=self.name,
                *self.init_args, **self.init_kwargs
            )
        else:
            super().__init__(
                system=application,
                name=self.name,
                *self.init_args, **self.init_kwargs
            )
        self.snapshots = self.system.snapshots
    
    def add_container(self, container):
        """
        Add a container to this service.
        
        Parameters:
        -----------
        container : RCCNContainer
            The container to add to this service.
            
        Raises:
        -------
        TypeError
            If the provided container is not an instance of RCCNContainer.
        """
        if not isinstance(container, RCCNContainer):
            raise TypeError('Container '+container.name+' is not a RCCNContainer.')
        container.add_to_service(self)
    
    def add_command(self, command):
        """
        Add a command to this service.
        
        Parameters:
        -----------
        command : RCCNCommand
            The command to add to this service.
            
        Raises:
        -------
        TypeError
            If the provided command is not an instance of RCCNCommand.
        """
        if not isinstance(command, RCCNCommand):
            raise TypeError('Command '+command.name+' is not a RCCNCommand.')
        command.add_to_service(self)
    
    def file_paths(self):
        """
        Get the file paths for various files used by this service.
        
        Returns:
        --------
        dict
            A dictionary mapping file types to their absolute paths, including
            source files, generated snapshots, user snapshots, diff files, and templates.
        """
        paths = {
            'service': os.path.join(self.export_directory, 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'service.rs'),
            'service_generated_snapshot': os.path.join(self.snapshot_directory, 'generated', 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'service.rs'),
            'service_user_snapshot': os.path.join(self.snapshot_directory, 'user', datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'service.rs'),
            'service_diff': os.path.join(self.diff_directory, 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'service.diff'),
            'service_template': os.path.join(self.text_modules_service_path, 'service.txt'),
            'command': os.path.join(self.export_directory, 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'command.rs'),
            'command_generated_snapshot': os.path.join(self.snapshot_directory, 'generated', 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'command.rs'),
            'command_user_snapshot': os.path.join(self.snapshot_directory, 'user', datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'command.rs'),
            'command_diff': os.path.join(self.diff_directory, 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'command.diff'),
            'command_template': os.path.join(self.text_modules_command_path, 'command.txt'),
            'mod': os.path.join(self.export_directory, 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'mod.rs'),
            'mod_template': os.path.join(self.text_modules_path, 'mod', 'mod.txt'),
            'telemetry': os.path.join(self.export_directory, 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'telemetry.rs'),
            'telemetry_generated_snapshot': os.path.join(self.snapshot_directory, 'generated', 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'telemetry.rs'),
            'telemetry_user_snapshot': os.path.join(self.snapshot_directory, 'user', datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'command.rs'),
            'telemetry_diff': os.path.join(self.diff_directory, 'rccn_usr_'+snakecase(self.system.name), 'src', snakecase(self.name), 'telemetry.diff'),
            'telemetry_template': os.path.join(self.text_modules_telemetry_path, 'telemetry.txt'),
        } 
        return paths

    def rccn_commands(self):
        """
        Get all RCCNCommand objects belonging to this service, excluding base commands.
        
        Returns:
        --------
        list
            A list of RCCNCommand objects that belong to this service but are not
            named 'base'.
        """
        return [command for command in self.commands if isinstance(command, RCCNCommand) and command.name != 'base']

    def find_and_replace_keywords(self, text, text_modules_path):
        """
        Replace template keywords with actual values specific to this service.
        
        This method processes the template text, replacing service-specific keywords,
        including module keywords, variable keywords, and command keywords. It delegates
        command-specific keyword replacement to each command's find_and_replace_keywords method.
        
        Parameters:
        -----------
        text : str
            The template text containing keywords to be replaced.
        text_modules_path : str
            The path to the directory containing text module templates.
            
        Returns:
        --------
        str
            The processed text with all keywords replaced with their actual values.
            
        Raises:
        -------
        FileExistsError
            If a referenced text module file does not exist.
        """
        # Find and replace service module keywords
        service_module_keywords = get_service_module_keywords(text)
        for service_module_keyword in service_module_keywords:
            service_module_file_name = service_module_keyword.replace('>','').replace('<', '').lower() + '.txt'
            service_module_path = os.path.join(text_modules_path, service_module_file_name)
            if not os.path.exists(service_module_path):
                raise FileExistsError('Specified keyword '+service_module_keyword+' does not correspond to a text file.')
            
            with open(service_module_path, 'r') as file:
                module_text = file.read()
            replacement_text = (self.find_and_replace_keywords(module_text, text_modules_path) + '\n')
            text = insert_before_with_indentation(text, service_module_keyword, replacement_text)
        
        for command in self.rccn_commands():
            text = command.find_and_replace_keywords(text, text_modules_path)
        
        # Find and replace service variable keywords
        var_keywords = get_var_keywords(text)
        service_var_translation = {
            '<<VAR_SERVICE_NAME>>': lambda: snakecase(self.name),
            '<<VAR_SERVICE_ID>>': lambda: str(self.service_id),
            '<<VAR_SERVICE_NAME_UCASE>>': lambda: pascalcase(self.name),
            '<<VAR_SERVICE_TELEMETRY>>': lambda: self.generate_rust_telemetry_definition(),
        }
        for var_keyword in var_keywords:
            if var_keyword in service_var_translation.keys():
                text = replace_with_indentation(text, var_keyword, service_var_translation[var_keyword]())
        
        # Delete all command module keywords
        text = delete_all_command_module_keywords(text)

        return text
    
    def generate_rccn_service_file(self):
        """
        Generate the service.rs file for this service.
        
        This method creates a diff file (if both current and snapshot files exist),
        takes a snapshot of user-modified service.rs if snapshots are enabled,
        generates the new service.rs from the template, takes a snapshot of the 
        newly generated file, and applies user changes from the diff if rebase_changes
        is enabled.
        """
        # Create service.diff file
        if os.path.exists(self.file_paths()['service']) and os.path.exists(self.file_paths()['service_generated_snapshot']):
            os.makedirs(os.path.dirname(self.file_paths()['service_diff']), exist_ok=True)
            self.generate_diff_file('service', 'service_generated_snapshot', 'service_diff')
        # Create snapshot of service.rs with user changes if instructed
        if self.snapshots and os.path.exists(self.file_paths()['service']):
            self.generate_snapshot('service', 'service_user_snapshot')
        # Generate service.rs file
        with open(self.file_paths()['service_template'], 'r') as file:
            service_template_file_text = file.read()
        with open(self.file_paths()['service'], 'w') as file:
            file.write(self.find_and_replace_keywords(service_template_file_text, self.text_modules_service_path))
        # Create snapshot of service.rs if instructed
        if self.snapshots:
            self.generate_snapshot('service', 'service_generated_snapshot')
        # Rebase main.diff on main.rs if instructed
        if self.system.rebase_changes and os.path.exists(self.file_paths()['service_diff']):
            os.system('patch '+self.file_paths()['service']+' <  '+self.file_paths()['service_diff'])
    
    def generate_rccn_command_file(self, export_file_dir='.', text_modules_path='./text_modules/command'):
        """
        Generate the command.rs file for this service.
        
        This method creates a diff file (if both current and snapshot files exist),
        takes a snapshot of user-modified command.rs if snapshots are enabled,
        generates the new command.rs from the template only if there are commands
        in the service, takes a snapshot of the newly generated file, and applies
        user changes from the diff if rebase_changes is enabled.
        
        Parameters:
        -----------
        export_file_dir : str, optional
            The directory where the command.rs file will be exported. Default is current directory.
        text_modules_path : str, optional
            The path to the directory containing command text module templates. 
            Default is './text_modules/command'.
        """
        # Create command.diff file
        if os.path.exists(self.file_paths()['command']) and os.path.exists(self.file_paths()['command_generated_snapshot']):
            os.makedirs(os.path.dirname(self.file_paths()['command_diff']), exist_ok=True)
            self.generate_diff_file('command', 'command_generated_snapshot', 'command_diff')
        # Create snapshot of command.rs with user changes if instructed
        if self.snapshots and os.path.exists(self.file_paths()['command']):
            self.generate_snapshot('command', 'command_user_snapshot')
        # Generate command.rs file
        if len(self.rccn_commands()) == 0:
            print('RCCN-Information: Service \''+self.name+'\' has no commands other than base command. Generation of command.rs file will be skipped.')
            return
        command_file_path = self.file_paths()['command_template']
        with open(command_file_path, 'r') as file:
            command_file_text = file.read()
        command_export_directory = os.path.join(export_file_dir, snakecase(self.name), 'command.rs')
        with open(command_export_directory, 'w') as file:
            file.write(self.find_and_replace_keywords(command_file_text, text_modules_path))
        # Create snapshot of command.rs if instructed
        if self.snapshots:
            self.generate_snapshot('command', 'command_generated_snapshot')
        # Rebase command.diff on command.rs if instructed
        if self.system.rebase_changes and os.path.exists(self.file_paths()['command_diff']):
            os.system('patch '+self.file_paths()['command']+' <  '+self.file_paths()['command_diff'])
    
    def generate_snapshot(self, current_file_reference, snapshot_file_reference):
        """
        Create a snapshot of a file.
        
        Parameters:
        -----------
        current_file_reference : str
            Reference to the current file in the file_paths dictionary.
        snapshot_file_reference : str
            Reference to the snapshot file in the file_paths dictionary.
        """
        os.makedirs(os.path.dirname(self.file_paths()[snapshot_file_reference]), exist_ok=True)
        shutil.copyfile(self.file_paths()[current_file_reference], self.file_paths()[snapshot_file_reference])
        
    def generate_diff_file(self, current_file_reference, snapshot_file_reference, diff_file_reference):
        """
        Generate a diff file between current and snapshot files.
        
        Parameters:
        -----------
        current_file_reference : str
            Reference to the current file in the file_paths dictionary.
        snapshot_file_reference : str
            Reference to the snapshot file in the file_paths dictionary.
        diff_file_reference : str
            Reference to the diff file in the file_paths dictionary.
        """
        with open(self.file_paths()[current_file_reference], 'r') as current_file:
            current_text = current_file.readlines()
        with open(self.file_paths()[snapshot_file_reference], 'r') as snapshot_file:
            snapshot_text = snapshot_file.readlines()
        diff = difflib.unified_diff(snapshot_text, current_text, fromfile='snapshot', tofile='current')
        diff_text = ''.join(diff)
        with open(self.file_paths()[diff_file_reference], 'w') as diff_file:
            diff_file.write(diff_text)
    
    def generate_mod_file(self):
        """
        Generate the mod.rs file for this service.
        
        This file serves as the module definition file for the service in Rust,
        defining what's exported from the service module.
        """
        with open(self.file_paths()['mod_template'], 'r') as file:
            mod_template_text = file.read()
        with open(self.file_paths()['mod'], 'w') as file:
            file.write(mod_template_text)
    
    def generate_telemetry_file(self):
        """
        Generate the telemetry.rs file for this service.
        
        This method creates a diff file (if both current and snapshot files exist),
        takes a snapshot of user-modified telemetry.rs if snapshots are enabled,
        generates the new telemetry.rs from the template, takes a snapshot of the newly 
        generated file, and applies user changes from the diff if rebase_changes is enabled.
        """
        # Create telemetry.diff file
        if os.path.exists(self.file_paths()['telemetry']) and os.path.exists(self.file_paths()['telemetry_generated_snapshot']):
            os.makedirs(os.path.dirname(self.file_paths()['telemetry_diff']), exist_ok=True)
            self.generate_diff_file('telemetry', 'telemetry_generated_snapshot', 'telemetry_diff')
        # Create snapshot of telemetry.rs with user changes if instructed
        if self.snapshots and os.path.exists(self.file_paths()['telemetry']):
            self.generate_snapshot('telemetry', 'telemetry_user_snapshot')
        # Generate telemetry.rs file
        with open(self.file_paths()['telemetry_template'], 'r') as file:
            telemetry_template_file_text = file.read()
        with open(self.file_paths()['telemetry'], 'w') as file:
            file.write(self.find_and_replace_keywords(telemetry_template_file_text, self.text_modules_telemetry_path))
        # Create snapshot of telemetry.rs if instructed
        if self.snapshots:
            self.generate_snapshot('telemetry', 'telemetry_generated_snapshot')
        # Rebase main.diff on main.rs if instructed
        if self.system.rebase_changes and os.path.exists(self.file_paths()['telemetry_diff']):
            os.system('patch '+self.file_paths()['telemetry']+' <  '+self.file_paths()['telemetry_diff'])
    
    def generate_rust_telemetry_definition(self):
        """
        Generate Rust code definitions for all telemetry containers in this service.
        
        Returns:
        --------
        str
            A string containing Rust struct definitions for all telemetry containers.
        """
        telemetry_definition_text = ''
        for container in self.containers:
            if not isinstance(container, RCCNContainer):
                container.__class__ = RCCNContainer
            telemetry_definition_text += container.generate_rccn_telemetry()
        return telemetry_definition_text
    
    def create_and_add_command(
            self,
            name: str,
            *,
            aliases: Mapping[str, str] | None = None,
            short_description: str | None = None,
            long_description: str | None = None,
            extra: Mapping[str, str] | None = None,
            abstract: bool = False,
            base: Command | str | None = None,
            assignments: Mapping[str, Any] | None = None,
            arguments: Sequence[Argument] | None = None,
            entries: Sequence[CommandEntry] | None = None,
            level: CommandLevel = CommandLevel.NORMAL,
            warning_message: str | None = None,
            constraint: (
                Union[TransmissionConstraint, Sequence[TransmissionConstraint]] | None
            ) = None,
    ):
        """
        Create a new command and add it to this service.
        
        Parameters:
        -----------
        name : str
            The name of the command.
        aliases : Mapping[str, str], optional
            Alternative names for the command, keyed by namespace.
        short_description : str, optional
            A short description of the command.
        long_description : str, optional
            A longer description of the command.
        extra : Mapping[str, str], optional
            Arbitrary information about the command, keyed by name.
        abstract : bool, optional
            Whether this command is abstract. Default is False.
        base : Command | str, optional
            The base command or reference to a base command.
        assignments : Mapping[str, Any], optional
            Command assignments.
        arguments : Sequence[Argument], optional
            The arguments for this command.
        entries : Sequence[CommandEntry], optional
            Command entries.
        level : CommandLevel, optional
            The command level. Default is CommandLevel.NORMAL.
        warning_message : str, optional
            Warning message to display when executing this command.
        constraint : Union[TransmissionConstraint, Sequence[TransmissionConstraint]], optional
            Transmission constraints for this command.
        """
        Command(
            name=name,
            system=self,
            aliases=aliases,
            short_description=short_description,
            long_description=long_description,
            extra=extra,
            abstract=abstract,
            base=base,
            assignments=assignments,
            arguments=arguments,
            entries=entries,
            level=level,
            warning_message=warning_message,
            constraint=constraint
        ) 
    
    def rccn_container(self):
        """
        Get all RCCNContainer objects belonging to this service.
        
        Returns:
        --------
        list
            A list of RCCNContainer objects that belong to this service.
        """
        return [container for container in self.containers if isinstance(container, RCCNContainer)]


class RCCNCommand(Command):
    """
    A Protocol Utilization Standard (PUS) command that belongs to a Service.
    
    This class extends the Command class and provides specialized functionality for 
    generating Rust code for commands within a PUS service. RCCNCommand manages command
    subtype assignment, struct name generation for arguments, and handling of base commands.
    
    Each RCCNCommand automatically gets assigned to its parent Service's APID (Application 
    Process ID) and a unique subtype within that service. It can generate Rust code for
    command structs and implements keyword replacement for templates.
    """
    def __init__(
        self,
        name: str,
        *,
        aliases: Mapping[str, str] | None = None,
        short_description: str | None = None,
        long_description: str | None = None,
        extra: Mapping[str, str] | None = None,
        abstract: bool = False,
        base: Command | str | None = None,
        assignments: Mapping[str, Any] | None = None,
        arguments: Sequence[Argument] | None = None,
        entries: Sequence[CommandEntry] | None = None,
        level: CommandLevel = CommandLevel.NORMAL,
        warning_message: str | None = None,
        constraint: (
            Union[TransmissionConstraint, Sequence[TransmissionConstraint]] | None
        ) = None,
        **kwargs
    ):
        """
        Initialize a new PUS command.
        
        Parameters:
        -----------
        name : str
            The name of the command.
        aliases : Mapping[str, str], optional
            Alternative names for the command, keyed by namespace.
        short_description : str, optional
            A short description of the command.
        long_description : str, optional
            A longer description of the command.
        extra : Mapping[str, str], optional
            Arbitrary information about the command, keyed by name.
        abstract : bool, optional
            Whether this command is abstract. Default is False.
        base : Command | str, optional
            The base command or reference to a base command.
        assignments : Mapping[str, Any], optional
            Command assignments, including the subtype.
        arguments : Sequence[Argument], optional
            The arguments for this command.
        entries : Sequence[CommandEntry], optional
            Command entries.
        level : CommandLevel, optional
            The command level. Default is CommandLevel.NORMAL.
        warning_message : str, optional
            Warning message to display when executing this command.
        constraint : Union[TransmissionConstraint, Sequence[TransmissionConstraint]], optional
            Transmission constraints for this command.
        **kwargs
            Additional keyword arguments that may include 'system' to specify
            which service this command belongs to.
        """
        self.init_args = ()
        self.init_kwargs = {
            'name': name,
            'aliases': aliases,
            'short_description': short_description,
            'long_description': long_description,
            'extra': extra,
            'abstract': abstract,
            'base': base,
            'assignments': assignments,
            'arguments': arguments,
            'entries': entries,
            'level': level,
            'warning_message': warning_message,
            'constraint': constraint,
            **kwargs
        }
        if 'system' in kwargs and isinstance(kwargs['system'], Service):
            self.add_to_service(kwargs['system'])
        elif base and (isinstance(base, Command) or isinstance(base, RCCNCommand)):
            self.add_to_service(base.system)

    def add_to_service(self, service):
        """
        Add this command to a Service.
        
        This method handles the initialization of the command as part of a service,
        setting up base commands if needed, and assigning a subtype if one isn't
        explicitly provided.
        
        Parameters:
        -----------
        service : Service
            The service this command will belong to.
            
        Notes:
        ------
        - If no base command is specified and the service has no base command,
          a standard base command will be created automatically
        - If no subtype is provided, a unique one will be assigned automatically
        - The command's APID is automatically set to match the service's application APID
        """
        if self.init_kwargs['base'] is None and not any(command.name == 'base' for command in service.commands):
            print("RCCN-Information: Command \'"+self.init_kwargs['name']+"\' doesn\'t have a base argument and no base command was found in service \'"+service.name+"\'.\nStandard base command will be created with system = \'"+service.name+"\' and type = "+str(service.service_id)+".")
            self.init_kwargs['base'] = Command(
                system=service, 
                name='base',
                abstract=True,
                base='/PUS/pus-tc',
                assignments={'type': service.service_id}
            )
        elif self.init_kwargs['base'] is None and any(command.name == 'base' for command in service.commands):
            print("RCCN-Information: Command \'"+self.init_kwargs['name']+"\' doesn\'t have a \'base\' argument. Existing base command for service \'"+service.name+"\' will be used.")
            self.init_kwargs['base'] = next(command for command in service.commands if command.name == 'base')
        if 'system' in self.init_kwargs and isinstance(self.init_kwargs['system'], Service):
            super().__init__(*self.init_args, **self.init_kwargs)
        else:
            super().__init__(system=service, *self.init_args, **self.init_kwargs)
        self.assignments['apid'] = self.system.system.apid
        if not 'subtype' in self.assignments and self.name != 'base':
            used_subtypes = [command.assignments['subtype'] if 'subtype' in command.assignments else None for command in self.system.rccn_commands()]
            new_subtype = 1
            while new_subtype in used_subtypes:
                new_subtype = new_subtype + 1
            print('RCCN-Information: Command \''+self.name+'\' has no subtype specified. Subtype will be set to '+str(new_subtype)+'.')
            self.assignments['subtype'] = new_subtype
        self.struct_name = self.name + 'Args'

    
    def find_and_replace_keywords(self, text, text_modules_path):
        """
        Replace template keywords with actual command values.
        
        This method processes template text, replacing command-specific keywords with 
        the actual values from this command. It handles:
        1. Command module keywords - references to external template files
        2. Command variable keywords - specific properties of this command
        
        Parameters:
        -----------
        text : str
            Template text containing keywords to be replaced.
        text_modules_path : str
            Path to the directory containing text module templates.
            
        Returns:
        --------
        str
            The processed text with all command keywords replaced with their actual values.
            
        Raises:
        -------
        FileExistsError
            If a referenced command module file does not exist.
        """
        # Find and replace command module keywords
        command_module_keywords = get_command_module_keywords(text)
        for command_module_keyword in command_module_keywords:
            command_module_file_name = command_module_keyword.replace('>','').replace('<', '').lower() + '.txt'
            command_module_path = os.path.join(text_modules_path, command_module_file_name)
            if not os.path.exists(command_module_path):
                raise FileExistsError('Specified keyword '+command_module_keyword+' does not correspond to a text file.')
            
            with open(command_module_path, 'r') as file:
                module_text = file.read()
            replacement_text = (self.find_and_replace_keywords(module_text, text_modules_path) + '\n')
            text = insert_before_with_indentation(text, command_module_keyword, replacement_text)

        # Find and replace command variable keywords
        command_var_keywords = get_var_keywords(text)
        command_var_translation = {
            '<<VAR_COMMAND_NAME_UCASE>>': lambda: pascalcase(self.name),
            '<<VAR_COMMAND_NAME>>': lambda: self.name,
            '<<VAR_COMMAND_STRUCT_NAME>>': lambda: self.struct_name,
            '<<VAR_COMMAND_SUBTYPE>>': lambda: str(self.assignments['subtype']),
            '<<VAR_COMMAND_STRUCT>>': lambda: self.struct_definition(),
            '<<VAR_SHORT_DESCRIPTION>>': lambda: "\n/// " + self.short_description if self.short_description is not None else "",
        }
        for command_var_keyword in command_var_keywords:
            if command_var_keyword in command_var_translation.keys():
                text = replace_with_indentation(text, command_var_keyword, command_var_translation[command_var_keyword]())
        return text
    
    def user_snapshot_path(self):
        """
        Get the path for user snapshots with current timestamp.
        
        Returns:
        --------
        str
            The path where user snapshots are stored.
        """
        return os.path.join(self.snapshot_directory, 'user', datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

    def struct_definition(self):
        """
        Generate a Rust struct definition for this command's arguments.
        
        This method creates a BitStruct definition in Rust for the command's arguments,
        with appropriate documentation comments. If the command has no arguments,
        an empty string is returned.
        
        Returns:
        --------
        str
            A string containing the Rust code for the struct definition, or an empty
            string if the command has no arguments.
        """
        struct_definition_text = ""
        if len(self.arguments) == 0:
            return ''
        if hasattr(self, 'long_description') and self.long_description is not None:
            struct_definition_text += "/// "+str(self.long_description)+"\n"
        struct_definition_text += "#[derive(BitStruct, Debug, PartialEq)]\npub struct "+pascalcase(self.struct_name)+" {\n"
        ins = ""
        append = ""
        for argument in self.arguments:
            arg_def = rust_type_definition(argument)
            ins += arg_def[0]
            append += arg_def[1]
        struct_definition_text += ins
        struct_definition_text += "}\n"
        struct_definition_text += append
        return struct_definition_text



class RCCNContainer(Container):
    """
    A Protocol Utilization Standard (PUS) telemetry container that belongs to a Service.
    
    This class extends the Container class and provides specialized functionality for 
    generating Rust code for telemetry containers within a PUS service. RCCNContainer
    manages container type and subtype assignment, condition expressions, and handles
    the generation of Rust struct definitions for telemetry data.
    
    Each RCCNContainer is automatically assigned to its parent Service's service ID (type)
    and receives a unique subtype within that service. It supports various parameter types
    for telemetry data collection and provides methods to add these parameters to the container.
    """
    def __init__(
        self,
        base="/PUS/pus-tm", 
        subtype = None,
        *,
        system: System = None, 
        name: str = None,
        entries: Sequence[ParameterEntry | ContainerEntry] | None = None,
        abstract: bool = False,
        condition: Expression | None = None,
        aliases: Mapping[str, str] | None = None,
        short_description: str | None = None,
        long_description: str | None = None,
        extra: Mapping[str, str] | None = None,
        bits: int | None = None,
        rate: float | None = None,
        hint_partition: bool = False,
    ):
        """
        Initialize a new PUS telemetry container.
        
        Parameters:
        -----------
        base : str, optional
            Base path for the telemetry packet. Default is "/PUS/pus-tm".
        subtype : int, optional
            Subtype for the container. If not provided, a unique value will be assigned.
        system : System, optional
            The system (usually a Service) this container belongs to.
        name : str
            The name of the container. Required.
        entries : Sequence[ParameterEntry | ContainerEntry], optional
            Parameter or container entries for this container.
        abstract : bool, optional
            Whether this container is abstract. Default is False.
        condition : Expression, optional
            Condition expression for when this container should be used.
        aliases : Mapping[str, str], optional
            Alternative names for the container, keyed by namespace.
        short_description : str, optional
            A short description of the container.
        long_description : str, optional
            A longer description of the container.
        extra : Mapping[str, str], optional
            Arbitrary information about the container, keyed by name.
        bits : int, optional
            Size in bits.
        rate : float, optional
            Expected rate of reception in Hz.
        hint_partition : bool, optional
            Hint to partition this container. Default is False.
            
        Raises:
        -------
        ValueError
            If name is not provided.
        """
        self.base = base
        self.subtype = subtype
        self.init_kwargs = {
            'system': system,
            'name': name,
            'entries': entries,
            'base': base,
            'abstract': abstract,
            'condition': condition,
            'aliases': aliases,
            'short_description': short_description,
            'long_description': long_description,
            'extra': extra,
            'bits': bits,
            'rate': rate,
            'hint_partition': hint_partition,
        }
        
        if name is None:
            raise ValueError('RCCN-Error: Container must have a name.')
            
        self.name = name
        if system is not None and isinstance(system, Service):
            self.add_to_service(system)

    def add_to_service(self, service):
        """
        Add this container to a Service.
        
        This method handles the initialization of the container as part of a service,
        setting up condition expressions for type and subtype, and managing the container's
        integration with the service.
        
        The method performs several key operations:
        1. Sets the container's type to match the service ID
        2. Extracts type/subtype from existing condition expressions if present
        3. Creates appropriate condition expressions for the container
        4. Assigns a unique subtype if one isn't explicitly provided
        
        Parameters:
        -----------
        service : Service
            The service this container will belong to.
        """
        self.type = service.service_id
        condition_type = None
        condition_subtype = None
        if self.init_kwargs['condition'] is not None:
            for eq_expression in self.init_kwargs['condition'].expressions:
                if eq_expression.ref == self.base+'/type':
                    condition_type = eq_expression.value
                if eq_expression.ref == self.base+'/subtype':
                    condition_subtype = eq_expression.value
        if condition_type is not None and condition_type != self.type:
            print('RCCN-Warning: Container '+self.name+' has a user-defined type of '+str(eq_expression.value)+', which does\'nt match the service ID. User-defined type will be used.')
            self.type = condition_type
        if condition_subtype is not None and self.subtype is not None and condition_subtype != self.subtype:
            print('RCCN-Warning: Container '+self.name+' has an ambiguous user-defined subtype. \'subtype\' argument should match the \'condition\' argument.')
        elif condition_subtype is not None:
            self.subtype = condition_subtype
        elif self.subtype is not None and self.init_kwargs['condition'] is not None:
            self.init_kwargs['condition'] = AndExpression(
                EqExpression(self.base+'/type', self.type),
                EqExpression(self.base+'/subtype', self.subtype)
                )
        else:
            used_subtypes = [container.subtype for container in service.rccn_container()]
            new_subtype = 1
            while new_subtype in used_subtypes:
                new_subtype = new_subtype + 1
            self.subtype = new_subtype
            self.init_kwargs['condition'] = AndExpression(
                EqExpression(self.base+'/type', self.type),
                EqExpression(self.base+'/subtype', self.subtype)
                )
            print('RCCN-Information: Subtype for Container '+self.name+' is not specified through \'subtype\' or \'condition\' arguments. Subtype will be set to '+str(self.subtype)+'.')

        if 'system' in self.init_kwargs and isinstance(self.init_kwargs['system'], Service):
            super().__init__(**self.init_kwargs)
        else:
            super().__init__(system=service, **self.init_kwargs)

    def generate_rccn_telemetry(self):
        """
        Generate Rust code for this telemetry container.
        
        This method creates a Rust struct definition for the container, including:
        1. Documentation comments from the container's short_description
        2. ServiceTelemetry and BitStruct derive attributes
        3. Subtype attribute if a subtype is defined
        4. All parameter entries from the container
        
        Returns:
        --------
        str
            A string containing the complete Rust struct definition for this container.
        """
        rccn_telemetry_text = ""
        if hasattr(self, 'short_description') and self.short_description is not None:
            rccn_telemetry_text += "/// "+str(self.short_description)+"\n"
        rccn_telemetry_text += "#[derive(ServiceTelemetry, BitStruct, Debug)]\n"
        if hasattr(self, 'subtype') and self.subtype is not None:
            rccn_telemetry_text += "#[subtype("+str(self.subtype)+")]\n"
        rccn_telemetry_text += "pub struct " + self.name + " {\n"
        insert, append = ["",""]
        for parameter_entry in self.entries:
            par_def = rust_type_definition(parameter_entry.parameter)
            insert += par_def[0]
            append += par_def[1]
        rccn_telemetry_text += insert
        rccn_telemetry_text += "}\n\n"
        rccn_telemetry_text += append        
        return rccn_telemetry_text
    
    def add_integer_parameter_entry(
            self,
            name: str,
            signed: bool = True,
            bits: int = 32,
            minimum: int | None = None,
            maximum: int | None = None,
            aliases: Mapping[str, str] | None = None,
            data_source: DataSource = DataSource.TELEMETERED,
            initial_value: Any = None,
            persistent: bool = True,
            short_description: str | None = None,
            long_description: str | None = None,
            extra: Mapping[str, str] | None = None,
            units: str | None = None,
            encoding: Encoding | None = None,
            calibrator: Calibrator | None = None,
            alarm: ThresholdAlarm | None = None,
            context_alarms: Sequence[ThresholdContextAlarm] | None = None,
     ):
        """
        Add an integer parameter to this container.
        
        This method creates an integer parameter and adds it as an entry to this container.
        
        Parameters:
        -----------
        name : str
            The name of the parameter.
        signed : bool, optional
            Whether the integer is signed. Default is True.
        bits : int, optional
            Number of bits. Default is 32.
        minimum : int, optional
            Minimum valid value.
        maximum : int, optional
            Maximum valid value.
        aliases : Mapping[str, str], optional
            Alternative names for the parameter, keyed by namespace.
        data_source : DataSource, optional
            Source of the parameter value. Default is DataSource.TELEMETERED.
        initial_value : Any, optional
            Initial value for this parameter.
        persistent : bool, optional
            Whether this parameter's value should be persisted. Default is True.
        short_description : str, optional
            A short description of the parameter.
        long_description : str, optional
            A longer description of the parameter.
        extra : Mapping[str, str], optional
            Arbitrary information about the parameter, keyed by name.
        units : str, optional
            Units of this parameter.
        encoding : Encoding, optional
            Encoding information for this parameter.
        calibrator : Calibrator, optional
            Calibration information for this parameter.
        alarm : ThresholdAlarm, optional
            Alarm conditions for this parameter.
        context_alarms : Sequence[ThresholdContextAlarm], optional
            Context-dependent alarm conditions for this parameter.
        """
        parameter = IntegerParameter(
            system=self.system,
            name=name,
            signed=signed,
            bits=bits,
            minimum=minimum,
            maximum=maximum,
            aliases=aliases,
            data_source=data_source,
            initial_value=initial_value,
            persistent=persistent,
            short_description=short_description,
            long_description=long_description,
            extra=extra,
            units=units,
            encoding=encoding,
            calibrator=calibrator,
            alarm=alarm,
            context_alarms=context_alarms
        )
        self.entries.append(ParameterEntry(parameter=parameter))

    def add_enumerated_parameter_entry( 
        self,
        name: str,
        choices: Choices,
        alarm: EnumerationAlarm | None = None,
        context_alarms: Sequence[EnumerationContextAlarm] | None = None,
        aliases: Mapping[str, str] | None = None,
        data_source: DataSource = DataSource.TELEMETERED,
        initial_value: Any = None,
        persistent: bool = True,
        short_description: str | None = None,
        long_description: str | None = None,
        extra: Mapping[str, str] | None = None,
        units: str | None = None,
        encoding: Encoding | None = None,
    ):
        """
        Add an enumerated parameter to this container.
        
        This method creates an enumerated parameter with predefined choices and adds it
        as an entry to this container.
        
        Parameters:
        -----------
        name : str
            The name of the parameter.
        choices : Choices
            The enumeration choices for this parameter.
        alarm : EnumerationAlarm, optional
            Alarm conditions for this parameter.
        context_alarms : Sequence[EnumerationContextAlarm], optional
            Context-dependent alarm conditions for this parameter.
        aliases : Mapping[str, str], optional
            Alternative names for the parameter, keyed by namespace.
        data_source : DataSource, optional
            Source of the parameter value. Default is DataSource.TELEMETERED.
        initial_value : Any, optional
            Initial value for this parameter.
        persistent : bool, optional
            Whether this parameter's value should be persisted. Default is True.
        short_description : str, optional
            A short description of the parameter.
        long_description : str, optional
            A longer description of the parameter.
        extra : Mapping[str, str], optional
            Arbitrary information about the parameter, keyed by name.
        units : str, optional
            Units of this parameter.
        encoding : Encoding, optional
            Encoding information for this parameter.
        """
        parameter = EnumeratedParameter(
            system = self.system,
            name=name,
            choices=choices,
            alarm=alarm,
            context_alarms=context_alarms,
            aliases=aliases,
            data_source=data_source,
            initial_value=initial_value,
            persistent=persistent,
            short_description=short_description,
            long_description=long_description,
            extra=extra,
            units=units,
            encoding=encoding
        )
        self.entries.append(ParameterEntry(parameter=parameter))
        
    def add_boolean_parameter_entry(
        self,
        name: str,
        zero_string_value: str = "False",
        one_string_value: str = "True",
        aliases: Mapping[str, str] | None = None,
        data_source: DataSource = DataSource.TELEMETERED,
        initial_value: Any = None,
        persistent: bool = True,
        short_description: str | None = None,
        long_description: str | None = None,
        extra: Mapping[str, str] | None = None,
        units: str | None = None,
        encoding: Encoding | None = None,
    ):
        """
        Add a boolean parameter to this container.
        
        This method creates a boolean parameter and adds it as an entry to this container.
        
        Parameters:
        -----------
        name : str
            The name of the parameter.
        zero_string_value : str, optional
            String representation of the boolean value 'false'. Default is "False".
        one_string_value : str, optional
            String representation of the boolean value 'true'. Default is "True".
        aliases : Mapping[str, str], optional
            Alternative names for the parameter, keyed by namespace.
        data_source : DataSource, optional
            Source of the parameter value. Default is DataSource.TELEMETERED.
        initial_value : Any, optional
            Initial value for this parameter.
        persistent : bool, optional
            Whether this parameter's value should be persisted. Default is True.
        short_description : str, optional
            A short description of the parameter.
        long_description : str, optional
            A longer description of the parameter.
        extra : Mapping[str, str], optional
            Arbitrary information about the parameter, keyed by name.
        units : str, optional
            Units of this parameter.
        encoding : Encoding, optional
            Encoding information for this parameter.
        """
        parameter = BooleanParameter(
            system=self.system,
            name=name,
            zero_string_value=zero_string_value,
            one_string_value=one_string_value,
            aliases=aliases,
            data_source=data_source,
            initial_value=initial_value,
            persistent=persistent,
            short_description=short_description,
            long_description=long_description,
            extra=extra,
            units=units,
            encoding=encoding
        )
        self.entries.append(ParameterEntry(parameter=parameter))

    def add_float_parameter_entry(
        self,
        name: str,
        bits: Literal[32, 64] = 32,
        minimum: float | None = None,
        minimum_inclusive: bool = True,
        maximum: float | None = None,
        maximum_inclusive: bool = True,
        aliases: Mapping[str, str] | None = None,
        data_source: DataSource = DataSource.TELEMETERED,
        initial_value: Any = None,
        persistent: bool = True,
        short_description: str | None = None,
        long_description: str | None = None,
        extra: Mapping[str, str] | None = None,
        units: str | None = None,
        encoding: Encoding | None = None,
        calibrator: Calibrator | None = None,
        alarm: ThresholdAlarm | None = None,
        context_alarms: Sequence[ThresholdContextAlarm] | None = None,
    ):
        """
        Add a floating-point parameter to this container.
        
        This method creates a float parameter and adds it as an entry to this container.
        
        Parameters:
        -----------
        name : str
            The name of the parameter.
        bits : Literal[32, 64], optional
            Number of bits, either 32 (float) or 64 (double). Default is 32.
        minimum : float, optional
            Minimum valid value.
        minimum_inclusive : bool, optional
            Whether the minimum value is inclusive. Default is True.
        maximum : float, optional
            Maximum valid value.
        maximum_inclusive : bool, optional
            Whether the maximum value is inclusive. Default is True.
        aliases : Mapping[str, str], optional
            Alternative names for the parameter, keyed by namespace.
        data_source : DataSource, optional
            Source of the parameter value. Default is DataSource.TELEMETERED.
        initial_value : Any, optional
            Initial value for this parameter.
        persistent : bool, optional
            Whether this parameter's value should be persisted. Default is True.
        short_description : str, optional
            A short description of the parameter.
        long_description : str, optional
            A longer description of the parameter.
        extra : Mapping[str, str], optional
            Arbitrary information about the parameter, keyed by name.
        units : str, optional
            Units of this parameter.
        encoding : Encoding, optional
            Encoding information for this parameter.
        calibrator : Calibrator, optional
            Calibration information for this parameter.
        alarm : ThresholdAlarm, optional
            Alarm conditions for this parameter.
        context_alarms : Sequence[ThresholdContextAlarm], optional
            Context-dependent alarm conditions for this parameter.
        """
        parameter = FloatParameter(
            system=self.system,
            name=name,
            bits=bits,
            minimum=minimum,
            minimum_inclusive=minimum_inclusive,
            maximum=maximum,
            maximum_inclusive=maximum_inclusive,
            aliases=aliases,
            data_source=data_source,
            initial_value=initial_value,
            persistent=persistent,
            short_description=short_description,
            long_description=long_description,
            extra=extra,
            units=units,
            encoding=encoding,
            calibrator=calibrator,
            alarm=alarm,
            context_alarms=context_alarms
        )
        self.entries.append(ParameterEntry(parameter=parameter))
    
    def add_string_parameter_entry(
        self,
        name: str,
        min_length: int | None = None,
        max_length: int | None = None,
        aliases: Mapping[str, str] | None = None,
        data_source: DataSource = DataSource.TELEMETERED,
        initial_value: Any = None,
        persistent: bool = True,
        short_description: str | None = None,
        long_description: str | None = None,
        extra: Mapping[str, str] | None = None,
        units: str | None = None,
        encoding: Encoding | None = None,
    ):
        """
        Add a string parameter to this container.
        
        This method creates a string parameter and adds it as an entry to this container.
        
        Parameters:
        -----------
        name : str
            The name of the parameter.
        min_length : int, optional
            Minimum valid length of the string.
        max_length : int, optional
            Maximum valid length of the string.
        aliases : Mapping[str, str], optional
            Alternative names for the parameter, keyed by namespace.
        data_source : DataSource, optional
            Source of the parameter value. Default is DataSource.TELEMETERED.
        initial_value : Any, optional
            Initial value for this parameter.
        persistent : bool, optional
            Whether this parameter's value should be persisted. Default is True.
        short_description : str, optional
            A short description of the parameter.
        long_description : str, optional
            A longer description of the parameter.
        extra : Mapping[str, str], optional
            Arbitrary information about the parameter, keyed by name.
        units : str, optional
            Units of this parameter.
        encoding : Encoding, optional
            Encoding information for this parameter.
        """
        parameter = StringParameter(
            system=self.system,
            name=name,
            min_length=min_length,
            max_length=max_length,
            aliases=aliases,
            data_source=data_source,
            initial_value=initial_value,
            persistent=persistent,
            short_description=short_description,
            long_description=long_description,
            extra=extra,
            units=units,
            encoding=encoding
        )
        self.entries.append(ParameterEntry(parameter=parameter))

    def add_binary_parameter_entry(
        self,
        name: str,
        min_length: int | None = None,
        max_length: int | None = None,
        aliases: Mapping[str, str] | None = None,
        data_source: DataSource = DataSource.TELEMETERED,
        initial_value: Any = None,
        persistent: bool = True,
        short_description: str | None = None,
        long_description: str | None = None,
        extra: Mapping[str, str] | None = None,
        units: str | None = None,
        encoding: Encoding | None = None,
    ):
        """
        Add a binary parameter to this container.
        
        This method creates a binary parameter and adds it as an entry to this container.
        
        Parameters:
        -----------
        name : str
            The name of the parameter.
        min_length : int, optional
            Minimum valid length of the binary data in bytes.
        max_length : int, optional
            Maximum valid length of the binary data in bytes.
        aliases : Mapping[str, str], optional
            Alternative names for the parameter, keyed by namespace.
        data_source : DataSource, optional
            Source of the parameter value. Default is DataSource.TELEMETERED.
        initial_value : Any, optional
            Initial value for this parameter.
        persistent : bool, optional
            Whether this parameter's value should be persisted. Default is True.
        short_description : str, optional
            A short description of the parameter.
        long_description : str, optional
            A longer description of the parameter.
        extra : Mapping[str, str], optional
            Arbitrary information about the parameter, keyed by name.
        units : str, optional
            Units of this parameter.
        encoding : Encoding, optional
            Encoding information for this parameter.
        """
        parameter = BinaryParameter(
            system=self.system,
            name=name,
            min_length=min_length,
            max_length=max_length,
            aliases=aliases,
            data_source=data_source,
            initial_value=initial_value,
            persistent=persistent,
            short_description=short_description,
            long_description=long_description,
            extra=extra,
            units=units,
            encoding=encoding
        )
        self.entries.append(ParameterEntry(parameter=parameter))

    def add_absolute_time_parameter_entry(
        self,
        name: str,
        reference: Union[Epoch, datetime.datetime, AbsoluteTimeParameter],
        aliases: Mapping[str, str] | None = None,
        data_source: DataSource = DataSource.TELEMETERED,
        initial_value: Any = None,
        persistent: bool = True,
        short_description: str | None = None,
        long_description: str | None = None,
        extra: Mapping[str, str] | None = None,
        units: str | None = None,
        encoding: TimeEncoding | None = None,
    ):
        """
        Add an absolute time parameter to this container.
        
        This method creates an absolute time parameter and adds it as an entry to this container.
        
        Parameters:
        -----------
        name : str
            The name of the parameter.
        reference : Union[Epoch, datetime.datetime, AbsoluteTimeParameter]
            Reference time (epoch) for this parameter.
        aliases : Mapping[str, str], optional
            Alternative names for the parameter, keyed by namespace.
        data_source : DataSource, optional
            Source of the parameter value. Default is DataSource.TELEMETERED.
        initial_value : Any, optional
            Initial value for this parameter.
        persistent : bool, optional
            Whether this parameter's value should be persisted. Default is True.
        short_description : str, optional
            A short description of the parameter.
        long_description : str, optional
            A longer description of the parameter.
        extra : Mapping[str, str], optional
            Arbitrary information about the parameter, keyed by name.
        units : str, optional
            Units of this parameter.
        encoding : TimeEncoding, optional
            Encoding information for this time parameter.
        """
        parameter = AbsoluteTimeParameter(
            system=self,
            name=name,
            reference=reference,
            aliases=aliases,
            data_source=data_source,
            initial_value=initial_value,
            persistent=persistent,
            short_description=short_description,
            long_description=long_description,
            extra=extra,
            units=units,
            encoding=encoding
        )
        self.entries.append(ParameterEntry(parameter=parameter))

    def add_aggregate_parameter_entry(
        self,
        name: str,
        members: Sequence[Member],
        aliases: Mapping[str, str] | None = None,
        data_source: DataSource = DataSource.TELEMETERED,
        initial_value: Any = None,
        persistent: bool = True,
        short_description: str | None = None,
        long_description: str | None = None,
        extra: Mapping[str, str] | None = None,
        encoding: Encoding | None = None,
    ):
        """
        Add an aggregate parameter to this container.
        
        This method creates an aggregate parameter (a parameter composed of multiple members)
        and adds it as an entry to this container.
        
        Parameters:
        -----------
        name : str
            The name of the parameter.
        members : Sequence[Member]
            The members that make up this aggregate parameter.
        aliases : Mapping[str, str], optional
            Alternative names for the parameter, keyed by namespace.
        data_source : DataSource, optional
            Source of the parameter value. Default is DataSource.TELEMETERED.
        initial_value : Any, optional
            Initial value for this parameter.
        persistent : bool, optional
            Whether this parameter's value should be persisted. Default is True.
        short_description : str, optional
            A short description of the parameter.
        long_description : str, optional
            A longer description of the parameter.
        extra : Mapping[str, str], optional
            Arbitrary information about the parameter, keyed by name.
        encoding : Encoding, optional
            Encoding information for this parameter.
        """
        parameter = AggregateParameter(
            system=self.system,
            name=name,
            members=members,
            aliases=aliases,
            data_source=data_source,
            initial_value=initial_value,
            persistent=persistent,
            short_description=short_description,
            long_description=long_description,
            extra=extra,
            encoding=encoding
        )
        self.entries.append(ParameterEntry(parameter=parameter))

    def add_array_parameter_entry(
        self,
        name: str,
        data_type: DataType,
        length: int | DynamicInteger,
        aliases: Mapping[str, str] | None = None,
        data_source: DataSource = DataSource.TELEMETERED,
        initial_value: Any = None,
        persistent: bool = True,
        short_description: str | None = None,
        long_description: str | None = None,
        extra: Mapping[str, str] | None = None,
        encoding: Encoding | None = None,
    ):
        """
        Add an array parameter to this container.
        
        This method creates an array parameter (a parameter containing multiple elements
        of the same type) and adds it as an entry to this container.
        
        Parameters:
        -----------
        name : str
            The name of the parameter.
        data_type : DataType
            The data type of the array elements.
        length : int | DynamicInteger
            The length of the array, either as a fixed integer or a dynamic reference.
        aliases : Mapping[str, str], optional
            Alternative names for the parameter, keyed by namespace.
        data_source : DataSource, optional
            Source of the parameter value. Default is DataSource.TELEMETERED.
        initial_value : Any, optional
            Initial value for this parameter.
        persistent : bool, optional
            Whether this parameter's value should be persisted. Default is True.
        short_description : str, optional
            A short description of the parameter.
        long_description : str, optional
            A longer description of the parameter.
        extra : Mapping[str, str], optional
            Arbitrary information about the parameter, keyed by name.
        encoding : Encoding, optional
            Encoding information for this parameter.
        """
        parameter = ArrayParameter(
            system=self.system,
            name=name,
            data_type=data_type,
            length=length,
            aliases=aliases,
            data_source=data_source,
            initial_value=initial_value,
            persistent=persistent,
            short_description=short_description,
            long_description=long_description,
            extra=extra,
            encoding=encoding
        )
        self.entries.append(ParameterEntry(parameter=parameter))