# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=C0330, g-bad-import-order, g-multiple-import

"""Module for defining ORM models and repositories."""

import abc
from collections.abc import Sequence

import sqlalchemy
from sqlalchemy.pool import StaticPool

from creative_assistant.models import entity


class BaseRepository(abc.ABC):
  """Interface for defining repositories."""

  @abc.abstractmethod
  def get_by_id(self, identifier: str) -> entity.Entity | None:
    """Specifies get operations."""

  @abc.abstractmethod
  def add(
    self,
    results: entity.Entity | Sequence[entity.Entity],
  ) -> None:
    """Specifies add operations."""

  def list(self) -> list[entity.Entity]:
    """Returns all entities from the repository."""
    return self.results


class SqlAlchemyRepository(BaseRepository):
  """Uses SqlAlchemy engine for persisting entities."""

  IN_MEMORY_DB = 'sqlite://'

  def __init__(
    self, db_url: str | None, orm_model: entity.Entity, primary_key: str
  ) -> None:
    """Initializes SqlAlchemyRepository."""
    self.db_url = db_url or self.IN_MEMORY_DB
    self.orm_model = orm_model
    self.primary_key = primary_key
    self.initialized = False
    self._engine = None

  def initialize(self) -> None:
    """Creates all ORM objects."""
    entity.Entity.metadata.create_all(self.engine)
    self.initialized = True

  @property
  def session(self) -> sqlalchemy.orm.sessionmaker[sqlalchemy.orm.Session]:
    """Property for initializing session."""
    if not self.initialized:
      self.initialize()
    return sqlalchemy.orm.sessionmaker(bind=self.engine)

  @property
  def engine(self) -> sqlalchemy.engine.Engine:
    """Initialized SQLalchemy engine."""
    if self._engine:
      return self._engine
    if self.db_url == self.IN_MEMORY_DB:
      self._engine = sqlalchemy.create_engine(
        self.db_url,
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
      )
    else:
      self._engine = sqlalchemy.create_engine(self.db_url)
    return self._engine

  def get_by_id(self, identifier: str) -> entity.Entity | None:
    """Specifies get operations."""
    return (
      self.session()
      .query(self.orm_model)
      .filter_by(**{self.primary_key: identifier})
      .one_or_none()
    )

  def add(
    self,
    results: entity.Entity | Sequence[entity.Entity],
  ) -> None:
    """Specifies add operations."""
    if not isinstance(results, Sequence):
      results = [results]
    with self.session() as session:
      for result in results:
        session.add(result)
      session.commit()

  def list(
    self,
    limit: int = 0,
    offset: int = 0,
  ) -> list[entity.Entity]:
    """Returns entities from the repository."""
    query = (
      self.session()
      .query(self.orm_model)
      .order_by(self.orm_model.pinned, self.orm_model.created_at.desc())
    )
    if offset:
      query = query.offset(limit * offset)
    if limit:
      query = query.limit(limit)
    return query.all()

  def delete_by_id(self, identifier: str) -> None:
    """Specifies delete operations."""
    with self.session() as session:
      session.query(self.orm_model).filter_by(
        **{self.primary_key: identifier}
      ).delete()
      session.commit()

  def update(self, identifier: str, update_mask: dict[str, str]) -> None:
    """Update entity in the repository."""
    with self.session() as session:
      session.query(self.orm_model).filter_by(
        **{self.primary_key: identifier}
      ).update(update_mask)
      session.commit()
