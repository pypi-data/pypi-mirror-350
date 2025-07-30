# utils/agg_builder.py

from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from .exceptions import InvalidLookupError, PipelineSerializationError, InvalidStageError
from .models import (
    Stage, MatchStage, ProjectStage, SortStage, LimitStage, SkipStage,
    UnwindStage, GroupStage, AddFieldsStage, ReplaceRootStage, LookupStage,
    FacetStage, RedactStage, CommentStage, Pipeline
)

class AggBuilder:
    """
    Fluent builder for constructing MongoDB aggregation pipelines.

    Example:
        pipeline = (
            AggBuilder()
            .match({"status": "active"})
            .lookup(
                from_="products",
                let_={"productId": "$productId"},
                pipeline=[
                    AggBuilder.match_expr({"$eq": ["$productId", "$$productId"]}),
                    AggBuilder.project({"title": 1})
                ],
                as_="productDetails"
            )
            .unwind("$productDetails")
            .project({"_id": 1, "productDetails": 1})
            .build()
        )
    """

    def __init__(self, pipeline: Optional[Pipeline] = None) -> None:
        """Initialize a new AggBuilder instance with an empty pipeline."""
        self._pipeline: Pipeline = pipeline or Pipeline()

    def add(self, stage: Union[Stage, Dict[str, Any]]) -> "AggBuilder":
        """
        Add a stage to the pipeline.
        
        Args:
            stage: Either a Stage object or a raw MongoDB stage dictionary
            
        Returns:
            AggBuilder: The builder instance for method chaining
            
        Example:
            # Using a Stage object
            builder.add(MatchStage(match={"status": "active"}))
            
            # Using a raw dictionary
            builder.add({"$match": {"status": "active"}})
        """
        if isinstance(stage, Stage):
            self._pipeline.stages.append(stage.to_mongo())
        else:
            # Validate the raw dictionary format
            if not isinstance(stage, dict):
                raise InvalidStageError(f"Stage must be a dictionary, got {type(stage)}")
            
            if len(stage) != 1:
                raise InvalidStageError(f"Stage must have exactly one key, got {len(stage)}")
            
            stage_name = list(stage.keys())[0]
            if not stage_name.startswith('$'):
                raise InvalidStageError(f"Stage operator must start with '$', got '{stage_name}'")
            
            self._pipeline.stages.append(stage)
        return self

    def match(self, query: Dict[str, Any]) -> AggBuilder:
        """
        Add a $match stage to filter documents.
        
        Args:
            query: The query criteria to match documents
            
        Returns:
            AggBuilder: The builder instance for method chaining
            
        Example:
            builder.match({"status": "active", "age": {"$gt": 18}})
        """
        return self.add(MatchStage(match=query))

    def filter(self, query: Dict[str, Any]) -> AggBuilder:
        """
        Alias for match(). Adds a $match stage to filter documents.
        
        Args:
            query: The query criteria to match documents
            
        Returns:
            AggBuilder: The builder instance for method chaining
        """
        return self.match(query)

    def match_expr(self, expr: Dict[str, Any]) -> "AggBuilder":
        """
        Returns a $match stage using $expr, used inside lookups.
        
        Args:
            expr: The expression to evaluate
            
        Returns:
            Dict[str, Any]: A $match stage with $expr
            
        Example:
            builder.match_expr({"$eq": ["$field1", "$field2"]})
        """
        return self.add(MatchStage(match={"$expr": expr}))

    def expr(self, expr: Dict[str, Any]) -> "AggBuilder":
        """
        Adds a $match stage using $expr, used inside lookups.
        
        Args:
            expr: The expression to evaluate
            
        Returns:
            AggBuilder: The builder instance for method chaining
        """
        return self.add(MatchStage(match={"$expr": expr}))
    
    def project(self, fields: Dict[str, Any]) -> AggBuilder:
        """
        Add a $project stage to reshape documents.
        
        Args:
            fields: Field specifications to include/exclude (1/0 or true/false)
            
        Returns:
            AggBuilder: The builder instance for method chaining
            
        Example:
            builder.project({"name": 1, "age": 1, "_id": 0})
        """
        return self.add(ProjectStage(project=fields))

    def fields(self, fields: Dict[str, Union[int, bool]]) -> AggBuilder:
        """
        Alias for project(). Add a $project stage to reshape documents.
        
        Args:
            fields: Field specifications to include/exclude (1/0 or true/false)
            
        Returns:
            AggBuilder: The builder instance for method chaining
        """
        return self.project(fields)

    def safe_project(self, fields: List[str]) -> AggBuilder:
        """
        Creates a projection stage that includes only the specified fields.
        Each field will be included with value 1 (included).
        
        Args:
            fields: List of field names to include in the projection
            
        Returns:
            AggBuilder: The builder instance for method chaining
            
        Example:
            builder.safe_project(["name", "age", "email"])
            # Equivalent to: builder.project({"name": 1, "age": 1, "email": 1})
        """
        projection = {field: 1 for field in fields}
        return self.project(projection)

    def select(self, fields: List[str]) -> AggBuilder:
        """
        Alias for safe_project(). Creates a projection stage that includes only the specified fields.
        
        Args:
            fields: List of field names to include in the projection
            
        Returns:
            AggBuilder: The builder instance for method chaining
        """
        return self.safe_project(fields)

    def sort(self, fields: Dict[str, Union[int, bool]]) -> AggBuilder:
        """
        Add a $sort stage to order documents.
        
        Args:
            fields: Field specifications with sort direction (1 for ascending, -1 for descending)
            
        Returns:
            AggBuilder: The builder instance for method chaining
            
        Example:
            builder.sort({"age": 1, "name": -1})
        """
        return self.add(SortStage(sort=fields))

    def order_by(self, fields: Dict[str, Union[int, bool]]) -> AggBuilder:
        """
        Alias for sort(). Add a $sort stage to order documents.
        
        Args:
            fields: Field specifications with sort direction (1 for ascending, -1 for descending)
            
        Returns:
            AggBuilder: The builder instance for method chaining
        """
        return self.sort(fields)

    def limit(self, n: int) -> AggBuilder:
        """
        Add a $limit stage to restrict the number of documents.
        
        Args:
            n: Maximum number of documents to return
            
        Returns:
            AggBuilder: The builder instance for method chaining
            
        Example:
            builder.limit(10)
        """
        return self.add(LimitStage(limit=n))

    def skip(self, n: int) -> AggBuilder:
        """
        Add a $skip stage to skip documents.
        
        Args:
            n: Number of documents to skip
            
        Returns:
            AggBuilder: The builder instance for method chaining
            
        Example:
            builder.skip(5)
        """
        return self.add(SkipStage(skip=n))

    def unwind(self, path: str, preserve_null_and_empty: bool = True) -> AggBuilder:
        """
        Add a $unwind stage to deconstruct an array field.
        
        Args:
            path: The array field path to unwind
            preserve_null_and_empty: Whether to preserve documents with null or empty arrays
            
        Returns:
            AggBuilder: The builder instance for method chaining
            
        Example:
            builder.unwind("$tags")
        """
        return self.add(UnwindStage(path=path, preserve_null_and_empty=preserve_null_and_empty))

    def group(self, id_field: Any, **accumulators: Any) -> AggBuilder:
        """
        Add a $group stage to group documents.
        
        Args:
            id_field: The group key expression
            **accumulators: Accumulator expressions for grouped values
            
        Returns:
            AggBuilder: The builder instance for method chaining
            
        Example:
            builder.group("$department", total={"$sum": "$salary"})
        """
        return self.add(GroupStage(id_field=id_field, accumulators=accumulators))

    def add_fields(self, fields: Dict[str, Any]) -> AggBuilder:
        """
        Add an $addFields stage to add new fields.
        
        Args:
            fields: New field specifications
            
        Returns:
            AggBuilder: The builder instance for method chaining
            
        Example:
            builder.add_fields({"total": {"$add": ["$price", "$tax"]}})
        """
        return self.add(AddFieldsStage(fields=fields))

    def replace_root(self, new_root: Dict[str, Any]) -> AggBuilder:
        """
        Add a $replaceRoot stage to replace the document root.
        
        Args:
            new_root: The new root document expression
            
        Returns:
            AggBuilder: The builder instance for method chaining
            
        Example:
            builder.replace_root({"$arrayElemAt": ["$items", 0]})
        """
        return self.add(ReplaceRootStage(new_root=new_root))

    def lookup(
        self,
        from_: str,
        as_: str,
        local_field: Optional[str] = None,
        foreign_field: Optional[str] = None,
        let_: Optional[Dict[str, Any]] = None,
        pipeline: Optional[Union[List[Union[Dict[str, Any], AggBuilder]], AggBuilder]] = None,
    ) -> AggBuilder:
        """
        Add a $lookup stage to perform a join-like operation.
        
        Args:
            from_: The collection to join with
            as_: The output array field name
            local_field: The field from the input documents
            foreign_field: The field from the documents of the "from" collection
            let_: Variables to use in the pipeline field
            pipeline: The pipeline to run on the joined collection. Can be a list of stages or an AggBuilder instance
            
        Returns:
            AggBuilder: The builder instance for method chaining
            
        Example:
            builder.lookup(
                from_="orders",
                local_field="userId",
                foreign_field="userId",
                as_="orders"
            )
        """
        if pipeline is not None:
            stages = []
            if isinstance(pipeline, AggBuilder):
                stages = pipeline.build()
            else:
                for p in pipeline:
                    if isinstance(p, AggBuilder):
                        stages.extend(p.build())
                    else:
                        stages.append(p)
            return self.add(LookupStage(
                from_=from_,
                as_=as_,
                let_=let_,
                pipeline=stages,
                local_field=local_field,
                foreign_field=foreign_field
            ))
        else:
            if not local_field or not foreign_field:
                raise InvalidLookupError("Both 'local_field' and 'foreign_field' are required for non-pipeline lookups.")
            return self.add(LookupStage(
                from_=from_,
                as_=as_,
                local_field=local_field,
                foreign_field=foreign_field,
                let_=let_,
                pipeline=pipeline
            ))

    def facet(self, **pipelines: List[Dict[str, Any]]) -> AggBuilder:
        """
        Add a $facet stage to process multiple aggregation pipelines.
        
        Args:
            **pipelines: Named aggregation pipelines
            
        Returns:
            AggBuilder: The builder instance for method chaining
            
        Example:
            builder.facet(
                categories=[{"$group": {"_id": "$category"}}],
                total=[{"$count": "total"}]
            )
        """
        return self.add(FacetStage(pipelines=pipelines))

    def redact(self, condition: Dict[str, Any]) -> AggBuilder:
        """
        Add a $redact stage to restrict document contents.
        
        Args:
            condition: The condition expression
            
        Returns:
            AggBuilder: The builder instance for method chaining
            
        Example:
            builder.redact({"$cond": {"if": {"$eq": ["$level", 5]}, "then": "$$DESCEND", "else": "$$PRUNE"}})
        """
        return self.add(RedactStage(condition=condition))

    def comment(self, text: str) -> AggBuilder:
        """
        Add a $comment stage for observability and debugging.
        
        Args:
            text: The comment text to add to the pipeline
            
        Returns:
            AggBuilder: The builder instance for method chaining
            
        Example:
            builder.comment("Find active users and their orders")
        """
        return self.add(CommentStage(text=text))

    def build(self) -> List[Dict[str, Any]]:
        """
        Returns the finalized aggregation pipeline.
        
        Returns:
            List[Dict[str, Any]]: The complete MongoDB aggregation pipeline
            
        Example:
            pipeline = builder.match({"status": "active"}).project({"name": 1}).build()
        """
        self.validate_pipeline()
        return self._pipeline.stages.copy()

    def validate_pipeline(self) -> None:
        """
        Validates the aggregation pipeline for common issues.
        Raises InvalidStageError if any issues are found.
        
        Raises:
            InvalidStageError: If the pipeline contains invalid stages
        """
        for i, stage in enumerate(self._pipeline.stages):
            if not isinstance(stage, dict):
                raise InvalidStageError(f"Stage {i} must be a dictionary, got {type(stage)}")
            
            if len(stage) != 1:
                raise InvalidStageError(f"Stage {i} must have exactly one key, got {len(stage)}")
            
            stage_name = list(stage.keys())[0]
            if not stage_name.startswith('$'):
                raise InvalidStageError(f"Stage {i} operator must start with '$', got '{stage_name}'")
            
            stage_value = stage[stage_name]
            
            # Validate $lookup stages
            if stage_name == '$lookup':
                if not isinstance(stage_value, dict):
                    raise InvalidStageError(f"$lookup stage {i} value must be a dictionary")
                
                if 'from' not in stage_value:
                    raise InvalidStageError(f"$lookup stage {i} missing required 'from' field")
                
                if 'as' not in stage_value:
                    raise InvalidStageError(f"$lookup stage {i} missing required 'as' field")
                
                # For non-pipeline lookups
                if 'pipeline' not in stage_value:
                    if 'localField' not in stage_value:
                        raise InvalidStageError(f"$lookup stage {i} missing required 'localField' for non-pipeline lookup")
                    if 'foreignField' not in stage_value:
                        raise InvalidStageError(f"$lookup stage {i} missing required 'foreignField' for non-pipeline lookup")
                
                # For pipeline lookups
                if 'pipeline' in stage_value:
                    if not isinstance(stage_value['pipeline'], list):
                        raise InvalidStageError(f"$lookup stage {i} pipeline must be a list")
                    if 'let' not in stage_value:
                        raise InvalidStageError(f"$lookup stage {i} with pipeline requires 'let' field")

            # Validate $match stages
            elif stage_name == '$match':
                if not isinstance(stage_value, dict):
                    raise InvalidStageError(f"$match stage {i} value must be a dictionary")

            # Validate $project stages
            elif stage_name == '$project':
                if not isinstance(stage_value, dict):
                    raise InvalidStageError(f"$project stage {i} value must be a dictionary")

            # Validate $sort stages
            elif stage_name == '$sort':
                if not isinstance(stage_value, dict):
                    raise InvalidStageError(f"$sort stage {i} value must be a dictionary")
                for field, direction in stage_value.items():
                    if direction not in (1, -1):
                        raise InvalidStageError(f"$sort stage {i} direction must be 1 or -1, got {direction}")

            # Validate $limit and $skip stages
            elif stage_name in ('$limit', '$skip'):
                if not isinstance(stage_value, int) or stage_value < 0:
                    raise InvalidStageError(f"{stage_name} stage {i} value must be a non-negative integer")

            # Validate $unwind stages
            elif stage_name == '$unwind':
                if isinstance(stage_value, str):
                    continue  # Simple path syntax is valid
                if not isinstance(stage_value, dict):
                    raise InvalidStageError(f"$unwind stage {i} value must be a string or dictionary")
                if 'path' not in stage_value:
                    raise InvalidStageError(f"$unwind stage {i} missing required 'path' field")

    def to_json(self) -> str:
        """
        Serializes the pipeline to a formatted JSON string.
        Useful for debugging and logging.
        
        Returns:
            str: Formatted JSON string representation of the pipeline
            
        Example:
            json_str = builder.to_json()
            print(json_str)
        """
        try:
            import json
            return json.dumps(self._pipeline.stages, indent=2, default=str)
        except (TypeError, ValueError) as e:
            raise PipelineSerializationError(f"Failed to serialize pipeline: {str(e)}")

    def print_pretty(self) -> None:
        """
        Prints the pipeline in a formatted, readable JSON format.
        Useful for debugging in development.
        
        Example:
            builder.print_pretty()
        """
        print(self.to_json())

    def __repr__(self) -> str:
        """
        Returns a string representation of the AggBuilder instance.
        
        Returns:
            str: A string showing the number of stages in the pipeline
        """
        return f"AggBuilder({len(self._pipeline.stages)} stages)"