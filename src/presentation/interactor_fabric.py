from contextlib import asynccontextmanager
from typing import AsyncContextManager

from fastapi import Depends, Response

from application.container import Container
from application.interactors.authenticate import Authenticate
from application.services.artist_service import TemplateService
from domain.auth.entities.enums import AuthOptions
from infrastructure.adapters import CookieAdapter, TokenAdapter


class AuthInteractorFactory:
    def __init__(
        self,
        token_adapter: TokenAdapter = Depends(Container.token_manager),
        template_service: TemplateService = Depends(),
        response: Response = None,
    ) -> None:
        self.token_adapter = token_adapter
        self.template_service = template_service
        self.response = response

    @asynccontextmanager
    async def authenticate(
        self, option: AuthOptions
    ) -> AsyncContextManager[Authenticate]:
        cookie_adapter = CookieAdapter(self.response) if self.response else None
        yield Authenticate(
            token_adapter=self.token_adapter,
            template_service=self.template_service,
            cookie_adapter=cookie_adapter,
            option=option,
        )
