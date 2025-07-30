import os
from pathlib import Path
import configparser
import socket
import time
import traceback
import shutil
import uuid
from argparse import RawTextHelpFormatter
from configparser import ConfigParser
from datetime import datetime, timedelta
from distutils.spawn import find_executable  # pylint: disable=deprecated-module
import argparse
from packaging.version import parse
from ScriptCollection.ScriptCollectionCore import ScriptCollectionCore
from ScriptCollection.GeneralUtilities import GeneralUtilities
import psutil
import yaml

product_name = "Adame"
version = "1.2.57"
__version__ = version
versioned_product_name = f"{product_name} v{version}"


class Adame:

    # <constants>
    __adame_commit_author_name: str = product_name
    __configuration_section_general: str = "general"
    __configuration_section_general_key_networkinterface: str = "networkinterface"
    __configuration_section_general_key_prescript: str = "prescript"
    __configuration_section_general_key_postscript: str = "postscript"
    __configuration_section_general_key_repositoryid: str = "repositoryid"
    __configuration_section_general_key_repositoryversion: str = "repositoryversion"
    __configuration_section_general_key_formatversion: str = "formatversion"
    __configuration_section_general_key_name: str = "name"
    __configuration_section_general_key_owner: str = "owner"
    __configuration_section_general_key_gpgkeyofowner: str = "gpgkeyofowner"
    __configuration_section_general_key_remoteaddress: str = "remoteaddress"
    __configuration_section_general_key_remotename: str = "remotename"
    __configuration_section_general_key_remotebranch: str = "remotebranch"
    __configuration_section_general_key_maximalexpectedstartduration: str = "maximalexpectedstartduration"
    __configuration_section_general_key_logtargetfolder: str = "logtargetfolder"
    __configuration_section_general_key_maximalexpectedstartduration_defaultvalue: int = 0
    __securityconfiguration_section_general: str = "general"
    __securityconfiguration_section_general_key_siemaddress: str = "siemaddress"
    __securityconfiguration_section_general_key_siemfolder: str = "siemfolder"
    __securityconfiguration_section_general_key_siemuser: str = "siemuser"
    __securityconfiguration_section_general_key_idsname: str = "idsname"
    __securityconfiguration_section_general_key_enabledids: str = "enableids"
    __securityconfiguration_section_snort: str = "snort"
    __securityconfiguration_section_snort_key_globalconfigurationfile: str = "globalconfigurationfile"
    _internal_configuration_folder: str = None
    __configuration_file: str = None
    __security_related_configuration_folder: str = None
    __repository_folder: str = None
    __configuration: ConfigParser = None
    __securityconfiguration: ConfigParser = None
    __log_folder: str = None
    __log_folder_for_internal_overhead: str = None
    __log_folder_for_application: str = None
    _internal_log_folder_for_ids: str = None
    __log_file_for_adame_overhead: str = None

    __readme_file: str = None
    __license_file: str = None
    __gitignore_file: str = None
    __dockercompose_file: str = None
    __renamed_items_file: str = None
    __volumes_folder: str = None
    __running_information_file: str = None
    __applicationprovidedsecurityinformation_file: str = None
    _internal_networktrafficgeneratedrules_file: str = None
    __networktrafficcustomrules_file: str = None
    __propertiesconfiguration_file: str = None
    __configurationfolder_name: str = "Configuration"
    __gitconfiguration_filename: str = ".gitconfig"
    __gitconfig_file: str = None
    __metadata_file: str = None
    __metadata_filename: str = "FileMetadata.csv"

    __testrule_trigger_content: str = "adame_testrule_trigger_content_0117ae72-6d1a-4720-8942-610fe9711a01"
    __testrule_log_content: str = "adame_testrule_trigger_content_0217ae72-6d1a-4720-8942-610fe9711a02"
    __testrule_sid: str = "8979665"
    __localipaddress_placeholder: str = "__.builtin.localipaddress.__"
    __gitkeep_filename = ".gitkeep"
    __path_separator = "/"
    # </constants>

    # <properties>

    verbose: bool = False
    diagnostic: bool = False
    encoding: str = "utf-8"
    format_datetimes_to_utc: bool = True

    __test_mode: bool = False
    _internal_demo_mode: bool = False
    _internal_sc: ScriptCollectionCore = ScriptCollectionCore()
    __mock_process_queries: list = list()
    __gpgkey_of_owner_is_available: bool = False
    __remote_address_is_available: bool = False

    # </properties>

    # <initialization>

    def __init__(self):
        self.set_test_mode(False)

    # </initialization>

    # <create-command>
    @GeneralUtilities.check_arguments
    def create(self, name: str, folder: str, image: str, owner: str, gpgkey_of_owner: str = None) -> int:
        self.__check_whether_execution_is_possible()
        self.__verbose_log_start_by_create_command(name, folder, image, owner)
        return self.__execute_task("Create", lambda: self.__create(name, folder, image, owner, gpgkey_of_owner))

    @GeneralUtilities.check_arguments
    def __create(self, name: str, folder: str, image: str, owner: str, gpgkey_of_owner: str) -> None:
        if name is None:
            raise ValueError("Argument 'name' is not defined")
        else:
            name = name.replace(" ", "-")

        if folder is None:
            raise ValueError("Argument 'folder' is not defined")
        else:
            if (os.path.isdir(folder) and not GeneralUtilities.folder_is_empty(folder)):
                raise ValueError(f"Folder '{folder}' does already have content")
            else:
                GeneralUtilities.ensure_directory_exists(folder)

        if image is None:
            raise ValueError("Argument 'image' is not defined")

        if owner is None:
            raise ValueError("Argument 'owner' is not defined")

        if gpgkey_of_owner is None:
            gpgkey_of_owner = ""

        configuration_file = GeneralUtilities.resolve_relative_path_from_current_working_directory(os.path.join(folder, "Configuration", "Adame.configuration"))

        self.__create_adame_configuration_file(configuration_file, name, owner)

        GeneralUtilities.ensure_directory_exists(self.__security_related_configuration_folder)

        self.__create_file_in_repository(self.__readme_file, self.__get_readme_file_content(self.__configuration, image))
        self.__create_file_in_repository(self.__license_file, self.__get_license_file_content(self.__configuration))
        self.__create_file_in_repository(self.__gitignore_file, self.__get_gitignore_file_content())
        self.__create_file_in_repository(self.__dockercompose_file, self.__get_dockercompose_file_content(image))
        self.__create_file_in_repository(self.__metadata_file, "")
        self.__create_file_in_repository(self.__applicationprovidedsecurityinformation_file, "")
        self.__create_file_in_repository(self._internal_networktrafficgeneratedrules_file, "")
        self.__create_file_in_repository(self.__networktrafficcustomrules_file, "")
        self.__create_file_in_repository(self.__propertiesconfiguration_file, "")
        self.__create_file_in_repository(self.__running_information_file, self.__get_running_information_file_content(False, False))

        self.__create_file_in_repository(os.path.join(self.__log_folder_for_application, self.__gitkeep_filename), "")
        self.__create_file_in_repository(os.path.join(self._internal_log_folder_for_ids, self.__gitkeep_filename), "")
        self.__create_file_in_repository(os.path.join(self.__log_folder_for_internal_overhead, self.__gitkeep_filename), "")

        self.__create_securityconfiguration_file(gpgkey_of_owner)

        self.__load_securityconfiguration()
        self.__create_file_in_repository(self.__gitconfig_file, self.__get_gitconfig_file_content(owner,  self.__gpgkey_of_owner_is_available, gpgkey_of_owner))

        self._internal_sc.set_permission(self._internal_log_folder_for_ids, "666", True)

        self.__start_program_synchronously("git", "init", self.__repository_folder)
        self.__set_git_configuration()  # TODO Improve: Call this function always before executing git commands (except creating a repository)

        self.__commit(f"Initial commit for app-repository of {name} managed by Adame in folder '{self.__repository_folder}' on host '{self.__get_hostname()}'")

    # </create-command>

    # <start-command>

    @GeneralUtilities.check_arguments
    def start(self, configurationfile: str) -> int:
        self.__check_whether_execution_is_possible()
        self.__check_configurationfile_argument(configurationfile)

        self.__verbose_log_start_by_configuration_file(configurationfile)
        self.__load_configuration(configurationfile)
        return self.__execute_task("Start", self.__start)

    @GeneralUtilities.check_arguments
    def __start(self) -> None:
        if self.__securityconfiguration.getboolean(self.__securityconfiguration_section_general, self.__securityconfiguration_section_general_key_enabledids):
            ids_is_running = self.__ensure_ids_is_running()
        else:
            ids_is_running = False
        container_is_running = self.__ensure_container_is_running()
        self.__log_running_state(container_is_running, ids_is_running, "Started")

    # </start-command>

    # <stop-command>

    @GeneralUtilities.check_arguments
    def stop(self, configurationfile: str) -> int:
        self.__check_whether_execution_is_possible()
        self.__check_configurationfile_argument(configurationfile)

        self.__verbose_log_start_by_configuration_file(configurationfile)
        self.__load_configuration(configurationfile)
        return self.__execute_task("Stop", self.__stop)

    @GeneralUtilities.check_arguments
    def __stop(self) -> None:
        container_is_running = not self.__ensure_container_is_not_running()
        ids_is_running = False
        if self.__securityconfiguration.getboolean(self.__securityconfiguration_section_general, self.__securityconfiguration_section_general_key_enabledids):
            ids_is_running = not self.__ensure_ids_is_not_running()
        self.__log_running_state(container_is_running, ids_is_running, "Stopped")

    # </stop>

    # <applyconfiguration-command>

    @GeneralUtilities.check_arguments
    def applyconfiguration(self, configurationfile: str) -> int:
        self.__check_whether_execution_is_possible()
        self.__check_configurationfile_argument(configurationfile)

        self.__verbose_log_start_by_configuration_file(configurationfile)
        self.__load_configuration(configurationfile)
        return self.__execute_task("ApplyConfiguration", self.__applyconfiguration)

    @GeneralUtilities.check_arguments
    def __applyconfiguration(self) -> None:
        self.__regenerate_networktrafficgeneratedrules_filecontent()
        if not self.__check_siem_is_reachable():
            self.__log_warning("The SIEM-connection is missing", False, True, True)
        self.__commit("Reapplied configuration")

    # </applyconfiguration-command>

    # <startadvanced-command>

    @GeneralUtilities.check_arguments
    def startadvanced(self, configurationfile: str) -> int:
        self.__check_whether_execution_is_possible()
        self.__check_configurationfile_argument(configurationfile)

        self.__verbose_log_start_by_configuration_file(configurationfile)
        self.__load_configuration(configurationfile)
        return self.__execute_task("StartAdvanced", self.__startadvanced)

    @GeneralUtilities.check_arguments
    def __startadvanced(self) -> None:
        self.__stopadvanced()
        self.__applyconfiguration()
        self.__restore_metadata()
        self.__start()

    # </startadvanced-command>

    # <stopadvanced-command>

    @GeneralUtilities.check_arguments
    def stopadvanced(self, configurationfile: str) -> int:
        self.__check_whether_execution_is_possible()
        self.__check_configurationfile_argument(configurationfile)

        self.__verbose_log_start_by_configuration_file(configurationfile)
        self.__load_configuration(configurationfile)
        return self.__execute_task("StopAdvanced", self.__stopadvanced)

    @GeneralUtilities.check_arguments
    def __stopadvanced(self) -> None:
        self.__stop()
        self.__commit("Saved changes")  # FIXME this saves filemetadata. saving filemetadata should only be done when the container really was running
        self.__exportlogs()

    # </stopadvanced-command>

    # <checkintegrity-command>

    @GeneralUtilities.check_arguments
    def checkintegrity(self, configurationfile: str) -> int:
        self.__check_whether_execution_is_possible()
        self.__check_configurationfile_argument(configurationfile)

        self.__verbose_log_start_by_configuration_file(configurationfile)
        self.__load_configuration(configurationfile)
        return self.__execute_task("CheckIntegrity", self.__checkintegrity)

    @GeneralUtilities.check_arguments
    def __checkintegrity(self) -> None:
        self.__check_integrity_of_repository(7)

    # </checkintegrity-command>

    # <exportlogs-command>

    @GeneralUtilities.check_arguments
    def exportlogs(self, configurationfile: str) -> int:
        self.__check_whether_execution_is_possible()
        self.__check_configurationfile_argument(configurationfile)

        self.__verbose_log_start_by_configuration_file(configurationfile)
        self.__load_configuration(configurationfile)
        return self.__execute_task("ExportLogs", self.__exportlogs)

    @GeneralUtilities.check_arguments
    def __exportlogs(self) -> None:
        self.__log_information("Export logs", False, True, True)

        log_target_folder_base = self.__configuration[self.__configuration_section_general][self.__configuration_section_general_key_logtargetfolder]
        if GeneralUtilities.string_has_content(log_target_folder_base):
            self.__log_information(f"Export logs to log-folder '{log_target_folder_base}'.", False, True, True)
            log_folders: list[str] = []
            log_folders.append(self.__log_folder_for_internal_overhead)
            log_folders.append(self._internal_log_folder_for_ids)
            log_folders.append(self.__log_folder_for_application)
            timebased_subfolder: str = GeneralUtilities.get_time_based_logfilename("Log", self.format_datetimes_to_utc)
            for log_folder in log_folders:
                self.__export_files_from_log_folder(log_folder, log_target_folder_base, timebased_subfolder)

        siemaddress = self.__securityconfiguration[self.__securityconfiguration_section_general][self.__securityconfiguration_section_general_key_siemaddress]
        siemfolder = self.__securityconfiguration[self.__securityconfiguration_section_general][self.__securityconfiguration_section_general_key_siemfolder]
        siemuser = self.__securityconfiguration[self.__securityconfiguration_section_general][self.__securityconfiguration_section_general_key_siemuser]
        siem_export_enabled: bool = GeneralUtilities.string_has_content(siemaddress) and GeneralUtilities.string_has_content(siemfolder) and GeneralUtilities.string_has_content(siemuser)
        if siem_export_enabled:
            self.__log_information("Export logs to SIEM", False, True, True)
            if (not self.__tool_exists_in_path("rsync")):
                self.__log_warning("rsync is not available", False, True, True)
                return
            if (not self.__check_siem_is_reachable()):
                self.__log_warning("The log-files can not be exported due to a missing SIEM-connection", False, True, True)
                return
            log_files = GeneralUtilities.get_direct_files_of_folder(self.__log_folder_for_internal_overhead) + \
                GeneralUtilities.get_direct_files_of_folder(self._internal_log_folder_for_ids)+GeneralUtilities.get_direct_files_of_folder(self.__log_folder_for_application)
            sublogfolder = GeneralUtilities.get_time_based_logfilename("Log", self.format_datetimes_to_utc)
            for log_file in log_files:
                if os.path.basename(log_file) != self.__gitkeep_filename:
                    exitcode = self.__start_program_synchronously("rsync", f'--compress --verbose --rsync-path="mkdir -p {siemfolder}/{sublogfolder}/ && rsync" -e ssh {log_file} {siemuser}@{siemaddress}:{siemfolder}/{sublogfolder}', "", False)[0]
                    if (exitcode == 0):
                        self.__log_information(f"Logfile '{log_file}' was successfully exported to {siemaddress}", True, True, True)
                        os.remove(log_file)
                    else:
                        self.__log_warning(f"Exporting Log-file '{log_file}' to {siemaddress} resulted in exitcode {str(exitcode)}", False, True, True)

        self.__log_information("Finished exporting logs", False, True, True)

    @GeneralUtilities.check_arguments
    def __export_files_from_log_folder(self, local_log_folder: str, log_target_folder_base: str, timebased_subfolder: str) -> None:
        appname: str = self.__configuration[self.__configuration_section_general][self.__configuration_section_general_key_name]
        log_name: str = os.path.basename(local_log_folder)
        target_folder: str = GeneralUtilities.resolve_relative_path(f"./{appname}/{timebased_subfolder}/{log_name}", log_target_folder_base)
        all_log_files = [file_to_export for file_to_export in GeneralUtilities.get_all_files_of_folder(local_log_folder) if ((not file_to_export.endswith(self.__gitkeep_filename)) and (not file_to_export.endswith(".gitignore")))]
        for log_file in all_log_files:
            self.__log_information(f"Export log-file '{log_file}' to log-folder...", True, True, True)
            target_file: str = GeneralUtilities.resolve_relative_path("./"+os.path.relpath(log_file, local_log_folder), target_folder)
            final_target_folder = os.path.dirname(target_file)
            GeneralUtilities.ensure_directory_exists(final_target_folder)
            shutil.copy2(log_file, final_target_folder)
            GeneralUtilities.ensure_file_does_not_exist(log_file)

    # </exportlogs-command>

    # <diagnosis-command>

    @GeneralUtilities.check_arguments
    def diagnosis(self, configurationfile: str) -> int:
        self.__check_whether_execution_is_possible()
        self.__verbose_log_start_by_configuration_file(configurationfile)
        if configurationfile is not None:
            self.__load_configuration(configurationfile)
        return self.__execute_task("Diagnosis", self.__diagnosis)

    @GeneralUtilities.check_arguments
    def __diagnosis(self) -> None:
        if not self.__adame_general_diagonisis():
            raise ValueError("General diagnosis found discrepancies")
        if self.__configuration is not None:
            if not self.__adame_repository_diagonisis():
                raise ValueError(f"General diagnosis found discrepancies in repository '{self.__repository_folder}'")

    # </checkintegrity-command>

    # <checkout-command>

    @GeneralUtilities.check_arguments
    def checkout(self, configurationfile: str, branch: str) -> int:
        self.__check_whether_execution_is_possible()
        self.__verbose_log_start_by_configuration_file(configurationfile)
        if configurationfile is not None:
            self.__load_configuration(configurationfile)
        return self.__execute_task("Checkout", lambda: self.__checkout(branch))

    @GeneralUtilities.check_arguments
    def __checkout(self, branch: str) -> None:
        self.__stopadvanced()
        self.__git_checkout(branch)
        self.__restore_metadata()

    # </checkout-command>

    # <other-functions>

    @GeneralUtilities.check_arguments
    def set_test_mode(self, test_mode_enabled: bool) -> None:
        "This function is for test-purposes only"
        self.__test_mode = test_mode_enabled
        self._internal_sc.mock_program_calls = self.__test_mode
        self._internal_sc.execute_program_really_if_no_mock_call_is_defined = self.__test_mode

    @GeneralUtilities.check_arguments
    def _internal_register_mock_process_query(self, process_id: int, command: str) -> None:
        "This function is for test-purposes only"
        process = Adame.__process()
        process.process_id = process_id
        process.command = command
        resultlist = list()
        resultlist.append(process)
        self.__mock_process_queries.append(resultlist)

    @GeneralUtilities.check_arguments
    def _internal_verify_no_pending_mock_process_queries(self) -> None:
        "This function is for test-purposes only"
        if (len(self.__mock_process_queries) > 0):
            for mock_query_result in self.__mock_process_queries:
                raise AssertionError("The following mock-process-queries were not queried:\n    " +
                                     ",\n    ".join([f"'pid: {r.process_id}, command: '{r.command}'" for r in mock_query_result]))

    # </other-functions>

    # <helper-functions>

    @GeneralUtilities.check_arguments
    def __git_checkout(self, branch: str) -> None:
        self.__start_program_synchronously("git", f"checkout {branch}", self.__repository_folder, True)

    @GeneralUtilities.check_arguments
    def _internal_ensure_git_folder_are_escaped(self, volumes_folder: str, renamed_items_file: str) -> dict[str, str]:
        result: dict[str, str] = None
        self.__log_information("Ensure git-folders are escaped...", True, True, True)
        if os.path.isdir(volumes_folder) and not os.path.isfile(renamed_items_file):
            self.__log_information("Escape git-folders...", True, True, True)
            renamed_items = self._internal_sc.escape_git_repositories_in_folder(volumes_folder)
            if 0 < len(renamed_items):
                prefix_length = len(volumes_folder)
                renamed_items_with_relative_paths: dict[str, str] = dict[str, str]()
                for renamed_item_key, renamed_item_value in renamed_items.items():
                    if not renamed_item_key.startswith(volumes_folder):
                        self.__log_warning(f'Renamed item "{renamed_item_key}" does not start with "{volumes_folder}"', False, True, True)
                    if not renamed_item_value.startswith(volumes_folder):
                        self.__log_warning(f'Renamed item "{renamed_item_value}" does not start with "{volumes_folder}"', False, True, True)
                    renamed_item_key_relative = f"./{renamed_item_key[prefix_length+1:]}"
                    renamed_item_value_relative = f"./{renamed_item_value[prefix_length+1:]}"
                    renamed_items_with_relative_paths[renamed_item_key_relative] = renamed_item_value_relative
                result = renamed_items_with_relative_paths
                GeneralUtilities.ensure_file_exists(renamed_items_file)
                GeneralUtilities.write_lines_to_file(renamed_items_file, [f"{key};{value}" for key, value in renamed_items_with_relative_paths.items()])
            else:
                GeneralUtilities.ensure_file_exists(renamed_items_file)
        else:
            self.__log_information("No folders for escaping available.", True, True, True)
        return result

    @GeneralUtilities.check_arguments
    def _internal_ensure_git_folder_are_deescaped(self, volumes_folder: str, renamed_items_file: str) -> None:
        self.__log_information("Ensure git-folders are deescaped...", True, True, True)
        if os.path.isfile(renamed_items_file):
            self.__log_information("Deescape git-folders...", True, True, True)
            lines: list[list[str]] = GeneralUtilities.read_csv_file(renamed_items_file, False, False, False)
            # TODO sort list to ensure there are no filenotfound-exceptions when a renamed file will is attempted to be renamed in an already renamed folder
            for line in lines:
                key_relative = line[0]
                value_relative = line[1]
                key_absolute = GeneralUtilities.resolve_relative_path(key_relative, volumes_folder)
                value_absolute = GeneralUtilities.resolve_relative_path(value_relative, volumes_folder)
                os.rename(key_absolute, value_absolute)
            GeneralUtilities.ensure_file_does_not_exist(renamed_items_file)
        else:
            self.__log_information("No folders for deescaping available.", True, True, True)

    @GeneralUtilities.check_arguments
    def __save_metadata(self) -> None:
        return  # disabled due to condition because escaping does not work properly (rename .git to .gitx does not work properly and the permissions-restoring does also not seem to work.
        self.__log_information("Save metadata...", True, True, True)  # pylint: disable=unreachable
        self._internal_ensure_git_folder_are_escaped(self.__volumes_folder, self.__renamed_items_file)
        self._internal_sc.export_filemetadata(self.__repository_folder, self.__metadata_file, self.encoding, self.__use_file)
        content = GeneralUtilities.read_text_from_file(self.__metadata_file, self.encoding)
        content = content.replace("\\", self.__path_separator)
        GeneralUtilities.write_text_to_file(self.__metadata_file, content, self.encoding)

    @GeneralUtilities.check_arguments
    def __restore_metadata(self) -> None:
        return   # disabled due to condition because escaping does not work properly (rename .git to .gitx does not work properly and the permissions-restoring does also not seem to work.
        self.__log_information("Restore metadata...", True, True, True)  # pylint: disable=unreachable
        self._internal_sc.restore_filemetadata(self.__repository_folder, self.__metadata_file, False, self.encoding)
        self._internal_ensure_git_folder_are_deescaped(self.__volumes_folder, self.__renamed_items_file)

    @GeneralUtilities.check_arguments
    def __use_file(self, repository_folder: str, file_or_folder: str) -> bool:
        if (GeneralUtilities.string_is_none_or_whitespace(file_or_folder)):
            return True
        if (file_or_folder == ".git" or file_or_folder.replace("\\", self.__path_separator).startswith(f".git{self.__path_separator}")):
            return False
        if Path(os.path.join(repository_folder, file_or_folder)).is_symlink():
            return False
        else:
            return not self._internal_sc.file_is_git_ignored(file_or_folder, repository_folder)

    @GeneralUtilities.check_arguments
    def __check_whether_execution_is_possible(self) -> None:
        if self.__test_mode:
            return
        if (not GeneralUtilities.current_user_has_elevated_privileges()):
            raise ValueError("Adame requries elevated privileges to get executed")

    @GeneralUtilities.check_arguments
    def __log_running_state(self, container_is_running: bool, ids_is_running: bool, action: str) -> None:
        GeneralUtilities.write_text_to_file(self.__running_information_file, self.__get_running_information_file_content(container_is_running, ids_is_running))
        self._internal_sc.git_unstage_all_changes(self.__repository_folder)
        self.__commit(f"{action} container (Container-process: {str(container_is_running)}; IDS-process: {str(ids_is_running)})", True, 1, not container_is_running)

    @GeneralUtilities.check_arguments
    def __adame_general_diagonisis(self) -> bool:
        if (not self.__check_whether_required_tools_for_adame_are_available()):
            return False
        # Add other checks if required
        return True

    @GeneralUtilities.check_arguments
    def __adame_repository_diagonisis(self) -> bool:
        if not self.__check_whether_required_files_for_adamerepository_are_available():
            return False
        # Add other checks if required
        return True

    @GeneralUtilities.check_arguments
    def __check_whether_required_tools_for_adame_are_available(self) -> bool:
        result = True
        if not self.__test_mode:
            return result
        tools = [
            "chmod",
            "chown",
            "docker",
            "git",
        ]
        recommended_tools = [
            "gpg",
            "rsync",
            "ssh",
            "snort",
        ]
        for tool in tools:
            if not self.__tool_exists_in_path(tool):
                self.__log_error(f"Tool '{tool}' is not available")
                result = False
        for tool in recommended_tools:
            if not self.__tool_exists_in_path(tool):
                self.__log_warning(f"Recommended tool '{tool}' is not available")
                result = False
        return result

    @GeneralUtilities.check_arguments
    def __check_whether_required_files_for_adamerepository_are_available(self) -> bool:
        # TODO Improve: Add checks for files like RunningInformation.txt etc.
        # Add other checks if required
        return True

    @GeneralUtilities.check_arguments
    def __check_configurationfile_argument(self, configurationfile: str) -> None:
        if configurationfile is None:
            raise ValueError("Argument 'configurationfile' is not defined")
        if not os.path.isfile(configurationfile):
            raise FileNotFoundError(f"File '{configurationfile}' does not exist")

    @GeneralUtilities.check_arguments
    def __check_integrity_of_repository(self, amount_of_days_of_history_to_check: int = None) -> None:
        """This function checks the integrity of the app-repository.
This function is idempotent."""
        until = datetime.now()
        since = until - timedelta(days=amount_of_days_of_history_to_check)
        commit_hashs_to_check_in_given_interval = self._internal_sc.get_commit_ids_between_dates(self.__repository_folder, until, since)
        for commithash in commit_hashs_to_check_in_given_interval:
            if not self._internal_sc.commit_is_signed_by_key(self.__repository_folder, commithash, self.__configuration[self.__securityconfiguration_section_general][self.__configuration_section_general_key_gpgkeyofowner]):
                self.__log_warning(f"The app-repository '{self.__repository_folder}' contains the unsigned commit {commithash}", False, True, True)

    @GeneralUtilities.check_arguments
    def get_entire_testrule_trigger_content(self) -> str:
        return f"testrule_content_{self.__testrule_trigger_content}_{self.__configuration[self.__configuration_section_general][self.__configuration_section_general_key_repositoryid]}"

    @GeneralUtilities.check_arguments
    def get_entire_testrule_trigger_answer(self) -> str:
        return f"testrule_answer_{self.__testrule_log_content}_{self.__configuration[self.__configuration_section_general][self.__configuration_section_general_key_repositoryid]}"

    @GeneralUtilities.check_arguments
    def __regenerate_networktrafficgeneratedrules_filecontent(self) -> None:
        """This function regenerates the content of the file Networktraffic.Generated.rules.
This function is idempotent."""
        customrules = GeneralUtilities.read_text_from_file(self.__networktrafficcustomrules_file, self.encoding)
        applicationprovidedrules = "# (not implemented yet)"  # TODO Improve: Implement usage of application-provided security-information
        local_ip_address = self.__get_local_ip_address()
        file_content = f"""# Rules file for Snort generated by Adame.
# Do not modify this file. Changes will be overwritten.

# --- Global configuration ---
# TODO include {self.__securityconfiguration[self.__securityconfiguration_section_snort][self.__securityconfiguration_section_snort_key_globalconfigurationfile]}

# --- Internal rules ---

# Test-rule for functionality test:
# TODO alert tcp any any -> {self.__localipaddress_placeholder} any (sid: {self.__testrule_sid}; content: "{self.get_entire_testrule_trigger_content()}"; msg: "{self.get_entire_testrule_trigger_answer()}";)

# --- Application-provided rules ---
{applicationprovidedrules}

# --- Custom created rules ---
{customrules}
"""
        file_content = file_content.replace(self.__localipaddress_placeholder, local_ip_address)  # replacement to allow to use this variable in the customrules.
        GeneralUtilities.write_text_to_file(self._internal_networktrafficgeneratedrules_file, file_content, self.encoding)

    @GeneralUtilities.check_arguments
    def __check_siem_is_reachable(self) -> bool:
        """This function checks wether the SIEM is available."""
        siemaddress = self.__securityconfiguration[self.__securityconfiguration_section_general][self.__securityconfiguration_section_general_key_siemaddress]
        if GeneralUtilities.string_is_none_or_whitespace(siemaddress):
            return False
        return True  # TODO Improve: Return true if and only if siemaddress is available to receive log-files

    @GeneralUtilities.check_arguments
    def __ensure_container_is_running(self) -> bool:
        self.__ensure_container_is_not_running()
        return self.__start_container()

    @GeneralUtilities.check_arguments
    def __ensure_container_is_not_running(self) -> bool:
        if (self._internal_container_is_running()):
            return self.__stop_container()
        return True

    @GeneralUtilities.check_arguments
    def __ensure_ids_is_running(self) -> bool:
        """This function ensures that the intrusion-detection-system (ids) is running and the rules will be applied correctly."""
        self.__ensure_ids_is_not_running()
        result = self.__start_ids()
        self.__test_ids()
        return result

    @GeneralUtilities.check_arguments
    def __ensure_ids_is_not_running(self) -> bool:
        """This function ensures that the intrusion-detection-system (ids) is not running anymore."""
        if (self._internal_ids_is_running()):
            return self.__stop_ids()
        return True

    @GeneralUtilities.check_arguments
    def _internal_container_is_running(self) -> bool:
        return self.__get_stored_running_processes()[0]

    @GeneralUtilities.check_arguments
    def _internal_ids_is_running(self) -> bool:
        ids = self.__securityconfiguration.get(self.__securityconfiguration_section_general, self.__securityconfiguration_section_general_key_idsname)
        if (ids == "snort"):
            return self.__get_stored_running_processes()[1]
        return False

    @GeneralUtilities.check_arguments
    def __start_ids(self) -> bool:
        if self.verbose:
            GeneralUtilities.write_message_to_stdout("Start ids...")
        success = True
        ids = self.__securityconfiguration.get(self.__securityconfiguration_section_general, self.__securityconfiguration_section_general_key_idsname)
        if (ids == "snort"):
            if self.format_datetimes_to_utc:
                utc_argument = " -U"
            else:
                utc_argument = ""
            if self.verbose:
                verbose_argument = " -v"
            else:
                verbose_argument = ""
            networkinterface = self.__configuration[self.__configuration_section_general][self.__configuration_section_general_key_networkinterface]
            success = self.__run_system_command(
                "snort", f'-D -i {networkinterface} -c "{self._internal_networktrafficgeneratedrules_file}" -l "{self._internal_log_folder_for_ids}"{utc_argument}{verbose_argument} -x -y -K ascii')
        if success:
            self.__log_information("IDS was started", False, True, True)
        else:
            self.__log_warning("IDS could not be started")
        return success

    @GeneralUtilities.check_arguments
    def __stop_ids(self) -> bool:
        self.__log_information("Stop ids...", True, True, True)
        result = 0
        ids = self.__securityconfiguration.get(self.__securityconfiguration_section_general, self.__securityconfiguration_section_general_key_idsname)
        if (ids == "snort"):
            for process in self.__get_running_processes():
                if (process.command.startswith("snort") and self.__repository_folder in process.command):
                    result = self.__start_program_synchronously("kill", f"-TERM {process.process_id}")[0]
                    if result != 0:
                        result = self.__start_program_synchronously("kill", f"-9 {process.process_id}")[0]
        result = 0
        success = result == 0
        if success:
            self.__log_information("IDS was stopped", False, True, True)
        else:
            self.__log_warning("IDS could not be stopped")
        return success

    @GeneralUtilities.check_arguments
    def __test_ids(self) -> None:
        pass  # TODO Improve: Test if a specific test-rule will be applied by sending a package to the docker-container which should be result in a log-folder

    @GeneralUtilities.check_arguments
    def __run_system_command(self, program: str, argument: str, working_directory: str = None) -> bool:
        """Starts a program which should be organize its asynchronous execution by itself. This function ensures that the asynchronous program will not get terminated when Adame terminates."""
        if (working_directory is None):
            working_directory = os.getcwd()
        working_directory = GeneralUtilities.resolve_relative_path_from_current_working_directory(working_directory)
        self.__log_information(f"Start '{working_directory}>{program} {argument}'", True, True, True)
        if self.__test_mode:
            self.__start_program_synchronously(program, argument, working_directory)  # mocks defined in self.__sc will be used here when running the unit-tests
        else:
            original_cwd = os.getcwd()
            if (GeneralUtilities.string_is_none_or_whitespace(working_directory)):
                working_directory = original_cwd
            os.chdir(working_directory)
            try:
                os.system(f"{program} {argument}")
            finally:
                os.chdir(original_cwd)
        return True  # TODO Improve: Find a possibility to really check that this program is currently running

    @GeneralUtilities.check_arguments
    def __get_stored_running_processes(self) -> tuple:
        # TODO Improve: Do a real check, not just reading this information from a file.
        lines = GeneralUtilities.read_text_from_file(self.__running_information_file).splitlines()
        processid_of_container_as_string = False
        processid_of_ids_as_string = False
        for line in lines:
            if ":" in line:
                splitted = line.split(":")
                value_as_string = splitted[1].strip()
                if GeneralUtilities.string_has_nonwhitespace_content(value_as_string):
                    value = GeneralUtilities.string_to_boolean(value_as_string)
                    if splitted[0] == "Container-process":
                        processid_of_container_as_string = value
                    if splitted[0] == "IDS-process":
                        processid_of_ids_as_string = value
        return (processid_of_container_as_string, processid_of_ids_as_string)

    @GeneralUtilities.check_arguments
    def __get_running_information_file_content(self, container_is_running: bool, ids_is_running: int) -> str:
        container_is_running_as_string = str(container_is_running)
        ids_is_running_as_string = str(ids_is_running)
        return f"""Container-process:{container_is_running_as_string}
IDS-process:{ids_is_running_as_string}
"""

    @GeneralUtilities.check_arguments
    def __get_gitconfig_file_content(self, username: str, gpgkey_of_owner_is_available: bool, gpgkey_of_owner: str):
        return f"""[core]
    filemode = false
    symlinks = true
[commit]
    gpgsign = {str(gpgkey_of_owner_is_available).lower()}
[user]
    name = {username}
    signingkey = {gpgkey_of_owner}
"""

    @GeneralUtilities.check_arguments
    def __create_adame_configuration_file(self, configuration_file: str, name: str, owner: str) -> None:
        self.__configuration_file = configuration_file
        GeneralUtilities.ensure_directory_exists(os.path.dirname(self.__configuration_file))
        local_configparser = ConfigParser()

        local_configparser.add_section(self.__configuration_section_general)
        local_configparser[self.__configuration_section_general][self.__configuration_section_general_key_formatversion] = version
        local_configparser[self.__configuration_section_general][self.__configuration_section_general_key_repositoryversion] = "1.0.0"
        local_configparser[self.__configuration_section_general][self.__configuration_section_general_key_name] = name
        local_configparser[self.__configuration_section_general][self.__configuration_section_general_key_owner] = owner
        local_configparser.set(self.__configuration_section_general, self.__configuration_section_general_key_maximalexpectedstartduration,
                               str(self.__configuration_section_general_key_maximalexpectedstartduration_defaultvalue))

        if self._internal_demo_mode:
            local_configparser[self.__configuration_section_general][self.__configuration_section_general_key_repositoryid] = "de30de30-de30-de30-de30-de30de30de30"
        else:
            local_configparser[self.__configuration_section_general][self.__configuration_section_general_key_repositoryid] = str(uuid.uuid4())
        local_configparser[self.__configuration_section_general][self.__configuration_section_general_key_networkinterface] = "eth0"
        local_configparser[self.__configuration_section_general][self.__configuration_section_general_key_prescript] = ""
        local_configparser[self.__configuration_section_general][self.__configuration_section_general_key_postscript] = ""

        with open(self.__configuration_file, 'w+', encoding=self.encoding) as configfile:
            local_configparser.write(configfile)
        self.__log_information(f"Created file '{self.__configuration_file}'", True)

        self.__load_configuration(self.__configuration_file, False)

    @GeneralUtilities.check_arguments
    def __verbose_log_start_by_configuration_file(self, configurationfile: str) -> None:
        self.__log_information(f"Started Adame with configurationfile '{configurationfile}'", True)

    @GeneralUtilities.check_arguments
    def __verbose_log_start_by_create_command(self, name: str, folder: str, image: str, owner: str) -> None:
        self.__log_information(
            f"Started Adame with  name='{GeneralUtilities.str_none_safe(name)}', folder='{GeneralUtilities.str_none_safe(folder)}', image='{GeneralUtilities.str_none_safe(image)}', owner='{GeneralUtilities.str_none_safe(owner)}'", True)

    @GeneralUtilities.check_arguments
    def __save_configfile(self, file: str, configuration: configparser.ConfigParser) -> None:
        with open(file, 'w', encoding=self.encoding) as file_writer:
            configuration.write(file_writer)

    @GeneralUtilities.check_arguments
    def __migrate_overhead(self, sourceVersion, target_version, function) -> None:
        try:
            self.__log_information(f"Start migrating from v{sourceVersion} to v{target_version}", False, True, True)
            function()
            self.__commit(f"Migrated from v{sourceVersion} to v{target_version}", True, no_changes_behavior=1, overhead=False)
            return target_version
        except Exception as exception:
            self.__log_exception(f"Error while migrating from v{sourceVersion} to v{target_version}", exception, False, True, True)
            raise

    @GeneralUtilities.check_arguments
    def __migrate_to_v_1_2_3(self, configuration_file: str, configuration_v_1_2_2: configparser.ConfigParser) -> None:
        configuration_v_1_2_2.set(self.__configuration_section_general, self.__configuration_section_general_key_maximalexpectedstartduration, str(self.__configuration_section_general_key_maximalexpectedstartduration_defaultvalue))
        self.__save_configfile(configuration_file, configuration_v_1_2_2)

    def __migrate_to_v_1_2_52(self, configuration_file: str, previous_config: configparser.ConfigParser) -> None:
        previous_config.set(self.__configuration_section_general, self.__configuration_section_general_key_logtargetfolder, "")
        self.__save_configfile(configuration_file, previous_config)

    @GeneralUtilities.check_arguments
    def __migrate_configuration_if_required(self, configuration_file: str, configuration: configparser.ConfigParser) -> configparser.ConfigParser:
        # Migration should only be done when the repository already exist and the repository-creation-process is already completed.
        if (os.path.isdir(os.path.join(self.__repository_folder, ".git"))):
            config_format_version = parse(configuration.get(self.__configuration_section_general, self.__configuration_section_general_key_formatversion))
            adame_version = parse(version)
            # Migration should only be done when the current adame-version and the repository-format-version differ.
            if adame_version != config_format_version:
                if config_format_version > adame_version:
                    raise ValueError(
                        f"Can not run {product_name} because the repository-format-version is greater than the current used version of {product_name} (v{version}). Please update {product_name} to the latest version.")
                if config_format_version < parse('1.2.2'):
                    raise ValueError("Migrations of repository-format-versions older than v1.2.2 are not supported")

                if config_format_version == parse('1.2.2'):
                    config_format_version = self.__migrate_overhead('1.2.2', '1.2.3', lambda:  self.__migrate_to_v_1_2_3(configuration_file, configuration))
                if config_format_version < parse('1.2.52'):
                    config_format_version = self.__migrate_overhead(config_format_version, '1.2.52', lambda:  self.__migrate_to_v_1_2_52(configuration_file, configuration))

                configuration.set(self.__configuration_section_general, self.__configuration_section_general_key_formatversion, version)
                self.__save_configfile(configuration_file, configuration)

                configuration = configparser.ConfigParser()
                configuration.read(configuration_file)
                configuration.set(self.__configuration_section_general, self.__configuration_section_general_key_formatversion, version)
                self.__save_configfile(configuration_file, configuration)
                self.__commit(f"Updated repository-version to v{version}", True, no_changes_behavior=1, overhead=False)
        return configuration

    @GeneralUtilities.check_arguments
    def __load_configuration(self, configurationfile: str, load_securityconfiguration: bool = True) -> None:
        try:
            self.__log_information("Load configuration...", True, True, True)
            configurationfile = GeneralUtilities.resolve_relative_path_from_current_working_directory(configurationfile)
            if not os.path.isfile(configurationfile):
                raise ValueError(F"'{configurationfile}' does not exist")
            self.__configuration_file = configurationfile
            self.__repository_folder = os.path.dirname(os.path.dirname(configurationfile))
            configuration = configparser.ConfigParser()
            configuration.read(configurationfile)

            configuration = self.__migrate_configuration_if_required(self.__configuration_file, configuration)

            self.__configuration = configuration
            self._internal_configuration_folder = os.path.join(self.__repository_folder, self.__configurationfolder_name)
            self.__log_information(f"Configuration-folder: '{self._internal_configuration_folder}'", True, True, True)
            self.__security_related_configuration_folder = os.path.join(self._internal_configuration_folder, "Security")

            self.__readme_file = os.path.join(self.__repository_folder, "ReadMe.md")
            self.__license_file = os.path.join(self.__repository_folder, "License.txt")
            self.__gitignore_file = os.path.join(self.__repository_folder, ".gitignore")
            self.__volumes_folder = os.path.join(self._internal_configuration_folder, "Volumes")
            self.__running_information_file = os.path.join(self._internal_configuration_folder, "RunningInformation.txt")
            self.__dockercompose_file = os.path.join(self._internal_configuration_folder, "docker-compose.yml")
            self.__renamed_items_file = os.path.join(self.__volumes_folder, "RenamedItems.csv")
            self.__gitconfig_file = os.path.join(self._internal_configuration_folder, self.__gitconfiguration_filename)
            self.__metadata_file = os.path.join(self._internal_configuration_folder, self.__metadata_filename)
            self.__applicationprovidedsecurityinformation_file = os.path.join(
                self.__security_related_configuration_folder, "ApplicationProvidedSecurityInformation.xml")
            self._internal_networktrafficgeneratedrules_file = os.path.join(self.__security_related_configuration_folder, "Networktraffic.Generated.rules")
            self.__networktrafficcustomrules_file = os.path.join(self.__security_related_configuration_folder, "Networktraffic.Custom.rules")
            self.__propertiesconfiguration_file = os.path.join(self.__security_related_configuration_folder, "Security.configuration")

            self.__log_folder = os.path.join(self.__repository_folder, "Logs")

            self.__log_folder_for_application = os.path.join(self.__log_folder, "Application")
            GeneralUtilities.ensure_directory_exists(self.__log_folder_for_application)

            self._internal_log_folder_for_ids = os.path.join(self.__log_folder, "IDS")
            GeneralUtilities.ensure_directory_exists(self._internal_log_folder_for_ids)

            self.__log_folder_for_internal_overhead = os.path.join(self.__log_folder, "Overhead")
            GeneralUtilities.ensure_directory_exists(self.__log_folder_for_internal_overhead)
            self.__log_file_for_adame_overhead = GeneralUtilities.get_time_based_logfile_by_folder(
                self.__log_folder_for_internal_overhead, product_name, self.format_datetimes_to_utc)
            GeneralUtilities.ensure_file_exists(self.__log_file_for_adame_overhead)

            if load_securityconfiguration:
                self.__load_securityconfiguration()

        except Exception as exception:
            self.__log_exception(f"Error while loading configurationfile '{configurationfile}'.", exception)
            raise

    @GeneralUtilities.check_arguments
    def __load_securityconfiguration(self) -> None:
        try:
            self.__log_information("Load security-configuration...", True, True, True)
            securityconfiguration = configparser.ConfigParser()
            if not os.path.isfile(self.__propertiesconfiguration_file):
                raise ValueError(F"'{self.__propertiesconfiguration_file}' does not exist")
            securityconfiguration.read(self.__propertiesconfiguration_file)
            self.__securityconfiguration = securityconfiguration

            self.__gpgkey_of_owner_is_available = GeneralUtilities.string_has_nonwhitespace_content(
                self.__securityconfiguration[self.__securityconfiguration_section_general][self.__configuration_section_general_key_gpgkeyofowner])
            self.__remote_address_is_available = GeneralUtilities.string_has_nonwhitespace_content(
                self.__securityconfiguration[self.__securityconfiguration_section_general][self.__configuration_section_general_key_remoteaddress])

            if (not self.__gpgkey_of_owner_is_available):
                self.__log_warning(
                    "GPGKey of the owner of the repository is not set. It is highly recommended to set this value to ensure the integrity of the app-repository.")
            if (not self.__remote_address_is_available):
                self.__log_warning(
                    "Remote-address of the repository is not set. It is highly recommended to set this value to save the content of the app-repository externally.")

        except Exception as exception:
            self.__log_exception(f"Error while loading configurationfile '{self.__propertiesconfiguration_file}'.", exception)
            raise

    @GeneralUtilities.check_arguments
    def _internal_get_container_name(self) -> str:
        return self.__name_to_docker_allowed_name(self.__configuration.get(self.__configuration_section_general, self.__configuration_section_general_key_name))

    @GeneralUtilities.check_arguments
    def __get_dockercompose_file_content(self, image: str) -> str:
        name_as_docker_allowed_name = self._internal_get_container_name()
        return f"""version: '3.2'
services:
  {name_as_docker_allowed_name}:
    image: '{image}'
    container_name: '{name_as_docker_allowed_name}'
#     environment:
#       - variable=value
#     ports:
#       - 443:443
#     volumes:
#       - ./Volumes/Configuration:/DirectoryInContainer/Configuration
#       - ./Volumes/Data:/DirectoryInContainer/Data
#       - ./../Logs/Application:/DirectoryInContainer/Logs
"""

    @GeneralUtilities.check_arguments
    def __create_file_in_repository(self, file, filecontent) -> None:
        GeneralUtilities.write_text_to_file(file, filecontent, self.encoding)
        self.__log_information(f"Created file '{file}'", True)

    @GeneralUtilities.check_arguments
    def __get_license_file_content(self, configuration: ConfigParser) -> str:
        return f"""Owner of this repository and its content: {configuration.get(self.__configuration_section_general, self.__configuration_section_general_key_owner)}
Only the owner of this repository is allowed to read, use, change, publish this repository or its content.
Only the owner of this repository is allowed to change the license of this repository or its content.
"""

    @GeneralUtilities.check_arguments
    def __get_gitignore_file_content(self) -> str:
        return """Logs/Application/**
!Logs/Application/.gitkeep

Logs/IDS/**
!Logs/IDS/.gitkeep

Logs/Overhead/**
!Logs/Overhead/.gitkeep
"""

    @GeneralUtilities.check_arguments
    def __create_securityconfiguration_file(self, gpgkey_of_owner: str) -> None:
        securityconfiguration = ConfigParser()
        securityconfiguration.add_section(self.__securityconfiguration_section_general)
        securityconfiguration[self.__securityconfiguration_section_general][self.__securityconfiguration_section_general_key_enabledids] = "false"
        self.__add_default_ids_configuration_to_securityconfiguration(securityconfiguration, gpgkey_of_owner)

        with open(self.__propertiesconfiguration_file, 'w+', encoding=self.encoding) as configfile:
            securityconfiguration.write(configfile)

    @GeneralUtilities.check_arguments
    def __add_default_ids_configuration_to_securityconfiguration(self, securityconfiguration: ConfigParser, gpgkey_of_owner: str) -> None:
        securityconfiguration[self.__securityconfiguration_section_general][self.__configuration_section_general_key_gpgkeyofowner] = gpgkey_of_owner
        securityconfiguration[self.__securityconfiguration_section_general][self.__configuration_section_general_key_remoteaddress] = ""
        securityconfiguration[self.__securityconfiguration_section_general][self.__configuration_section_general_key_remotename] = "Backup"
        securityconfiguration[self.__securityconfiguration_section_general][self.__configuration_section_general_key_remotebranch] = "main"
        securityconfiguration[self.__securityconfiguration_section_general][self.__securityconfiguration_section_general_key_enabledids] = "true"
        securityconfiguration[self.__securityconfiguration_section_general][self.__securityconfiguration_section_general_key_idsname] = "snort"
        securityconfiguration[self.__securityconfiguration_section_general][self.__securityconfiguration_section_general_key_siemaddress] = ""
        securityconfiguration[self.__securityconfiguration_section_general][self.__securityconfiguration_section_general_key_siemfolder] = f"/var/log/{self.__get_hostname()}/{self._internal_get_container_name()}"
        securityconfiguration[self.__securityconfiguration_section_general][self.__securityconfiguration_section_general_key_siemuser] = "username_on_siem_system"
        securityconfiguration.add_section(self.__securityconfiguration_section_snort)
        securityconfiguration[self.__securityconfiguration_section_snort][self.__securityconfiguration_section_snort_key_globalconfigurationfile] = "/etc/snort/snort.conf"

    @GeneralUtilities.check_arguments
    def __get_hostname(self) -> str:
        if self._internal_demo_mode:
            return "Hostname"
        else:
            return socket.gethostname()

    @GeneralUtilities.check_arguments
    def __get_readme_file_content(self, configuration: ConfigParser, image: str) -> str:

        if self.__remote_address_is_available:
            remote_address_info = f"The data of this repository will be saved as backup in '{configuration.get(self.__securityconfiguration_section_general, self.__configuration_section_general_key_remoteaddress)}'."
        else:
            remote_address_info = "Currently there is no backup-address defined for backups of this repository."

        if self.__gpgkey_of_owner_is_available:
            gpgkey_of_owner_info = f"The integrity of the data of this repository will ensured using the GPG-key {configuration.get(self.__securityconfiguration_section_general, self.__configuration_section_general_key_gpgkeyofowner)}."
        else:
            gpgkey_of_owner_info = "Currently there is no GPG-key defined to ensure the integrity of this repository."

        return f"""# {configuration.get(self.__configuration_section_general, self.__configuration_section_general_key_name)}

## Purpose

This repository manages the application {configuration.get(self.__configuration_section_general, self.__configuration_section_general_key_name)} and its data.

## Technical information

### Image

The image {image} will be used.

### Backup

{remote_address_info}

### Integrity

{gpgkey_of_owner_info}

## License

The license of this repository is defined in the file `License.txt`.
"""

    @GeneralUtilities.check_arguments
    def __run_script_if_available(self, file: str, name: str):
        if (GeneralUtilities.string_has_content(file)):
            self.__log_information(f"Run {name} (File: {file})", False, True, True)
            file = GeneralUtilities.resolve_relative_path(file, self._internal_configuration_folder)
            self.__start_program_synchronously("sh", file, self._internal_configuration_folder, True)

    @GeneralUtilities.check_arguments
    def __stop_container(self) -> None:
        projectname = self._internal_get_container_name()
        # TODO do "docker compose -p {projectname} stop"
        # TODO for each container in compose-project save the output of "docker logs {containername}" in the log-folder in the file "Container_{containername}.log"
        result = self.__start_program_synchronously("docker", f"compose --project-name {projectname} down", self._internal_configuration_folder)[0]
        success = result == 0
        if success:
            self.__log_information("Container was stopped", False, True, True)
        else:
            self.__log_warning("Container could not be stopped")
        self.__run_script_if_available(self.__configuration.get(
            self.__configuration_section_general, self.__configuration_section_general_key_postscript), "PostScript")
        return success

    @GeneralUtilities.check_arguments
    def __start_container(self) -> bool:
        # TODO remove existing container if exist
        self.__run_script_if_available(self.__configuration.get(self.__configuration_section_general, self.__configuration_section_general_key_prescript), "PreScript")
        success = self.__run_system_command("docker", f"compose --project-name {self._internal_get_container_name()} up --detach --build --quiet-pull --force-recreate --always-recreate-deps", self._internal_configuration_folder)
        time.sleep(int(self.__configuration.get(self.__configuration_section_general, self.__configuration_section_general_key_maximalexpectedstartduration)))
        if success:
            self.__log_information("Container was started", False, True, True)
        else:
            self.__log_warning("Container could not be started")
        return success

    @GeneralUtilities.check_arguments
    def _internal_remove_existing_container(self, docker_compose_file: str) -> None:
        with open(docker_compose_file, "r", encoding="utf-8") as stream:
            parsed = yaml.safe_load(stream)
            container_names: list[str] = []
            try:
                for service_name in parsed['services']:
                    service = parsed['services'][service_name]
                    container_names.append(service['container_name'])
            except Exception as exception:
                self.__log_warning(f"Can not check for container-name due to an exception: {str(exception)}")
            for container_name in container_names:
                self.__run_system_command("docker", f"container rm -f {container_name}", self._internal_configuration_folder)

    @GeneralUtilities.check_arguments
    def __get_running_processes(self) -> list:
        if self.__test_mode:
            if len(self.__mock_process_queries) == 0:
                raise LookupError("Tried to query process-list but no mock-queries are available anymore")
            else:
                return self.__mock_process_queries.pop(0)
        else:
            result = list()
            for item in psutil.process_iter():
                try:
                    process = Adame.__process()
                    process.process_id = item.pid
                    process.command = " ".join(item.cmdline())
                    result.append(process)
                except psutil.AccessDenied:
                    # The process searched for is always queryable. Some other processes may not be queryable but they can be ignored since they are not relevant for this use-case.
                    pass
            return result

    @GeneralUtilities.check_arguments
    def _internal_process_is_running(self, process_id: int, command: str) -> bool:
        for process in self.__get_running_processes():
            if (self.__process_is_running_helper(process.process_id, process.command, process_id, command)):
                return True
        return False

    @GeneralUtilities.check_arguments
    def __process_is_running_helper(self, actual_pid: int, actual_command: str, expected_pid: int, expected_command: str) -> bool:
        if actual_pid == expected_pid:
            if expected_command in actual_command:
                return True
            else:
                if (GeneralUtilities.string_is_none_or_whitespace(actual_command)):
                    self.__log_warning(f"It seems that the process with id {expected_pid} was not executed", False, True, False)
                else:
                    self.__log_warning(f"The process with id {expected_pid} changed unexpectedly. Expected a process with a commandline like '{expected_command}...' but was '{actual_command}...'", False, True, False)
        return False

    @GeneralUtilities.check_arguments
    def __get_local_ip_address(self) -> str:
        return "<insert local ip address>"  # TODO calculate value

    @GeneralUtilities.check_arguments
    def __commit(self, message: str, stage_all_changes: bool = True, no_changes_behavior: int = 0, overhead: bool = True) -> None:
        # no_changes_behavior=0 => No commit
        # no_changes_behavior=1 => Commit anyway
        # no_changes_behavior=2 => Exception
        self.__log_information(f"Commit changes (message='{message}', stage_all_changes={str(stage_all_changes)}, no_changes_behavior={str(no_changes_behavior)}, overhead={str(overhead)}')...", True, True, True)
        repository = self.__repository_folder
        if overhead:  # disabled due to condition because escaping does not work properly (rename .git to .gitx does not work properly and the permissions-restoring does also not seem to work.
            self.__save_metadata()
        commit_id = self._internal_sc.git_commit(repository, message, self.__adame_commit_author_name, "", stage_all_changes, no_changes_behavior)
        if overhead:
            remote_name = self.__securityconfiguration[self.__securityconfiguration_section_general][self.__configuration_section_general_key_remotename]
            branch_name = self.__securityconfiguration[self.__securityconfiguration_section_general][self.__configuration_section_general_key_remotebranch]
            remote_address = self.__securityconfiguration.get(self.__securityconfiguration_section_general,  self.__configuration_section_general_key_remoteaddress)
            self.__log_information(f"Created commit {commit_id} in repository '{repository}' (commit-message: '{message}')", False, True, True)
            if self.__remote_address_is_available:
                self._internal_sc.git_add_or_set_remote_address(self.__repository_folder, remote_name, remote_address)
                self._internal_sc.git_push(self.__repository_folder, remote_name, branch_name, branch_name, False, False)
                self.__log_information(f"Pushed repository '{repository}' to remote remote_name ('{remote_address}')", False, True, True)
            else:
                self.__log_warning("Either no remote-address is defined or the remote-address for the backup of the app-repository is not available.")

    @GeneralUtilities.check_arguments
    def __name_to_docker_allowed_name(self, name: str) -> str:
        name = name.lower()
        return name

    @GeneralUtilities.check_arguments
    def __start_program_synchronously(self, program: str, argument: str, workingdirectory: str = None, expect_exitcode_zero: bool = True) -> tuple[int, str, str, int]:
        workingdirectory = GeneralUtilities.str_none_safe(workingdirectory)
        self.__log_information(f"Start program '{workingdirectory}>{program} {argument}' synchronously", True)
        self.__log_diagnostic_information(f"Argument: '{argument}'")
        if self.verbose:
            verbose_argument = 2
        else:
            verbose_argument = 1
        result: tuple[int, str, str, int] = self._internal_sc.run_program(program, argument, workingdirectory, verbose_argument, False, throw_exception_if_exitcode_is_not_zero=expect_exitcode_zero)
        self.__log_information(f"Program resulted in exitcode {result[0]}", True)
        self.__log_information("Stdout:", True)
        self.__log_information(result[1], True)
        self.__log_information("Stderr:", True)
        self.__log_information(result[2], True)
        return result

    @GeneralUtilities.check_arguments
    def __tool_exists_in_path(self, name: str) -> bool:
        return find_executable(name) is not None

    class __process:
        "This class is for test-purposes only"
        process_id: str
        command: str

    @GeneralUtilities.check_arguments
    def __execute_task(self, name: str, function) -> int:
        exitcode = 0
        try:
            self.__log_information(f"Started task '{name}'")
            function()
        except Exception as exception:
            exitcode = 1
            self.__log_exception(f"Exception occurred in task '{name}'", exception)
        finally:
            self.__log_information(f"Finished task '{name}'. Task resulted in exitcode {exitcode}")
        return exitcode

    @GeneralUtilities.check_arguments
    def __log_diagnostic_information(self, message: str) -> None:
        if self.diagnostic:
            self.__write_to_log("Diagnostic", message, True, True, True)

    @GeneralUtilities.check_arguments
    def __log_information(self, message: str, is_verbose_log_entry: bool = False, write_to_console: bool = True, write_to_logfile: bool = False) -> None:
        self.__write_to_log("Information", message, is_verbose_log_entry, write_to_console, write_to_logfile)

    @GeneralUtilities.check_arguments
    def __log_warning(self, message: str, is_verbose_log_entry: bool = False, write_to_console: bool = True, write_to_logfile: bool = False) -> None:
        self.__write_to_log("Warning", message, is_verbose_log_entry, write_to_console, write_to_logfile)

    @GeneralUtilities.check_arguments
    def __log_error(self, message: str, is_verbose_log_entry: bool = False, write_to_console: bool = True, write_to_logfile: bool = False) -> None:
        self.__write_to_log("Error", message, is_verbose_log_entry, write_to_console, write_to_logfile)

    @GeneralUtilities.check_arguments
    def __log_exception(self, message: str, exception: Exception, is_verbose_log_entry: bool = False, write_to_console: bool = True, write_to_logfile: bool = True) -> None:
        self.__write_to_log("Error", f"{message}; {str(exception)}", is_verbose_log_entry, write_to_console, write_to_logfile)
        if (self.verbose):
            GeneralUtilities.write_exception_to_stderr_with_traceback(exception, traceback, message)

    @GeneralUtilities.check_arguments
    def __write_to_log(self, loglevel: str, message: str, is_verbose_log_entry: bool, write_to_console: bool, write_to_logfile: bool) -> None:
        if is_verbose_log_entry and not self.verbose:
            return
        if (self.format_datetimes_to_utc):
            date_as_string = datetime.utcnow()
        else:
            date_as_string = datetime.now()
        logentry = f"[{GeneralUtilities.datetime_to_string_for_logfile_entry(date_as_string)}] [{loglevel}] {message}"
        if (write_to_console):
            if (loglevel == "Error"):
                GeneralUtilities.write_message_to_stderr(logentry)
            else:
                GeneralUtilities.write_message_to_stdout(logentry)
        if (write_to_logfile and self.__log_file_for_adame_overhead is not None):
            GeneralUtilities.ensure_file_exists(self.__log_file_for_adame_overhead)
            if GeneralUtilities.file_is_empty(self.__log_file_for_adame_overhead):
                prefix = ''
            else:
                prefix = '\n'
            with open(self.__log_file_for_adame_overhead, "a", encoding="utf-8") as file:
                file.write(prefix+logentry)

    @GeneralUtilities.check_arguments
    def __set_git_configuration(self):
        self.__start_program_synchronously("git", f"config --local include.path ../{self.__configurationfolder_name}/{self.__gitconfiguration_filename}", self.__repository_folder)

    # </helper-functions>

# <miscellaneous>


@GeneralUtilities.check_arguments
def get_adame_version() -> str:
    return version


@GeneralUtilities.check_arguments
def adame_cli() -> int:
    arger = argparse.ArgumentParser(description=f"""{versioned_product_name}
Adame (Automatic Docker Application Management Engine) is a tool which manages (install, start, stop) docker-applications.
One focus of Adame is to store the state of an application: Adame stores all data of the application in a git-repository. So with Adame it is very easy move the application with all its data and configurations to another computer.
Another focus of Adame is IT-forensics and IT-security: Adame generates a basic ids-configuration for each application to detect/log/block networktraffic from the docker-container of the application which is obvious harmful.

Required commandline-commands:
-chmod (For setting up permissions on the generated files)
-chown (For setting up ownerships on the generated files)
-docker (For starting and stopping Docker-container)
-git (For integrity)

Recommended commandline-commands:
-gpg (For checking the integrity of commits)
-kill (For killing snort)
-rsync (For exporting the log-files to a SIEM-server)
-ssh (Required for rsync)
-snort (For inspecting the network-traffic of the application)

Adame must be executed with elevated privileges. This is required to run commands like docker or snort.
""", formatter_class=RawTextHelpFormatter)

    arger.add_argument("-v", "--verbose", action="store_true", required=False, default=False)
    arger.add_argument("-d", "--diagnostic", action="store_true", required=False, default=False)

    subparsers = arger.add_subparsers(dest="command")

    create_command_name = "create"
    create_parser = subparsers.add_parser(create_command_name)
    create_parser.add_argument("-n", "--name", required=True)
    create_parser.add_argument("-f", "--folder", required=False, default=None)
    create_parser.add_argument("-i", "--image", required=False, default=None)
    create_parser.add_argument("-o", "--owner", required=True)
    create_parser.add_argument("-g", "--gpgkey_of_owner", required=False)

    start_command_name = "start"
    start_parser = subparsers.add_parser(start_command_name)
    start_parser.add_argument("-c", "--configurationfile", required=True)

    stop_command_name = "stop"
    stop_parser = subparsers.add_parser(stop_command_name)
    stop_parser.add_argument("-c", "--configurationfile", required=True)

    apply_configuration_command_name = "applyconfiguration"
    apply_configuration_parser = subparsers.add_parser(apply_configuration_command_name)
    apply_configuration_parser.add_argument("-c", "--configurationfile", required=True)

    startadvanced_command_name = "startadvanced"
    startadvanced_parser = subparsers.add_parser(startadvanced_command_name)
    startadvanced_parser.add_argument("-c", "--configurationfile", required=True)

    stopadvanced_command_name = "stopadvanced"
    stopadvanced_parser = subparsers.add_parser(stopadvanced_command_name)
    stopadvanced_parser.add_argument("-c", "--configurationfile", required=True)

    checkintegrity_command_name = "checkintegrity"
    checkintegrity_parser = subparsers.add_parser(checkintegrity_command_name)
    checkintegrity_parser.add_argument("-c", "--configurationfile", required=True)

    exportlogs_command_name = "exportlogs"
    exportlogs_parser = subparsers.add_parser(exportlogs_command_name)
    exportlogs_parser.add_argument("-c", "--configurationfile", required=True)

    diagnosis_command_name = "diagnosis"
    diagnosis_parser = subparsers.add_parser(diagnosis_command_name)
    diagnosis_parser.add_argument("-c", "--configurationfile", required=False)

    checkout_command_name = "checkout"
    checkout_parser = subparsers.add_parser(checkout_command_name)
    checkout_parser.add_argument("-c", "--configurationfile", required=True)
    checkout_parser.add_argument("-b", "--branch", required=True)

    options = arger.parse_args()

    core = Adame()

    core.diagnostic = options.diagnostic
    if core.diagnostic:
        core.verbose = True
    else:
        core.verbose = options.verbose

    if options.command == create_command_name:
        if not hasattr(options, 'image'):
            options.image = "SomeImage:latest"
        if not hasattr(options, 'folder'):
            options.folder = options.name+"App"
        return core.create(options.name, options.folder, options.image, options.owner, options.gpgkey_of_owner)

    elif options.command == start_command_name:
        return core.start(options.configurationfile)

    elif options.command == stop_command_name:
        return core.stop(options.configurationfile)

    elif options.command == apply_configuration_command_name:
        return core.applyconfiguration(options.configurationfile)

    elif options.command == startadvanced_command_name:
        return core.startadvanced(options.configurationfile)

    elif options.command == stopadvanced_command_name:
        return core.stopadvanced(options.configurationfile)

    elif options.command == checkintegrity_command_name:
        return core.checkintegrity(options.configurationfile)

    elif options.command == exportlogs_command_name:
        return core.exportlogs(options.configurationfile)

    elif options.command == diagnosis_command_name:
        return core.diagnosis(options.configurationfile)

    elif options.command == checkintegrity_command_name:
        return core.checkout(options.configurationfile, options.branch)

    else:
        GeneralUtilities.write_message_to_stdout(versioned_product_name)
        GeneralUtilities.write_message_to_stdout(f"Run '{product_name} --help' to get help about the usage.")
        return 0

# </miscellaneous>


if __name__ == '__main__':
    adame_cli()
