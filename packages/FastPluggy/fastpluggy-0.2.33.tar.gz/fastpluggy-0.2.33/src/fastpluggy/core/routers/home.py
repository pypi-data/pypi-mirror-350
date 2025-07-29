from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from starlette.responses import JSONResponse

from fastpluggy.core.dependency import get_templates, get_fastpluggy
from fastpluggy.core.tools.system import trigger_reload

home_router = APIRouter()


@home_router.get("/admin", response_class=HTMLResponse)
def fast_pluggy_home(request: Request, templates=Depends(get_templates)):
    """
    Home page route that renders the index.html.j2 template.
    """
    from fastpluggy.fastpluggy import FastPluggy

    fp_widget_admin_home = FastPluggy.get_global('fp_widgets',{}).get('admin_home',None)

    return templates.TemplateResponse("index.html.j2", {
        "request": request,
        "fp_widget_admin_home":fp_widget_admin_home
    })


@home_router.get("/ready", response_class=HTMLResponse)
def fast_pluggy_ready(request: Request, fast_pluggy=Depends(get_fastpluggy)):
    """
    Readiness probe for Fast-Pluggy: returns 200 when fully initialized,
    503 otherwise.
    """
    if fast_pluggy.is_ready:
        # trigger reload if needed
        plugins_dir = fast_pluggy.get_folder_by_module_type('plugin')
        trigger_reload(plugins_dir)
        return JSONResponse(status_code=200, content={"status": "ready"})
    return JSONResponse(status_code=503, content={"status": "not_ready"})

