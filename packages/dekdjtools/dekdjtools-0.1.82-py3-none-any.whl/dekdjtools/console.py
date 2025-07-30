# File | Settings | Build, Execution, Deployment | Console | Django Console
# Starting script

from django_extensions.management.commands.shell_plus import Command;globals().update(Command().get_imported_objects({}))
