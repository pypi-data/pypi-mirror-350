from paprika import data

@data
class Topic:
    id: int
    title: str
    replies: int
    url: str
    content: str
    content_rendered: str
    node_title: str
    username: str
    last_reply_user: str
    created: str


@data
class Reply:
    id: int
    topic_id: int
    content: str
    content_rendered: str
    username: str
    created: str


