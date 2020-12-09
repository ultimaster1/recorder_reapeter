class bat_maker():
    def __init__(self,path_to_bat,path_to_log,path_to_repeater,path_to_studio):
        self.path_to_bat = path_to_bat
        self.path_to_log = path_to_log
        self.path_to_repeater = path_to_repeater
        self.path_to_studio = path_to_studio
        self.vbs = None

    def make_files(self):
        command = 'java -jar ' + self.path_to_studio + ' -r ' + self.path_to_repeater + ' -- ' + self.path_to_log
        bat_path = self.path_to_bat + '/action.bat'
        action_bat = open(bat_path, 'w+')
        action_bat.write(command)
        action_bat.close()
        self.vbs = self.path_to_bat + '/command_vbs.vbs'
        vbs_file = open(self.vbs, 'w+')
        vbs_file_command = "Set WshShell = CreateObject(\"WScript.Shell\")\n WshShell.Run chr(34) & \"" + bat_path + "\" & Chr(34), 0\nSet WshShell = Nothing"
        vbs_file.write(vbs_file_command)
        vbs_file.close()


    def make_shedule(self,shedule_type,task_name):
        create_command = 'schtasks /create /sc ' + shedule_type + ' /tn ' + task_name + ' /tr ' + self.vbs + ' /st 11:25'
        delete_command = 'schtasks /delete /tn ' + task_name
        create_bat = open(self.path_to_bat + 'create.bat', 'w+')
        create_bat.write(create_command)
        create_bat.close()
        delete_bat = open(self.path_to_bat + 'delete.bat', 'w+')
        delete_bat.write(delete_command)
        delete_bat.close()
