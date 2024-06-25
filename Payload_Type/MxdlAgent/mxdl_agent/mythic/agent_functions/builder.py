from mythic_container.PayloadBuilder import *
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *

import json
import os
import pathlib


class MxdlAgent(PayloadType):
    name = "mxdl_agent"  # NEEDS TO BE THE SAME AS THE DIRECTORY THE AGENT IS IN
    file_extension = "exe"
    author = "@maximedelis"
    supported_os = [SupportedOS.Linux, SupportedOS.Windows]
    wrapper = False
    wrapped_payloads = []
    note = """A Rust agent by Mxdl"""
    supports_dynamic_loading = False
    c2_profiles = ["http"]
    mythic_encrypts = True
    translation_container = None
    build_parameters = [
        BuildParameter(
            name="output",
            parameter_type=BuildParameterType.ChooseOne,
            description="Choose output format",
            choices=["exe"],
            default_value="exe"
        ),
        BuildParameter(
            name="https_check",
            parameter_type=BuildParameterType.ChooseOne,
            description="Verify HTTPS certificate (if HTTP, leave yes)",
            choices=["Yes", "No"],
            default_value="Yes"
        )
    ]
    agent_path = pathlib.Path(".") / "mxdl_agent"
    agent_icon_path = agent_path / "mythic" / "agent_functions" / "rust_mxdl.jpg"
    agent_code_path = agent_path / "agent_code"

    build_steps = [  # Build steps
        BuildStep(step_name="Gathering Files", step_description="Making sure all commands have backing files on disk"),
        BuildStep(step_name="Configuring", step_description="Stamping in configuration values"),
        BuildStep(step_name="Compiling", step_description="Compiling the agent")
    ]

    async def build(self) -> BuildResponse:  # Build function called when an agent is generated
        resp = BuildResponse(status=BuildStatus.Success)
        build_msg = ""
        return resp

    # Automatically called when a new callback is received
    async def on_new_callback(self, newCallback: PTOnNewCallbackAllData) -> PTOnNewCallbackResponse:
        new_task_resp = await SendMythicRPCTaskCreate(MythicRPCTaskCreateMessage(
            AgentCallbackID=newCallback.Callback.AgentCallbackID,
            CommandName="shell",
            Params="whoami",
        ))
        if new_task_resp.Success:
            return PTOnNewCallbackResponse(AgentCallbackID=newCallback.Callback.AgentCallbackID, Success=True)
        return PTOnNewCallbackResponse(AgentCallbackID=newCallback.Callback.AgentCallbackID, Success=False,
                                       Error=new_task_resp.Error)
