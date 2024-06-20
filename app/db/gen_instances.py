from typing import Optional

from sqlalchemy import DateTime, Float, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column
import datetime

class Base(MappedAsDataclass, DeclarativeBase):
    pass


class CnPosts(Base):
    __tablename__ = 'cn_posts'

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(255))
    avatar_template: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    cooked: Mapped[Optional[str]] = mapped_column(Text)
    post_number: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    post_type: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    reply_count: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    reply_to_post_number: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    quote_count: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    incoming_link_count: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    reads: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    readers_count: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    score: Mapped[Optional[float]] = mapped_column(Float)
    yours: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    topic_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    topic_slug: Mapped[Optional[str]] = mapped_column(String(255))
    version: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    can_edit: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    can_delete: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    can_recover: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    can_see_hidden_post: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    can_wiki: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    bookmarked: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    raw: Mapped[Optional[str]] = mapped_column(Text)
    moderator: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    admin: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    staff: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    user_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    hidden: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    trust_level: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    user_deleted: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    can_view_edit_history: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    wiki: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    can_accept_answer: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    can_unaccept_answer: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    accepted_answer: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    topic_accepted_answer: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    en_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    translated: Mapped[Optional[str]] = mapped_column(Text)


class CnTopics(Base):
    __tablename__ = 'cn_topics'

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String(255))
    fancy_title: Mapped[Optional[str]] = mapped_column(String(255))
    slug: Mapped[Optional[str]] = mapped_column(String(255))
    posts_count: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    reply_count: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    highest_post_number: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    last_posted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    archetype: Mapped[Optional[str]] = mapped_column(String(255))
    pinned: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    visible: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    closed: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    archived: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    views: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    like_count: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    has_summary: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    category_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    pinned_globally: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    has_accepted_answer: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    en_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    translated_title: Mapped[Optional[str]] = mapped_column(Text)


class SyncProgress(Base):
    __tablename__ = 'sync_progress'

    cn_topic_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    en_topic_id: Mapped[Optional[int]] = mapped_column(INTEGER(11), server_default=text("'-1'"))
    cn_title: Mapped[Optional[str]] = mapped_column(String(255))
    cn_created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    translate_state: Mapped[Optional[int]] = mapped_column(INTEGER(11), server_default=text("'0'"), comment='0 - not translate, 1 - translating, 2 - translated')
    translate_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text("'1980-01-01 00:00:00'"))
