from ..Application.Abstractions.base_service_collection import BaseServiceCollectionFWDI

class DependencyInjection():

    @staticmethod
    def AddUtilites(services:BaseServiceCollectionFWDI)->None:
        from .jwt_tools import JwtToolsFWDI
        services.AddTransient(JwtToolsFWDI)