import traceback

from baker import logger
from baker import settings
from baker.cli import Parser
from baker.recipe import RecipeParser
from baker.repository import Repository
from baker.secret import SecretKey, Encryption
from baker.template import ReplaceTemplate
from baker.repository import ListRecipes, download


class Commands:
    """
    Commands available for baker
    """
    @staticmethod
    def config(args):
        """
        List of current baker configs
        """
        configs = settings.values(custom_only=not args.all)
        for key, value in configs.items():
            logger.log(key + '=' + str(value))

    @staticmethod
    def encrypt(args):
        """
        Encrypt values from recipe file or list of strings
        """
        secret_key = str(SecretKey().key)
        enc = Encryption(secret_key)

        if args.file:
            parser = RecipeParser(args.file, case_sensitive=True)
            for instruction in parser.instructions:
                instruction.plan_to_secrets()
            parser.update_secrets()
        elif args.plantexts:
            for text in args.plantexts:
                logger.log(text, enc.encrypt(text))

    @staticmethod
    def generate_key(args):
        """
        Generate and storage secret key from key pass to encrypt secret values
        """
        SecretKey.generate(args.keypass)

    @staticmethod
    def pull(args):
        """
        Pull recipe from repository and version specific
        """
        Repository(args.name).pull(args.force)

    @staticmethod
    def recipes(args):
        """
        List all recipes locally
        """
        ListRecipes.list(args.all)

    @staticmethod
    def rm_recipe(args):
        """
        Remove local recipe from id
        """
        Repository.remove(args.recipe_id)

    @staticmethod
    def run(args):
        """
        Run a recipe from local path or get it from repository
        """
        if args.name and not args.path:
            repo = Repository(args.name)
            repo.pull(args.force)
            path = repo.local_path
        elif not args.name and args.path:
            path = args.path
        else:
            raise ValueError("Run command does not support 'name' and '--path' options together")

        recipe = RecipeParser(path)
        for instruction in recipe.instructions:
            instruction.secrets_to_plan()
            if instruction.is_remote:
                instruction.template = download(instruction.template, force=args.force)

        template = ReplaceTemplate(recipe.instructions)
        template.replace()


def execute_command_line(args):
    """
    Execute command line and wrap exceptions to show a friendly message
    """
    del args[0]
    parser = Parser(args, Commands)
    options = parser.options

    try:
        settings.load(DEBUG=options.verbose)
        logger.init()

        if 'multiprocess' in options:
            logger.log('Baker start <:::> \n')

        parser.execute()

        if 'multiprocess' in options:
            logger.log('\nAll done with success! \\ o /')
    except Exception as e:
        logger.debug(str(traceback.format_exc()))
        logger.log(str(e))
        parser.exit_with_error(
            '\nERROR: Unexpected error was caught. Add --verbose option for more information.\n')
