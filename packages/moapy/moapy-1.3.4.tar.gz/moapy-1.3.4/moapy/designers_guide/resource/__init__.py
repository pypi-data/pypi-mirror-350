from itertools import chain

import moapy.designers_guide.resource.component_request as component_request
from moapy.designers_guide.resource_handler.content_component import (
    Component,
    Content,
)
from moapy.designers_guide.resource.content_component import (
    component_list as origin_component_list,
)
from moapy.designers_guide.resource.contents import (
    contents as origin_content_list,
)
import moapy.designers_guide.resource.component17 as component17
import moapy.designers_guide.resource.component18 as component18
import moapy.designers_guide.resource.component19 as component19
import moapy.designers_guide.resource.component20 as component20
import moapy.designers_guide.resource.component21 as component21
import moapy.designers_guide.resource.component22 as component22
import moapy.designers_guide.resource.component23 as component23
import moapy.designers_guide.resource.component24 as component24
import moapy.designers_guide.resource.component25 as component25
import moapy.designers_guide.resource.component26 as component26
import moapy.designers_guide.resource.component27 as component27
import moapy.designers_guide.resource.component28 as component28
import moapy.designers_guide.resource.component29 as component29
import moapy.designers_guide.resource.component30 as component30
import moapy.designers_guide.resource.component31 as component31
import moapy.designers_guide.resource.component32 as component32
import moapy.designers_guide.resource.component33 as component33
import moapy.designers_guide.resource.component34 as component34
import moapy.designers_guide.resource.component35 as component35
import moapy.designers_guide.resource.component36 as component36
import moapy.designers_guide.resource.component37 as component37
import moapy.designers_guide.resource.component38 as component38
import moapy.designers_guide.resource.component39 as component39
import moapy.designers_guide.resource.component40 as component40

def compose_component_list(*args: list[list[Component]]):
    return list(chain(*args))

def compose_content_list(*args: list[list[Content]]):
    return list(chain(*args))


components = compose_component_list(
    component_request.component_list,
    origin_component_list,
    component17.component_list,
    component18.component_list,
    component19.component_list,
    component20.component_list,
    component21.component_list,
    component22.component_list,
    component23.component_list,
    component24.component_list,
    component25.component_list,
    component26.component_list,
    component27.component_list,
    component28.component_list,
    component29.component_list,
    component30.component_list,
    component31.component_list,
    component32.component_list,
    component33.component_list,
    component34.component_list,
    component35.component_list,
    component36.component_list,
    component37.component_list,
    component38.component_list,
    component39.component_list,
    component40.component_list,
)

contents = compose_content_list(
    # component_request.content_list,
    origin_content_list,
    component17.content,
    component18.content,
    component19.content,
    component20.content,
    component21.content,
    component22.content,
    component23.content,
    component24.content,
    component25.content,
    component26.content,
    component27.content,
    component28.content,
    component29.content,
    component30.content,
    component31.content,
    component32.content,
    component33.content,
    component34.content,
    component35.content,
    component36.content,
    component37.content,
    component38.content,
    component39.content,
    component40.content,
)