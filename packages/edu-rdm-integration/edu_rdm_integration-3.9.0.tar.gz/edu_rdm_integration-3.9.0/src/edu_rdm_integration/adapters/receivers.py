from sys import (
    stdout,
)


def m3_edu_function_tools_after_migrate_receiver(sender, **kwargs):
    """
    Действия выполняемые после прогона миграций.
    """
    from function_tools.management.commands.register_entities import (
        EntityRegistrar,
    )

    try:
        registrar = EntityRegistrar(logger=stdout)
        registrar.run()
    except Exception as e:
        stdout.write(
            f'Register function_tools_entities exception. ----- START IGNORING EXCEPTION\n{e}\n----- '
            f'FINISH IGNORING EXCEPTION\n'
        )
