from typing import Type, TypeVar, List, Dict, Any, Union, Optional
from abs_exception_core.exceptions import BadRequestError, NotFoundError, GenericHttpError, ValidationError
from pydantic import BaseModel
from pymongo import ASCENDING, DESCENDING
from beanie.operators import Set
from pymongo.errors import PyMongoError
from datetime import datetime, UTC
from motor.motor_asyncio import AsyncIOMotorDatabase
from beanie import Document
from bson import ObjectId, Decimal128
from decimal import Decimal
from uuid import uuid4

from ..schema import ListFilter, SortDirection, Operator, FindUniqueByFieldInput, FieldRule, Aggregations, AggregationType, ReferenceField
from ..util.operator_mappings import logical_operator_map, apply_condition
from ..util.coerce_value import coerce_value
T = TypeVar("T", bound=BaseModel)
DocumentType = TypeVar("DocumentType", bound=Document)

class BaseRepository:
    """
    Base repository class for doing all the database operations using Beanie for NoSQL database.
    """

    def __init__(self, document: Type[DocumentType] = None, db: AsyncIOMotorDatabase = None):
        if document is None and db is None:
            raise ValidationError(detail="Either document or db must be provided")        
        self.document = document
        self.db = db

    def _convert_to_json_serializable(self, data: Any) -> Any:
        """
        Converts MongoDB documents to JSON-serializable format.
        """
        if data is None:
            return None
            
        # Fast path for common types
        if isinstance(data, (str, int, float, bool)):
            return data
            
        # Handle MongoDB specific types
        if isinstance(data, (ObjectId, Decimal128)):
            return str(data)
            
        if isinstance(data, datetime):
            return data.isoformat()
            
        if isinstance(data, Decimal):
            return float(data)
            
        # Handle collections
        if isinstance(data, dict):
            return {str(k): self._convert_to_json_serializable(v) for k, v in data.items()}
            
        if isinstance(data, (list, tuple, set)):
            return [self._convert_to_json_serializable(item) for item in data]
            
        # Handle Pydantic and Beanie models
        if isinstance(data, (BaseModel, Document)):
            return self._convert_to_json_serializable(data.model_dump())
            
        # Handle objects with __dict__
        if hasattr(data, '__dict__'):
            return self._convert_to_json_serializable(vars(data))
            
        # If we can't convert it, return string representation
        return str(data)

    def get_collection(self, collection_name: Optional[str] = None) -> Any:
        """Get the collection from the database"""
        return self.db[collection_name] if collection_name else self.document.get_motor_collection()
    
    def get_base_document_fields(self) -> Dict[str, Any]:
        """Get the base document fields"""
        return {
            "uuid": str(uuid4()),  
            "created_at": datetime.now(UTC),
            "updated_at": datetime.now(UTC)
        }

    async def _handle_mongo_error(self, operation: str, error: Exception) -> None:
        """Handle MongoDB errors consistently."""
        if isinstance(error, PyMongoError):
            raise GenericHttpError(
                status_code=500,
                detail=str(error),
                error_type="PyMongoError",
                message=f"Failed to {operation}"
            )
        raise error

    def _coerce_document(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coerce all values in a document to their appropriate types.
        This is used before saving to the database to ensure proper type conversion.
        """
        return coerce_value(data)

    async def create(self, obj: T, collection_name: Optional[str] = None) -> Dict[str, Any]:
        """Create a new document in the collection"""
        try:
            # Convert to dict and coerce values
            obj_dict = obj.model_dump() if hasattr(obj, 'model_dump') else dict(obj)
            obj_dict = self._coerce_document(obj_dict)
            
            if collection_name:
                collection = self.get_collection(collection_name)
                result = await collection.insert_one({**self.get_base_document_fields(), **obj_dict})
                return await self.get_by_attr("_id", result.inserted_id, collection_name)
            
            model_instance = self.document(**obj_dict)
            model = await model_instance.insert()
            return await self.get_by_attr("id", model.id)
            
        except Exception as e:
            await self._handle_mongo_error("create document", e)

    async def bulk_create(self, data: List[T], collection_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Create multiple documents in the collection"""
        try:
            # Convert to dicts and coerce values
            get_obj = lambda obj: obj.model_dump() if hasattr(obj, 'model_dump') else dict(obj)
            coerced_data = [self._coerce_document(get_obj(item)) for item in data]
            
            if collection_name:
                collection = self.get_collection(collection_name)
                documents = [{**self.get_base_document_fields(), **item} for item in coerced_data]
                result = await collection.insert_many(documents)
                # Convert the documents to JSON serializable format
                created_docs = []
                for doc in documents:
                    doc['_id'] = str(doc.get('_id', ''))
                    created_docs.append(self._convert_to_json_serializable(doc))
                return created_docs
            
            model_instances = [self.document(**item) for item in coerced_data]
            await self.document.insert_many(model_instances)
            return [self._convert_to_json_serializable(doc.model_dump()) for doc in model_instances]
            
        except Exception as e:
            await self._handle_mongo_error("bulk create documents", e)

    async def update(self, id: Union[str, ObjectId], obj: T, collection_name: Optional[str] = None) -> Dict[str, Any]:
        """Update a document by id"""
        try:
            # Convert to dict and coerce values
            obj_dict = obj.model_dump() if hasattr(obj, 'model_dump') else dict(obj)
            obj_dict = self._coerce_document(obj_dict)
            object_id = ObjectId(id) if isinstance(id, str) else id

            if collection_name:
                collection = self.get_collection(collection_name)
                result = await collection.update_one(
                    {"_id": object_id},
                    {"$set": obj_dict, "$currentDate": {"updated_at": True}}
                )
                
                if result.matched_count == 0:
                    raise NotFoundError(detail=f"Document with id {id} not found")
                
                return await self.get_by_attr("_id", object_id, collection_name)
            
            obj_dict["updated_at"] = datetime.now(UTC)
            result = await self.document.get(object_id)
            if not result:
                raise NotFoundError(detail=f"Document with id {id} not found")
                
            await result.update(Set(obj_dict))
            return await self.get_by_attr("id", object_id)
            
        except Exception as e:
            await self._handle_mongo_error("update document", e)

    async def get_by_attr(self, attr: Union[str, Dict[str, Any]], value: Any = None, collection_name: Optional[str] = None) -> Dict[str, Any]:
        try:
            # Handle multiple attributes
            if isinstance(attr, dict):
                query = {}
                for field, field_value in attr.items():
                    if field == "id":
                        field = "_id"
                        field_value = ObjectId(field_value)
                    query[field] = field_value
            else:
                if attr == "id":
                    attr = "_id"
                    value = ObjectId(value)
                query = {attr: value}

            if collection_name:
                collection = self.get_collection(collection_name)
                result = await collection.find_one(query)
                if not result:
                    raise NotFoundError(detail=f"Document with {attr}={value} not found")
                return self._convert_to_json_serializable(result)

            if not self.document:
                raise ValueError("Document class is not provided.")

            result = await self.document.find_one(query)
            if not result:
                raise NotFoundError(detail=f"Document with {attr}={value} not found")
            return self._convert_to_json_serializable(result)

        except Exception as e:
            await self._handle_mongo_error("get document", e)

    # async def get_all(self, find: ListFilter, collection_name: Optional[str] = None) -> Dict[str, Any]:
    #     """Get all documents with filtering, sorting, searching and pagination"""
    #     try:
    #         page = find.page or 1
    #         page_size = find.page_size or 20
    #         skip = (page - 1) * page_size

    #         collection = self.get_collection(collection_name) if collection_name else self.document.get_motor_collection()
    #         mongo_filter = self._build_query_filter(find,collection_name)

    #         count = await collection.count_documents(mongo_filter or {})
    #         query = collection.find(mongo_filter or {})
            
    #         if find.sort_order:
    #             query = query.sort(self._get_sort_order(find.sort_order))
            
    #         query = query.skip(skip).limit(page_size)
    #         data = await query.to_list(length=None) or []
            
    #         total_pages = (count + page_size - 1) // page_size
            
    #         return {
    #             "founds": self._convert_to_json_serializable(data),
    #             "search_options": {
    #                 "total_pages": total_pages,
    #                 "total_count": count,
    #                 "page": page,
    #                 "page_size": page_size,
    #                 "search": find.search,
    #                 "sort_order": find.sort_order
    #             }
    #         }
            
    #     except Exception as e:
    #         await self._handle_mongo_error("get documents", e)

    def _build_query_filter(self, find: ListFilter, collection_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Build MongoDB filter from ListFilter"""
        base_filter = self._build_filter_condition(find.filters.model_dump(), collection_name, is_expr=False) if find.filters else None

        if find.search and find.searchable_fields:
            search_filter = {"$or": self._build_search_conditions(find.search, find.searchable_fields)}
            return {"$and": [base_filter, search_filter]} if base_filter else search_filter

        return base_filter

    def _build_search_conditions(self, search_term: str, searchable_fields: List[str]) -> List[Dict[str, Any]]:
        """Build case-insensitive search conditions for fields"""
        regex = {"$regex": f".*{search_term}.*", "$options": "i"}
        return [{field: regex} for field in searchable_fields]

    def _get_sort_order(self, sort_order: List[Dict[str, Any]]) -> List[tuple]:
        """Generate sort tuples for MongoDB"""
        return [(s.field, ASCENDING if s.direction == SortDirection.ASC else DESCENDING) for s in sort_order] or [("_id", DESCENDING)]

    def _build_filter_condition(self, filter_dict: Dict[str, Any], collection_name: Optional[str] = None, is_expr: bool = False) -> Dict[str, Any]:
        """Recursively build MongoDB filter"""
        if not isinstance(filter_dict, dict):
            return {}

        if "operator" in filter_dict and "conditions" in filter_dict:
            conditions = [self._build_filter_condition(cond, collection_name, is_expr) for cond in filter_dict["conditions"]]
            return {logical_operator_map[filter_dict["operator"]]: conditions}

        if all(k in filter_dict for k in ["field", "operator", "value"]):
            try:
                model = self.document or self.db[collection_name]
                op = Operator(filter_dict["operator"].lower())
                if filter_dict["field"] == "id" or filter_dict["field"] == "_id":
                    if isinstance(filter_dict["value"], list):
                        value = [ObjectId(v) for v in filter_dict["value"]]
                    else:
                        value = ObjectId(filter_dict["value"])
                else:
                    value = coerce_value(filter_dict["value"])
                return apply_condition(model, op, filter_dict["field"], value, is_expr)
            except ValueError:
                raise BadRequestError(f"Invalid comparison operator: {filter_dict['operator']}")

        return {}

    async def get_all(self, find: ListFilter, collection_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve documents with filtering, sorting, and pagination"""
        page, page_size = find.page or 1, find.page_size or 20
        skip = (page - 1) * page_size
        pipeline = []

        if find.reference_fields:
            pipeline = self._build_reference_stage(pipeline, find.reference_fields)

        query_filter = self._build_query_filter(find, collection_name)
        if query_filter:
            pipeline.append({"$match": query_filter})

        if find.field_rules:
            pipeline = self._get_field_rule(find.field_rules, pipeline, collection_name)

        if find.sort_order:
            pipeline.append({"$sort": dict(self._get_sort_order(find.sort_order))})

        model = self.document or self.db[collection_name]

        # First get the total count before any aggregations or pagination
        count_pipeline = pipeline + [{"$count": "total"}]
        count_result = await model.aggregate(count_pipeline).to_list(length=1)
        total_count = count_result[0]["total"] if count_result else 0

        # Now add aggregations if needed
        if find.aggregations:
            group_stage = self._build_group_stage(find.aggregations)
            pipeline.append(group_stage)
            # For aggregations, we don't paginate the results
            data = await model.aggregate(pipeline).to_list(length=None)
            total_pages = 1
        else:
            # Add pagination only if no aggregations
            pipeline += [{"$skip": skip}, {"$limit": page_size}]
            data = await model.aggregate(pipeline).to_list(length=None)
            total_pages = (total_count + page_size - 1) // page_size

        return {
            "founds": self._convert_to_json_serializable(data),
            "search_options": {
                "total_pages": total_pages,
                "total_count": total_count,
                "page": page,
                "page_size": page_size,
                "search": find.search,
                "sort_order": find.sort_order,
            }
        }
    

    def _get_field_rule(
        self,
        field_rules: List[FieldRule],
        pipeline: List[Dict[str, Any]],
        collection_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Append field modifier stages to the aggregation pipeline."""
        if not field_rules:
            return pipeline

        field_rule_stages = self._build_field_rules_stage(field_rules, collection_name)
        pipeline.extend(field_rule_stages)
        return pipeline    
    
    def _build_field_rules_stage(
        self, field_rules: List[FieldRule], collection_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Build $addFields stages for dynamic array inclusion/exclusion logic"""
        stages = []

        for rule in field_rules:
            action = rule.action.lower()
            field_path = rule.field
            conditions = rule.conditions

            if not conditions or not conditions.conditions:
                continue

            if action not in ("include", "exclude"):
                raise ValueError(f"Unsupported filter action: {action}")

            condition_expr = self._build_filter_condition(
                filter_dict=conditions.model_dump(),
                collection_name=collection_name,
                is_expr=True
            )


            filter_condition = {"$not": [condition_expr]} if action == "exclude" else condition_expr

            stages.append({
                "$addFields": {
                    field_path: {
                        "$filter": {
                            "input": f"${field_path}",
                            "as": "item",
                            "cond": filter_condition,
                        }
                    }
                }
            })

        return stages

    
    def _build_reference_stage(
        self,
        pipeline: List[Dict[str, Any]],
        references: List[ReferenceField]
    ) -> List[Dict[str, Any]]:
        """
        Adds $set and $lookup stages to the pipeline for each reference.
        """

        for ref in references:
            local = ref.local_field
            foreign = ref.foreign_field
            from_collection = ref.foreign_entity
            as_field = ref.alias
            project_fields = ref.view_fields
            use_graph_lookup = ref.use_graph_lookup
            if foreign == "id" or foreign == "_id":
                foreign = "_id"
                # Convert string to ObjectId if needed
                pipeline.append({
                    "$set": {
                        local: {
                            "$switch": {
                                "branches": [
                                    {
                                        "case": { "$eq": [{ "$type": f"${local}" }, "array"] },
                                        "then": {
                                            "$map": {
                                                "input": f"${local}",
                                                "as": "id",
                                                "in": {
                                                    "$cond": {
                                                        "if": { "$eq": [{ "$type": "$$id" }, "string"] },
                                                        "then": {
                                                            "$convert": {
                                                                "input": "$$id",
                                                                "to": "objectId",
                                                                "onError": "$$id",
                                                                "onNull": "$$id"
                                                            }
                                                        },
                                                        "else": "$$id"
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    {
                                        "case": { "$eq": [{ "$type": f"${local}" }, "string"] },
                                        "then": {
                                            "$convert": {
                                                "input": f"${local}",
                                                "to": "objectId",
                                                "onError": f"${local}",
                                                "onNull": f"${local}"
                                            }
                                        }
                                    }
                                ],
                                "default": f"${local}"
                            }
                        }
                    }
                })

            if use_graph_lookup:
                # Use $graphLookup for recursive resolution
                pipeline.append({
                    "$graphLookup": {
                        "from": from_collection,
                        "startWith": f"${local}",
                        "connectFromField": use_graph_lookup.connect_from_field,
                        "connectToField": use_graph_lookup.connect_to_field,
                        "as": as_field,
                        "maxDepth": use_graph_lookup.max_depth,
                        "depthField": "depth"
                    }
                })
            else:
                # Standard $lookup
                pipeline.append({
                    "$lookup": {
                        "from": from_collection,
                        "localField": local,
                        "foreignField": foreign,
                        "as": as_field
                    }
                })

            if project_fields:
                pipeline.append({
                    "$addFields": {
                        as_field: {
                            "$cond": {
                                "if": { "$eq": [{ "$size": f"${as_field}" }, 0] },
                                "then": [],
                                "else": {
                                    "$map": {
                                        "input": f"${as_field}",
                                        "as": "item",
                                        "in": {field: f"$$item.{field}" for field in project_fields}
                                    }
                                }
                            }
                        }
                    }
                })

        return pipeline

    def _build_group_stage(self, group_agg: Aggregations) -> Dict[str, Any]:
        _id = {field: f"${field}" for field in group_agg.group_by} if group_agg.group_by else None
        group_stage = {"_id": _id}

        if group_agg.document_inclusion_mode == "all":
            group_stage["data"] = {"$push": "$$ROOT"}
        elif group_agg.document_inclusion_mode == "partial" and group_agg.included_fields:
            group_stage["data"] = {
                "$push": {field: f"${field}" for field in group_agg.included_fields}
            }
        if group_agg.aggregation_fields:
            for agg in group_agg.aggregation_fields:
                agg_type = agg.type.lower()
                field = agg.field
                alias = agg.alias


                if agg_type == "count":
                    group_stage[alias] = {"$sum": 1}
                elif agg_type in AggregationType:
                    group_stage[alias] = {f"${agg_type}": f"${field}"}
                else:
                    raise ValueError(f"Unsupported aggregation type: {agg_type}")

        return {"$group": group_stage}
    
    async def delete(self, id: Union[str, ObjectId], collection_name: Optional[str] = None) -> bool:
        """Delete a document by id"""
        try:
            object_id = ObjectId(id) if isinstance(id, str) else id
            
            if collection_name:
                collection = self.get_collection(collection_name)
                result = await collection.delete_one({"_id": object_id})
                if result.deleted_count == 0:
                    raise NotFoundError(detail="Document not found")
            else:
                result = await self.document.get(object_id)
                if not result:
                    raise NotFoundError(detail="Document not found")
                await result.delete()
                
            return True
            
        except Exception as e:
            await self._handle_mongo_error("delete document", e)

    async def delete_many(self, attr: Union[str, Dict[str, Any]], value: Any = None, collection_name: Optional[str] = None) -> bool:
        """Delete multiple documents by attribute"""
        try:
            query = {}
            if isinstance(attr,dict):
                for key,value in attr.items():
                    query[key] = value
            else:
                query = {attr: value}
            
            if collection_name:
                collection = self.get_collection(collection_name)
                result = await collection.delete_many(query)
                return result.deleted_count
            else:
                result = await self.document.find(query).delete_many()
                return result.deleted_count
        except Exception as e:
            await self._handle_mongo_error("delete documents", e)
                

    async def get_unique_values(self, schema: FindUniqueByFieldInput, collection_name: Optional[str] = None) -> Dict[str, Any]:
        """Get unique values for a field with pagination and search"""
        try:
            if not schema.field_name:
                raise BadRequestError(detail="Field name is required")

            collection = self.get_collection(collection_name) if collection_name else self.document.get_motor_collection()
            
            pipeline = []
            
            if schema.search:
                pipeline.append({
                    "$match": {
                        schema.field_name: {"$regex": f".*{schema.search}.*", "$options": "i"}
                    }
                })
            
            pipeline.append({"$group": {"_id": f"${schema.field_name}"}})
            
            if schema.ordering:
                pipeline.append({
                    "$sort": {
                        "_id": ASCENDING if schema.ordering == "asc" else DESCENDING
                    }
                })
            
            count_pipeline = pipeline + [{"$count": "total"}]
            count_result = await collection.aggregate(count_pipeline).to_list(length=1)
            total_count = count_result[0]["total"] if count_result else 0
            
            skip = ((schema.page or 1) - 1) * (schema.page_size or 10)
            pipeline.extend([
                {"$skip": skip},
                {"$limit": schema.page_size or 10}
            ])
            
            results = await collection.aggregate(pipeline).to_list(length=None)
            values = [r["_id"] for r in results]
            
            return {
                "founds": values,
                "search_options": {
                    "page": schema.page or 1,
                    "page_size": schema.page_size or 10,
                    "ordering": schema.ordering or "asc",
                    "total_count": total_count
                }
            }
            
        except Exception as e:
            await self._handle_mongo_error("get unique values", e)