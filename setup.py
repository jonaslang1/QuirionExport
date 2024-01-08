import py2exe

py2exe.freeze(console=[{'script': 'quirion_bot.py'}], options={
    "py2exe": {
        "includes": ["selenium", "webdriver_manager"],
        "skip_archive": True,  # tell script to not create a library folder
        "unbuffered": True,
        "optimize": 2
    }
})
