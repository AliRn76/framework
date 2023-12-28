from fastui import components as c
from fastui import prebuilt_html
from fastui.components.display import DisplayLookup
from fastui.events import GoToEvent

from panther.app import GenericAPI
from panther.configs import config
from panther.panel.utils import get_model_fields, _Model
from panther.response import HTMLResponse


class Landing(GenericAPI):
    def get(self):
        return HTMLResponse(prebuilt_html(title='Panther Admin Panel'))


class ModelsAPI(GenericAPI):
    def get(self):
        models = [{
            'name': m['name'],
            'module': m['module'],
            'index': i
        } for i, m in enumerate(config['models'])]
        return [
            c.Page(
                components=[
                    c.Heading(text='Models', level=2),
                    c.Table[_Model](
                        data=models,
                        columns=[
                            DisplayLookup(field='name', on_click=GoToEvent(url='{index}/')),
                            DisplayLookup(field='module'),
                        ],
                    ),
                ]
            ).model_dump(by_alias=True, exclude_none=True),
        ]


class DocumentsAPI(GenericAPI):
    def get(self, index: int):
        try:
            model = config['models'][index]['class']
        except IndexError:
            return []

        return [
            c.Page(
                components=[
                    c.Heading(text='Models', level=2),
                    c.Table[model](
                        data=model.find(),
                        columns=[DisplayLookup(field=field) for field in get_model_fields(model).keys()],
                    ),
                ]
            ).model_dump(by_alias=True, exclude_none=True),
        ]
