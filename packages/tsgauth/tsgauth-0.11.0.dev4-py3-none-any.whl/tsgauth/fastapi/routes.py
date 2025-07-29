from fastapi import HTTPException, Request, APIRouter, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from tsgauth.fastapi.settings import settings
from tsgauth.fastapi.authstores import SessionAuthBase, get_auth_store
from tsgauth.fastapi.tokenutil import exchange_code_for_token
from urllib.parse import urlencode 

"""
defines all the authentication related routes for the fastapi server
note that a claims route is not defined as wanted to make that optional for each
service to define themselves and control what they return for that endpoint
"""

router = APIRouter(prefix="/auth")

@router.get("/token_request",tags=["auth"])
async def get_token_from_auth_server(request: Request, redirect_uri : str,extra_scopes : str = "",auth_store: SessionAuthBase = Depends(get_auth_store)) -> RedirectResponse:
    """Redirects to the authorization server to obtain a token."""
    await auth_store.auth_attempt(request)        
    params = {
        "client_id": settings.oidc_client_id,
        "redirect_uri": f"{request.url_for('auth_callback')}",
        "response_type": "code",
        "scope": f"openid email profile {extra_scopes}".rstrip(),
        "state": str(redirect_uri)#.split("@")[0]+"@"+extra_scopes,
    }
    auth_url = f"{settings.oidc_auth_uri}?{urlencode(params)}"
    return RedirectResponse(auth_url)


#feels like it should be a post but seems to be required to be a get
@router.get("/callback",tags=["auth"])
async def auth_callback(request: Request, auth_store : SessionAuthBase = Depends(get_auth_store)) -> RedirectResponse:
    """Handles the callback from the OIDC provider after authentication."""
    
    params = dict(request.query_params)
    if "error" in params:
        raise HTTPException(detail=f"error getting token from SSO: {params['error']}", status_code=400)

    code = params.get("code")
    if not code:
        raise HTTPException(detail="error getting token from SSO: no code provided", status_code=400)
    
    token_response = exchange_code_for_token(code, request)    
    redirect_uri = params.get("state") or "/"        
    #this was simply to fake an offline access token for testing
    #offline_access = redirect_uri.split("@")[-1] == "offline_access"
    #if offline_access:
    #    token_response["refresh_expires_in"] = 0
    #redirect_uri = redirect_uri.split("@")[0]
    try:
        await auth_store.store(request, token_response)
    except SessionAuthBase.AuthResponseException as e:
        raise HTTPException(detail=f"error getting token from SSO: {e}", status_code=401)
    except SessionAuthBase.TokenNotOfflineException as e:
        print("requesting offline access")
        return RedirectResponse(f"{request.url_for('get_token_from_auth_server')}?redirect_uri={redirect_uri}&extra_scopes=offline_access")
    
    return RedirectResponse(redirect_uri)

#probably should be delete but is get for simplicity when calling from web browser
@router.get("/clear",tags=["auth"])
async def clear_session_auth(request: Request, deep: bool =False,auth_store: SessionAuthBase = Depends(get_auth_store)) -> JSONResponse:
    """
    clears the auth session but does not log the user out\n
    deep=1 will do a deep clear of the session (which is up to the auth store to decide what that means)
    """
    await auth_store.clear(request,deep=deep)
    return {"status": "cleared auth session, user still logged into SSO"}

#probably should be delete but is get for simplicity when calling directly from web browser
@router.get("/logout",tags=["auth"])
async def logout(request: Request, deep : bool = False)-> RedirectResponse:
    """
    logs the user out, clearing the session and logging out of the OIDC provider\n
    deep=1 will do a deep clear of the session (which is up to the auth store to decide what that means)
    """
    await clear_session_auth(request,deep=deep)
    return RedirectResponse(settings.oidc_logout_uri)

