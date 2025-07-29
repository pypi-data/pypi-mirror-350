#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

#------INTERFACES-----------------------------------------------------------
from ..Application.Abstractions.base_jwt_service import BaseAuthServiceFWDI
from ..Application.Abstractions.base_service_collection import BaseServiceCollectionFWDI
from ..Application.Abstractions.base_rest_client import BaseRestClientFWDI
#------/INTERFACES----------------------------------------------------------

#-----INSTANCE--------------------------------------------------------------
from ..Infrastructure.Rest.rest_client import RestClientFWDI
from .AuthService.auth_service import AuthServiceFWDI
#-----/INSTANCE-------------------------------------------------------------

class DependencyInjection():
    def AddInfrastructure(services:BaseServiceCollectionFWDI):
        services.AddTransient(BaseRestClientFWDI, RestClientFWDI)
        services.AddTransient(BaseAuthServiceFWDI, AuthServiceFWDI)