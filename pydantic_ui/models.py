from typing import List, Type

from pydantic import BaseModel


class UIModel:
    __registered_models: List[Type["UIModel"]] = []

    kind: Type[BaseModel]

    def __init_subclass__(cls, **kwargs):  # type: ignore
        super().__init_subclass__(**kwargs)
        if getattr(cls, "kind", None) is None:
            raise NotImplementedError(f"Subclass of UIModel {cls.__name__} has no attribute `kind`")
        cls.__registered_models.append(cls)

    @classmethod
    def get_registered_models(cls) -> List[Type["UIModel"]]:
        return cls.__registered_models


class PydanticUI:
    registered_models: List[Type[UIModel]]
    theme: str

    def __init__(self) -> None:
        self.registered_models = UIModel.get_registered_models()

    def list_models(self) -> List[Type[UIModel]]:
        return self.registered_models

    def get_models_name(self) -> List[str]:
        return [model.__name__ for model in self.registered_models]

    def get_model_by_name(self, name: str) -> Type[UIModel]:
        for model in self.registered_models:
            if model.__name__ == name:
                return model
        return None  # type: ignore
