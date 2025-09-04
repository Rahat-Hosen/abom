
from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from ..common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash


@action("dashboard/index")
@action.uses("dashboard/index.html",session,flash)
def index():

    return  locals()