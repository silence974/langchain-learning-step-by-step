checkpointer = MemorySaver()

agent = create_deep_agent(
    backend=FilesystemBackend(root_dir="/user/{project}", virtual_mode=True),
    skills=["/user/{project}/skills/"],
    interrupt_on=[
        "write_file": True,
        "read_file": False,
        "edit_file": True,
    ],
    checkpointer=checkpointer,
)