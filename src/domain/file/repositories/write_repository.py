from infrastructure.adapters.database.alchemy_adapter import AlchemyAdapter
from infrastructure.database.models import File
from infrastructure.database.repositories.write_repository import WriteRepository


class FileWriteRepository(WriteRepository[File]):

    def __init__(self, session_adapter: AlchemyAdapter) -> None:
        super().__init__(session_adapter, File)
