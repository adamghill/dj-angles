from dj_angles.middleware import RequestMethodMiddleware


def test_get(rf):
    middleware = RequestMethodMiddleware(lambda _: None)

    request = rf.get("/")
    middleware.__call__(request)

    assert request.is_get
    assert not request.is_post
    assert not request.is_patch
    assert not request.is_head
    assert not request.is_put
    assert not request.is_delete
    assert not request.is_trace


def test_post(rf):
    middleware = RequestMethodMiddleware(lambda _: None)

    request = rf.post("/")
    middleware.__call__(request)

    assert not request.is_get
    assert request.is_post
    assert not request.is_patch
    assert not request.is_head
    assert not request.is_put
    assert not request.is_delete
    assert not request.is_trace


def test_patch(rf):
    middleware = RequestMethodMiddleware(lambda _: None)

    request = rf.patch("/")
    middleware.__call__(request)

    assert not request.is_get
    assert not request.is_post
    assert request.is_patch
    assert not request.is_head
    assert not request.is_put
    assert not request.is_delete
    assert not request.is_trace


def test_head(rf):
    middleware = RequestMethodMiddleware(lambda _: None)

    request = rf.head("/")
    middleware.__call__(request)

    assert not request.is_get
    assert not request.is_post
    assert not request.is_patch
    assert request.is_head
    assert not request.is_put
    assert not request.is_delete
    assert not request.is_trace


def test_put(rf):
    middleware = RequestMethodMiddleware(lambda _: None)

    request = rf.put("/")
    middleware.__call__(request)

    assert not request.is_get
    assert not request.is_post
    assert not request.is_patch
    assert not request.is_head
    assert request.is_put
    assert not request.is_delete
    assert not request.is_trace


def test_delete(rf):
    middleware = RequestMethodMiddleware(lambda _: None)

    request = rf.delete("/")
    middleware.__call__(request)

    assert not request.is_get
    assert not request.is_post
    assert not request.is_patch
    assert not request.is_head
    assert not request.is_put
    assert request.is_delete
    assert not request.is_trace


def test_trace(rf):
    middleware = RequestMethodMiddleware(lambda _: None)

    request = rf.trace("/")
    middleware.__call__(request)

    assert not request.is_get
    assert not request.is_post
    assert not request.is_patch
    assert not request.is_head
    assert not request.is_put
    assert not request.is_delete
    assert request.is_trace
