from application.config import settings
from application.use_cases.file_use_case import FileUseCase
from domain.file.repositories.read_repository import FileReadRepository
from domain.file.repositories.write_repository import FileWriteRepository
from infrastructure.adapters.database.alchemy_adapter import AlchemyAdapter
from infrastructure.common.base_entities.singleton import OnlyContainer, Singleton


class Container(Singleton):

    alchemy_manager: AlchemyAdapter = OnlyContainer(
        AlchemyAdapter,
        dialect=settings.POSTGRES.dialect,
        host=settings.POSTGRES.host,
        login=settings.POSTGRES.login,
        password=settings.POSTGRES.password,
        port=settings.POSTGRES.port,
        database=settings.POSTGRES.database,
        echo=settings.POSTGRES.echo,
    )

    file_read_repository: FileReadRepository = OnlyContainer(
        FileReadRepository,
        session_adapter=alchemy_manager(),
    )

    file_write_repository: FileWriteRepository = OnlyContainer(
        FileWriteRepository,
        session_adapter=alchemy_manager(),
    )

    file_service: FileUseCase = OnlyContainer(
        FileUseCase,
        read_repository=file_read_repository(),
        write_repository=file_write_repository(),
    )
