from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *


class UploadArguments(TaskArguments):

    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="file",
                type=ParameterType.File,
                description="file to upload"
            ),
            CommandParameter(
                name="remote_path",
                type=ParameterType.String,
                description="/remote/path/on/victim.txt",
            ),
        ]

    async def parse_arguments(self):  # not even sure it's useful
        if len(self.command_line) == 0:
            raise ValueError("Must supply the file to upload")
        self.add_arg("command", self.command_line)

    async def parse_dictionary(self, dictionary_arguments):
        self.load_args_from_dictionary(dictionary_arguments)


class UploadCommand(CommandBase):
    cmd = "upload"
    needs_admin = False
    help_cmd = "upload"
    description = "Upload a file to the target machine"
    version = 1
    author = "@maximedelis"
    argument_class = UploadArguments
    attackmapping = ["T1132", "T1030", "T1105"]
    attributes = CommandAttributes(
        supported_os=[SupportedOS.MacOS, SupportedOS.Linux, SupportedOS.Windows],
        builtin=False,
        suggested_command=False,
    )

    async def create_go_tasking(self,
                                taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        response = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
        )
        try:
            file_resp = await SendMythicRPCFileSearch(MythicRPCFileSearchMessage(
                TaskID=taskData.Task.ID,
                AgentFileID=taskData.args.get_arg("file")
            ))
            if file_resp.Success:
                if len(file_resp.Files) > 0:
                    original_file_name = file_resp.Files[0].Filename
                    if len(taskData.args.get_arg("remote_path")) == 0:
                        taskData.args.add_arg("remote_path", original_file_name)
                    elif taskData.args.get_arg("remote_path")[-1] == "/":
                        taskData.args.add_arg("remote_path", taskData.args.get_arg("remote_path") + original_file_name)
                    response.DisplayParams = f"{original_file_name} to {taskData.args.get_arg('remote_path')}"
                else:
                    raise Exception("Failed to find that file")
            else:
                raise Exception("Error from Mythic trying to get file: " + str(file_resp.Error))
        except Exception as e:
            raise Exception("Error from Mythic: " + str(sys.exc_info()[-1].tb_lineno) + " : " + str(e))
        return response

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp