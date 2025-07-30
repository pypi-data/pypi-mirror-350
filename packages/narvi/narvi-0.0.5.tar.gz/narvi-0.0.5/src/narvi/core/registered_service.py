
from dataclasses import dataclass
from typing import Any, Callable
from narvi.core.webapp import WebApp

@dataclass
class RegisteredService:

    constructor_fn:Callable[[str],WebApp]
    namespace:str
    app_service_name:str
    app_cls_name:str
    app_parameters:dict[str,Any]
    fixed_service_id:str=None
    is_shared_service:bool=True
    service_id_validator:Callable[[str],bool]=lambda service_id: True

    def validate_service_id(self, service_id, logger):
        if self.fixed_service_id:
            if service_id != self.fixed_service_id:
                logger.warning(f"validation failed {service_id} does not match fixed service id {self.fixed_service_id}")
                return False
        if self.service_id_validator is not None:
            try:
                validated = self.service_id_validator(service_id)
                if not validated:
                    logger.warning(f"validation failed for {service_id}")
                return validated
            except:
                logger.exception(f"validation exception for {service_id}")
        else:
            return True
