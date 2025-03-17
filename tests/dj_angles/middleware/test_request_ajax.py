from dj_angles.middleware import RequestAJAXMiddleware


def test_not_ajax(rf):
    middleware = RequestAJAXMiddleware(lambda _: None)

    request = rf.get("/")
    middleware.__call__(request)

    assert not request.is_ajax


def test_ajax(rf):
    middleware = RequestAJAXMiddleware(lambda _: None)

    request = rf.get("/", HTTP_X_REQUESTED_WITH="XMLHttpRequest")
    middleware.__call__(request)

    assert request.is_ajax
