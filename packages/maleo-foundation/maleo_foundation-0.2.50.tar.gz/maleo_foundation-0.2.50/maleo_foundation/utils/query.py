from sqlalchemy import Column, Table
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Query
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.expression import or_, asc, cast, desc
from sqlalchemy.types import DATE, String, TEXT, TIMESTAMP
from typing import Type
from maleo_foundation.types import BaseTypes
from maleo_foundation.extended_types import ExtendedTypes

class BaseQueryUtils:
    @staticmethod
    def filter_column(
        query:Query,
        table:Type[DeclarativeMeta],
        column:str,
        value:BaseTypes.OptionalAny
    ) -> Query:
        if not value:
            return query
        column_attr = getattr(table, column, None)
        if not column_attr:
            return query
        if isinstance(value, list):
            value_filters = [column_attr == val for val in value]
            query = query.filter(or_(*value_filters))
            return query
        query = query.filter(column_attr == value)
        return query

    @staticmethod
    def filter_ids(
        query:Query,
        table:Type[DeclarativeMeta],
        column:str,
        ids:BaseTypes.OptionalListOfIntegers
    ) -> Query:
        if ids is not None:
            column_attr = getattr(table, column, None)
            if column_attr:
                id_filters = [column_attr == id for id in ids]
                query = query.filter(or_(*id_filters))
        return query
    
    @staticmethod
    def filter_timestamps(
        query:Query,
        table:Type[DeclarativeMeta],
        date_filters:ExtendedTypes.ListOfDateFilters
    ) -> Query:
        if date_filters and len(date_filters) > 0:
            for date_filter in date_filters:
                try:
                    table:Table = table.__table__
                    column:Column = table.columns[date_filter.name]
                    column_attr:InstrumentedAttribute = getattr(table, date_filter.name)
                    if isinstance(column.type, (TIMESTAMP, DATE)):
                        if date_filter.from_date and date_filter.to_date:
                            query = query.filter(
                                column_attr.between(
                                    date_filter.from_date,
                                    date_filter.to_date
                                )
                            )
                        elif date_filter.from_date:
                            query = query.filter(column_attr >= date_filter.from_date)
                        elif date_filter.to_date:
                            query = query.filter(column_attr <= date_filter.to_date)
                except KeyError:
                    continue
        return query
    
    @staticmethod
    def filter_statuses(
        query:Query,
        table:Type[DeclarativeMeta],
        statuses:BaseTypes.OptionalListOfStatuses
    ) -> Query:
        if statuses is not None:
            status_filters = [table.status == status for status in statuses]
            query = query.filter(or_(*status_filters))
        return query
    
    @staticmethod
    def filter_search(
        query:Query,
        table:Type[DeclarativeMeta],
        search:BaseTypes.OptionalString
    ) -> Query:
        if search:
            search_term = f"%{search}%" #* Use wildcard for partial matching
            search_filters = []
            sqla_table:Table = table.__table__
            for name, attr in vars(table).items():
                try:
                    column: Column = sqla_table.columns[name]
                    if not isinstance(attr, InstrumentedAttribute):
                        continue
                    if isinstance(column.type, (String, TEXT)):
                        search_filters.append(cast(attr, TEXT).ilike(search_term))
                except KeyError:
                    continue
            if search_filters:
                query = query.filter(or_(*search_filters))
        return query
    
    @staticmethod
    def sort(
        query:Query,
        table:Type[DeclarativeMeta],
        sort_columns:ExtendedTypes.ListOfSortColumns
    ) -> Query:
        for sort_column in sort_columns:
            try:
                sort_col = getattr(table, sort_column.name)
                sort_col = asc(sort_col) if sort_column.order.value.lower() == "asc" else desc(sort_col)
                query = query.order_by(sort_col)
            except AttributeError:
                continue
        return query

    @staticmethod
    def paginate(query:Query, page:int, limit:int) -> Query:
        offset:int = (page - 1) * limit #* Calculate offset based on page
        query = query.limit(limit=limit).offset(offset=offset)
        return query