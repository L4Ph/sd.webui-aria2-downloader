import launch

if not launch.is_installed("aria2p"):
    launch.run_pip("install aria2p==0.11.3", "requirements for aria2c")
# TODO: add pip dependency if need extra module only on extension

# if not launch.is_installed("aitextgen"):
#     launch.run_pip("install aitextgen==0.6.0", "requirements for MagicPrompt")